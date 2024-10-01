from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.data_visualization import execute_code_from_string, generate_data_visualization

router = APIRouter()

class QueryRequest(BaseModel):
    results : list

@router.post("/data-visualization")
async def send_query(request: QueryRequest):

    results = request.results
    response = generate_data_visualization(results)
    print(response["response"]["Code"])
    execute_code_from_string(response["response"]["Code"])
    return response


