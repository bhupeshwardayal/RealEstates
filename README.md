# AI-Powered Real Estate Advisor & Property Matcher

[![SRS Compliance](https://img.shields.io/badge/SRS%20Spec-Version%201.0-emerald.svg)](./DESIGN.md)
[![Vector Index](https://img.shields.io/badge/Vector%20Search-FAISS%20IndexFlatIP-064E3B.svg)](./app/vector_store/)
[![Framework](https://img.shields.io/badge/Backend-FastAPI%20%2B%20SQLAlchemy-003527.svg)](./app/main.py)
[![Stitch Design](https://img.shields.io/badge/Stitch%20Theme-Sovereign%20Asset%20%26%20Capital-10b981.svg)](./.stitch/metadata.json)

> **Software Requirements Specification (SRS v1.0) Implementation**  
> **Author:** Bhupeshwar Dayal  
> **Institution:** G. H. Raisoni College of Engineering, Nagpur  
> **Department:** Department of Information Technology  
> **Target Stack:** Python 3.13, FAISS, SQLAlchemy, FastAPI, Tailwind CSS, Plus Jakarta Sans & Inter  

---

## 🏛️ System Overview

The **AI-Powered Real Estate Advisor & Property Matcher** bridges the gap between unstructured conversational human intent and structured property inventory. Traditional real estate search engines rely on rigid drop-down filters that fail when buyers express complex multi-faceted constraints (e.g., *"Looking for a 2 or 3 BHK near an IT park in Pune under 85 Lakhs with good school connectivity and an estimated monthly EMI below 50,000 INR"*).

This application implements the complete 3-tier architecture specified in the SRS:
1. **Presentation Tier:** A responsive, bright luxury proptech interface generated and styled using **Google Stitch** (`Sovereign Asset & Capital` design system) featuring interactive conversational chat, dynamic loan amortization sliders, and grounded property cards.
2. **Orchestration & RAG Tier:** Deterministic intent extraction, multi-vector similarity scoring, strict zero-hallucination grounded prompts, and mathematical financial engines.
3. **Data Tier:** In-memory dense vector indexing (**FAISS**) coupled with relational schema persistence (**SQLAlchemy** / PostgreSQL compatibility).

---

## 🧩 Architectural Modules

```
RealEstates/
├── .stitch/                          # Google Stitch Project Artifacts
│   ├── metadata.json                 # Project ID & Screen tracking
│   └── designs/
│       └── screen_9321b591.html      # Downloaded high-fidelity Stitch screen
├── DESIGN.md                         # Semantic Design System specification
├── requirements.txt                  # Python dependencies
├── app/
│   ├── config.py                     # App configuration & vector index paths
│   ├── main.py                       # FastAPI application & entry point
│   ├── database/
│   │   ├── db.py                     # SQLAlchemy models (properties & user_conversations)
│   │   └── seed_data.py              # Realistic Indian property catalog (Pune, Mumbai, Nagpur, etc.)
│   ├── vector_store/
│   │   ├── embedder.py               # L2-normalized dense vector embeddings
│   │   └── indexer.py                # FAISS IndexFlatIP persistence & sub-50ms retrieval
│   ├── rag/
│   │   ├── intent.py                 # Hard constraint & soft semantic intent extractor
│   │   ├── engine.py                 # Grounded RAG generator with fallback handling
│   │   └── financial.py              # Decimal EMI & gross rental yield calculator
│   └── api/
│       └── routes.py                 # REST API endpoints (/chat, /properties, /financial/emi)
├── frontend/
│   └── templates/
│       └── index.html                # Bright luxury UI matching Stitch design tokens
└── tests/
    ├── test_financial.py             # EMI & rental yield precision tests
    ├── test_vector_search.py         # FAISS vector similarity & latency benchmarks
    └── test_rag.py                   # Grounding & zero-hallucination tests
```

---

## 🎨 Front-End & Stitch Design System

The visual language follows the **Sovereign Asset & Capital** design system generated via Stitch:
- **Atmosphere:** Bright, sunlit architectural luxury, pristine neutral backgrounds (`#FAF8FF`, `#FFFFFF`), deep imperial emerald accents (`#003527`, `#064E3B`), and surgical micro-borders (`#E2E8F0`).
- **Typography:** Display and quantitative valuations in **Plus Jakarta Sans** with `tabular-nums` enabled to avoid optical shift during dynamic recalculations. Body text in **Inter**.
- **Interactive Components:**
  - **Conversational Console:** Natural language search stream with RERA verification badges and quick prompt chips.
  - **Dynamic Financial Simulator:** Dual-slider controls for Property Value, Down Payment, Loan Tenure, and Interest Rate. Real-time dynamic recalculations of monthly EMI, Gross Yield, and LTV.
  - **Property Dossier Cards:** RERA registration badges, AI Match confidence scores, carpet area, configuration, and direct modal inspection triggers.
  - **Modals:** Grounding Inspector Modal and 5-Year Amortization Schedule Table.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Pip package manager

### 2. Installation
Clone or navigate to the project directory:
```bash
cd c:\Users\Acer\Desktop\RealEstates
pip install -r requirements.txt
```

### 3. Run the Automated Test Suite
Verify that all 10 unit and latency benchmarks pass:
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### 4. Start the Application Server
Run the FastAPI application with Uvicorn:
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser at:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📡 API Specification Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the interactive Bright Luxury Web Application |
| `GET` | `/api/health` | Health probe, FAISS vector count, and engine status |
| `GET` | `/api/properties` | List catalog properties with filtering options (city, BHK, price) |
| `GET` | `/api/properties/{id}` | Detailed property profile with RERA and financial metadata |
| `POST` | `/api/chat` | Conversational RAG property search with grounding verification |
| `POST` | `/api/financial/emi` | Deterministic EMI and amortization schedule calculation |
| `POST` | `/api/financial/yield` | Gross rental yield and annual cash-flow estimation |

---

## 📐 Mathematical Formulas (Module 4)

### 1. Equated Monthly Installment (EMI)
$$\text{EMI} = P \cdot r \cdot \frac{(1 + r)^n}{(1 + r)^n - 1}$$
- $P$: Principal loan amount (in INR)
- $r$: Monthly interest rate ($\frac{\text{annual rate}}{12 \times 100}$)
- $n$: Total repayment tenure in months

### 2. Gross Rental Yield
$$\text{Gross Rental Yield (\%)} = \left(\frac{\text{Annual Expected Rent}}{\text{Total Property Purchase Price}}\right) \times 100$$

---

## 📜 Academic Attribution
Developed in accordance with the requirements specification authored by:
- **Bhupeshwar Dayal**
👉 https://realestates-ai-advisor.onrender.com

