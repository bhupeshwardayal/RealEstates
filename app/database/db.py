import json
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"

    property_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    locality = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False)
    price_inr = Column(Float, nullable=False)
    bhk_count = Column(Integer, nullable=False)
    carpet_area_sqft = Column(Integer, nullable=False)
    amenities = Column(JSON, default=list)  # Stored as JSON array
    possession_status = Column(String(50), default="Ready to Move")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    rera_id = Column(String(100), nullable=True)
    annual_rent_estimate = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        amenities_val = self.amenities
        if isinstance(amenities_val, str):
            try:
                amenities_val = json.loads(amenities_val)
            except Exception:
                amenities_val = [amenities_val]

        return {
            "property_id": self.property_id,
            "title": self.title,
            "locality": self.locality,
            "city": self.city,
            "price_inr": float(self.price_inr),
            "bhk_count": self.bhk_count,
            "carpet_area_sqft": self.carpet_area_sqft,
            "amenities": amenities_val or [],
            "possession_status": self.possession_status,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "description": self.description or "",
            "image_url": self.image_url or "",
            "rera_id": self.rera_id or "RERA-VERIFIED",
            "annual_rent_estimate": float(self.annual_rent_estimate or (self.price_inr * 0.05)),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def to_context_chunk(self) -> str:
        """
        Unified contextual text blob as specified in SRS Section 4.2:
        Context Chunk = "Property: {title} | Location: {locality}, {city} | 
                         Price: INR {price_inr} | Specs: {bhk_count} BHK, 
                         {carpet_area_sqft} sqft | Amenities: {amenities} | 
                         Description: {description}"
        """
        amenities_str = ", ".join(self.amenities) if isinstance(self.amenities, list) else str(self.amenities)
        return (
            f"Property: {self.title} | Location: {self.locality}, {self.city} | "
            f"Price: INR {self.price_inr:,.0f} | Specs: {self.bhk_count} BHK, "
            f"{self.carpet_area_sqft} sqft | Amenities: {amenities_str} | "
            f"Description: {self.description or ''}"
        )

class UserConversation(Base):
    __tablename__ = "user_conversations"

    session_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_query = Column(Text, nullable=False)
    retrieved_property_ids = Column(JSON, default=list)
    ai_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Engine & Session
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

