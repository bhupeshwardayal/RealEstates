from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.database.db import get_db, Property, UserConversation
from app.rag.engine import RealEstateRAGEngine
from app.rag.financial import FinancialEngine
from app.vector_store.indexer import vector_index

router = APIRouter()
rag_engine = RealEstateRAGEngine()

# Pydantic Schemas
class ChatRequest(BaseModel):
    query: str = Field(..., description="Conversational property search query")
    session_id: Optional[str] = Field(None, description="Session ID for multi-turn context")
    previous_context: Optional[Dict[str, Any]] = None

class EMICalculationRequest(BaseModel):
    principal: float = Field(..., description="Loan principal in INR")
    interest_rate_pct: float = Field(8.5, description="Annual interest rate in %")
    tenure_years: int = Field(20, description="Loan tenure in years")

class YieldCalculationRequest(BaseModel):
    annual_rent: float = Field(..., description="Estimated annual rent in INR")
    purchase_price: float = Field(..., description="Total purchase price in INR")

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "vector_index_size": vector_index.index.ntotal if vector_index.index else 0,
        "engine": "FAISS + RAG LangChain Spec v1.0",
        "hallucination_guard": "STRICT_ACTIVE"
    }

@router.get("/properties")
def list_properties(
    city: Optional[str] = None,
    locality: Optional[str] = None,
    bhk: Optional[int] = None,
    max_price: Optional[float] = None,
    possession: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Property)
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if locality:
        query = query.filter(Property.locality.ilike(f"%{locality}%"))
    if bhk:
        query = query.filter(Property.bhk_count >= bhk)
    if max_price:
        query = query.filter(Property.price_inr <= max_price)
    if possession:
        query = query.filter(Property.possession_status == possession)

    properties = query.all()
    results = []
    for p in properties:
        p_dict = p.to_dict()
        loan_principal = p_dict["price_inr"] * 0.80
        emi_data = FinancialEngine.calculate_emi(loan_principal, 8.5, 20)
        yield_data = FinancialEngine.calculate_rental_yield(p_dict["annual_rent_estimate"], p_dict["price_inr"])
        p_dict["calculated_emi"] = emi_data["monthly_emi"]
        p_dict["calculated_yield_pct"] = yield_data["gross_yield_pct"]
        p_dict["price_per_sqft"] = FinancialEngine.calculate_price_per_sqft(p_dict["price_inr"], p_dict["carpet_area_sqft"])
        results.append(p_dict)
    return results

@router.get("/properties/{property_id}")
def get_property_detail(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    p_dict = prop.to_dict()
    loan_principal = p_dict["price_inr"] * 0.80
    emi_data = FinancialEngine.calculate_emi(loan_principal, 8.5, 20)
    yield_data = FinancialEngine.calculate_rental_yield(p_dict["annual_rent_estimate"], p_dict["price_inr"])
    amortization = FinancialEngine.generate_amortization_schedule(loan_principal, 8.5, 20, max_years_displayed=5)
    
    p_dict["financials"] = {
        "emi_data": emi_data,
        "yield_data": yield_data,
        "amortization_preview": amortization,
        "price_per_sqft": FinancialEngine.calculate_price_per_sqft(p_dict["price_inr"], p_dict["carpet_area_sqft"])
    }
    return p_dict

@router.post("/chat")
def chat_query(req: ChatRequest, db: Session = Depends(get_db)):
    result = rag_engine.process_query(req.query, req.previous_context)
    
    # Log conversation to database (FR-2.2 and Section 4.1 Schema)
    try:
        conv = UserConversation(
            session_id=req.session_id,
            user_query=req.query,
            retrieved_property_ids=[p["property_id"] for p in result["properties"]],
            ai_response=result["ai_response"]
        )
        db.add(conv)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Conversation log error: {e}")

    return result

@router.post("/financial/emi")
def calculate_emi_endpoint(req: EMICalculationRequest):
    emi_data = FinancialEngine.calculate_emi(req.principal, req.interest_rate_pct, req.tenure_years)
    schedule = FinancialEngine.generate_amortization_schedule(req.principal, req.interest_rate_pct, req.tenure_years, max_years_displayed=5)
    return {
        "summary": emi_data,
        "amortization_schedule": schedule
    }

@router.post("/financial/yield")
def calculate_yield_endpoint(req: YieldCalculationRequest):
    return FinancialEngine.calculate_rental_yield(req.annual_rent, req.purchase_price)

