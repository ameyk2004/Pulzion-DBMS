from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import connection_uri, queries
from app.services.metadata_service import generate_metadata
from app.config import connection_uri, queries
from app.services.metadata_service import generate_metadata
import requests

import json

API_KEY = 'sk-96f006f61ebd416ea5b99c9ecaece174'  # Replace with your actual API key
WORQHAT_URL = 'https://api.worqhat.com/api/ai/content/v3' 

# Define a Pydantic model for the request body
class QueryRequest(BaseModel):
    query: str  # This defines the required field 'query'

router = APIRouter()


def parse_and_return_json(input_string):
    clean_input = input_string.strip().replace("\\n", "")
    
    json_data = json.loads(clean_input)

    return json.dumps(json_data, indent=2)

@router.post("/query")
async def send_query(request: QueryRequest):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    nlp_query = request.query
    print(f"NLP Query: {nlp_query}")

    try:
        meta_data = generate_metadata(queries, connection_uri)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metadata: {str(e)}")

    data = {
        "question": f"""
        Prompt:
        I have provided a JSON structure containing metadata about a database, including tables, views, and procedures. 
        Please analyze the data step by step and return a new JSON structure with the following requirements:

        1. Database Description:
        - Provide a brief description of the overall database, including its purpose and primary functions.

        2. Table Descriptions:
        For each table, generate:
        - A description summarizing the table's purpose.
        - For each column in the table, provide:
            - A description of its role and significance.
        - Analyze relationships with other tables:
            - Provide descriptions of these relationships, including the cardinality (e.g., one-to-many, many-to-one).

        3. View Descriptions:
        For each view, provide:
        - A description of what the view represents.
        - Explain how it relates to the underlying tables and any relevant filters or calculations.

        4. Output Structure:
        - Organize the resulting descriptions clearly within a new JSON format, maintaining clarity and conciseness for each description.

        Processing Steps:
        Please follow these processing steps while analyzing the JSON data:

        1. Overall Database Analysis:
        - Begin with a high-level overview of the database.

        2. Independent Tables:
        - Identify and analyze all independent tables first.
        - For each independent table, repeat the description process as outlined.

        3. Dependent Tables:
        - Identify dependent tables that relate to the independent ones.
        - Repeat the description process for each dependent table accordingly.

        4. Views Analysis:
        - For each view, generate a description based on its definition and context within the database.

        5. Final Output:
        - Ensure the final output is in a well-structured JSON format with clear and concise descriptions.

        Here is the JSON data:
        {meta_data}
        """
    }

    try:
        response = requests.post(WORQHAT_URL, json=data, headers=headers)
        response.raise_for_status() 



        return json.dumps(response.json())

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
