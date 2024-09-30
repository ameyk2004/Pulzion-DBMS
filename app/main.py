from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.metadata import router as metadata_router

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware configuration (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for metadata and query handling
app.include_router(metadata_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the NLP to SQL API!"}

# Include any other routes or middlewares here as needed
