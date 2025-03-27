from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from .utils.summarize import get_news_insights
from .routers import auth, search_terms
from .mongodb.models import UserModel, SearchTermModel
from .mongodb.config import db

app = FastAPI(title="News AI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(search_terms.router)

class SearchRequest(BaseModel):
    search_term: str
    num_results: int = 5

class Insight(BaseModel):
    insight: str
    source_title: str
    source_link: str

@app.post("/api/insights", response_model=List[Insight])
async def get_insights(request: SearchRequest):
    try:
        insights = get_news_insights(request.search_term, request.num_results)
        if not insights:
            raise HTTPException(status_code=404, detail="No insights found")
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Create MongoDB indexes on startup
@app.on_event("startup")
async def startup_db_client():
    UserModel.create_indexes(db)
    SearchTermModel.create_indexes(db)
    print("MongoDB connection established and indexes created")

# Close MongoDB connection on shutdown
@app.on_event("shutdown")
async def shutdown_db_client():
    from .mongodb.config import client
    client.close()
    print("MongoDB connection closed")