from fastapi import APIRouter
from app.models.schemas import (
    DecisionEvaluationRequest,
    DecisionEvaluationResponse,
    TransitionRequest,
    TransitionResponse,
)
from app.services.decision_service import DecisionService
from app.core.config import settings

router = APIRouter()
service = DecisionService(settings)

@router.get("/v1/config")
def get_config():
    return settings.model_dump()

@router.post("/v1/decisions/evaluate", response_model=DecisionEvaluationResponse)
def evaluate_decision(payload: DecisionEvaluationRequest):
    return service.evaluate(payload)

@router.post("/v1/decisions/transition", response_model=TransitionResponse)
def transition_decision(payload: TransitionRequest):
    return service.transition(payload)
