from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.agent import TitanicAgent
from app.utils.data_loader import get_dataset_info

app = FastAPI(title="Titanic Dataset ChatBot API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a dependency for our agent
def get_agent():
    api_key = os.environ.get("OPENAI_API_KEY")
    return TitanicAgent(api_key=api_key)

class QueryRequest(BaseModel):
    query: str
    api_key: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    visualization_type: Optional[str] = None
    success: bool

@app.get("/")
def read_root():
    return {"message": "Titanic Dataset ChatBot API is running"}

@app.get("/dataset-info")
def dataset_information():
    """Get basic information about the Titanic dataset"""
    return get_dataset_info()

@app.post("/query", response_model=QueryResponse)
def process_query(query_request: QueryRequest, agent: TitanicAgent = Depends(get_agent)):
    """Process a natural language query about the Titanic dataset"""
    if query_request.api_key:
        # If API key provided in request, create a new agent with it
        agent = TitanicAgent(api_key=query_request.api_key)
    
    response = agent.process_query(query_request.query)
    return response

@app.post("/query-form")
def process_query_form(
    query: str = Form(...),
    api_key: Optional[str] = Form(None),
    agent: TitanicAgent = Depends(get_agent)
):
    """Form-based endpoint for processing queries (useful for Streamlit)"""
    if api_key:
        # If API key provided in form, create a new agent with it
        agent = TitanicAgent(api_key=api_key)
    
    response = agent.process_query(query)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)