from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.main_agent_service import solve_task_with_agent
from .security import AuthChecker # Import the new AuthChecker

# Create a new router
router = APIRouter()

# Define request and response models
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

# Here, we initialize the AuthChecker with the roles required for this specific endpoint.
# This creates a dependency that will check if the user has the 'admin' role.
# You can change this to ["admin", "editor"] to allow either role.
auth_checker_dependency = AuthChecker()

# Apply the role checker dependency to the endpoint
@router.post("/ask",
    response_model=AnswerResponse
)
async def ask_question(request: QuestionRequest, auth_result: dict = Depends(auth_checker_dependency)):
    """
    Receives a question and uses the agent service to find the answer.
    This endpoint is protected and requires the 'admin' role.
    """
    try:
        # Extract the JWT token from the auth result
        jwt_token = auth_result["token"]
        # Call the service function to handle the core logic with JWT
        result = solve_task_with_agent(request.question, jwt_token)
        return AnswerResponse(answer=result)
    except Exception as e:
        # Handle potential errors from the service
        raise HTTPException(status_code=500, detail=str(e))
