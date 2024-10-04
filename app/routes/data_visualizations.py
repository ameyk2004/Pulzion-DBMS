from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.data_visualization import execute_code_from_string, generate_data_visualization

router = APIRouter()

class QueryRequest(BaseModel):
    results : list
    model: Optional[str] = "gemini"

@router.post("/data-visualization")
async def send_query(request: QueryRequest):

    results = request.results
    model = request.model

    if not model:
        model = "gemini"

    print("\n\n\n Results Recieved",results)
    response = generate_data_visualization(results, model)

    print("\n\n\n Response Genexrated\n\n", response)

    data = response["response"]

    count = 1

    image_urls = []

    for res in data:
        print(f"\n\n\n Res {count} GENERATIION")
        print("\n IMAGE URLS \n\n",image_urls)
        url = execute_code_from_string(res["Code"], res["data"], count)
        if url != "":
            image_urls.append(url)
        count +=1

    response["image_urls"] = image_urls


    return response


