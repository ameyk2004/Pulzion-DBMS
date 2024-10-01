from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import connection_uri, queries
from app.services.metadata_service import generate_metadata
from app.config import connection_uri, queries
from app.services.metadata_service import generate_metadata
import requests

import json

from app.services.query_service import generate_query

API_KEY = 'sk-96f006f61ebd416ea5b99c9ecaece174'  # Replace with your actual API key
WORQHAT_URL = 'https://api.worqhat.com/api/ai/content/v3' 

# Define a Pydantic model for the request body
class QueryRequest(BaseModel):
    query: str 
    model: str

router = APIRouter()


@router.post("/query")
async def send_query(request: QueryRequest):

    nlp_query = request.query
    model = request.model
    print(f"NLP Query: {nlp_query}")
    print(f"Model : {model}")

    sql_query = generate_query(nlp_query, model)

    return {"query" : sql_query}


