from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import connection_uri, queries
from app.models.data.postgres_local import PostgresLocal
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
    dbms: str

router = APIRouter()


@router.post("/query")
async def send_query(request: QueryRequest):

    nlp_query = request.query
    model = request.model
    dbms = request.dbms

    print(f"NLP Query: {nlp_query}")
    print(f"Model : {model}")
    print(f"Database : {dbms}")

    sql_queries= generate_query(nlp_query, model, dbms)

    db_user = "postgres"
    db_password = "Amey1234"
    db_host = "localhost"
    db_name = "fastapi_db"
    db_port = '5432'

    my_db = PostgresLocal(db_host,db_user, db_password, db_name)

    my_db.connect()
    results = my_db.run_queries(sql_queries)

    return {"query" : sql_queries, "results" : results}


