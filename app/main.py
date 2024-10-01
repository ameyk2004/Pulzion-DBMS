from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.metadata import router as metadata_router
from app.routes.query import router as query_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(metadata_router, prefix="/api")
app.include_router(query_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the NLP to SQL API!"}

# Include any other routes or middlewares here as needed
