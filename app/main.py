from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

# Create the FastAPI app instance
app = FastAPI(
    title="Scalable AutoGen Agent API",
    description="A structured API to interact with an AutoGen agent.",
    version="1.0.0",
)

# --- Add CORS Middleware ---
# This will allow your browser-based chat UI to communicate with the API.
origins = [
    "http://localhost",
    "http://localhost:8000",
    "null", # Allow requests from local files (e.g., file://)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"], # Allow all headers
)

# Include the API router
# All routes from api/routes.py will be prefixed with /api/v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    """
    Root endpoint for basic health checks.
    """
    return {"message": "Welcome to the Scalable AutoGen Agent API!"}
