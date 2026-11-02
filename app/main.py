import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.database.seed_data import seed_properties
from app.vector_store.indexer import vector_index

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="AI-Powered Real Estate Advisor & Property Matcher",
    description="Full-Stack RAG & FAISS Real Estate Matching Architecture as specified in SRS v1.0",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and Templates configuration
static_dir = BASE_DIR / "frontend" / "static"
static_dir.mkdir(parents=True, exist_ok=True)
templates_dir = BASE_DIR / "frontend" / "templates"
templates_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

# Include API Router
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    print("🚀 Initializing database and property inventory...")
    seed_properties()
    print("🧠 Initializing FAISS vector embeddings...")
    vector_index.load_or_build()
    print("✅ System ready.")

@app.get("/")
def serve_home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/srs")
def serve_srs_document(request: Request):
    return templates.TemplateResponse(request=request, name="srs.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

