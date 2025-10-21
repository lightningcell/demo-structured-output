from pydantic import BaseModel, Field
from typing import List, Dict, Any


class UserInput(BaseModel):
    """User input model for the fitness endpoint"""
    user_name: str = Field(..., description="User's name")
    user_goals: List[str] = Field(..., description="List of user goals")
    user_body_info: Dict[str, Any] = Field(..., description="User body information (e.g., {weight: 76.8, height: 180, ...})")
    user_input: str = Field(..., description="User's text input to validate and process")


class FitnessValidationResponse(BaseModel):
    """Response model for fitness validation"""
    is_fitness_related: bool = Field(..., description="Whether the input is fitness-related")
    score: float = Field(..., description="Confidence score (0-1) for fitness relevance")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    details: str = Field(default="", description="Additional error details")


class SuccessResponse(BaseModel):
    """Success response model"""
    response: str = Field(..., description="AI-generated response based on user data")
    fitness_score: float = Field(..., description="Fitness relevance score")
