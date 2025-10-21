import os
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from dotenv import load_dotenv
from models import (
    UserInput,
    FitnessValidationResponse,
    ErrorResponse,
    SuccessResponse
)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Fitness AI API",
    description="API for validating fitness-related inputs and generating personalized responses",
    version="1.0.0"
)

# Initialize OpenAI client (lazy initialization to allow testing without API key)
client = None


def get_openai_client():
    """Get or initialize the OpenAI client"""
    global client
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key is not configured. Please set OPENAI_API_KEY environment variable."
            )
        client = OpenAI(api_key=api_key)
    return client


def validate_fitness_input(user_input: str) -> FitnessValidationResponse:
    """
    Step 1: Validate if the user input is fitness-related using OpenAI structured output.
    
    Args:
        user_input: The user's text input to validate
        
    Returns:
        FitnessValidationResponse with is_fitness_related boolean and confidence score
    """
    try:
        client = get_openai_client()
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": """You are a fitness expert validator. Analyze the user input and determine if it's related to fitness, health, exercise, nutrition, or wellness.
                    
Return a boolean indicating if it's fitness-related and a confidence score between 0 and 1.
- Score 0.0-0.3: Definitely not fitness-related
- Score 0.3-0.6: Somewhat related or ambiguous
- Score 0.6-1.0: Clearly fitness-related"""
                },
                {
                    "role": "user",
                    "content": f"Is this input fitness-related? Input: '{user_input}'"
                }
            ],
            response_format=FitnessValidationResponse,
        )
        
        return completion.choices[0].message.parsed
    except Exception as e:
        # Default to considering it not fitness-related if there's an error
        return FitnessValidationResponse(is_fitness_related=False, score=0.0)


def generate_ai_response(user_name: str, user_goals: list, user_body_info: dict, user_input: str) -> str:
    """
    Step 2: Generate AI response using user information.
    
    Args:
        user_name: User's name
        user_goals: List of user goals
        user_body_info: Dictionary of user body information
        user_input: The validated user input
        
    Returns:
        AI-generated response string
    """
    # Construct the prompt with user information
    user_context = f"""
User Information:
- Name: {user_name}
- Goals: {', '.join(user_goals)}
- Body Info: {', '.join([f'{k}: {v}' for k, v in user_body_info.items()])}

User Input: {user_input}
"""
    
    try:
        client = get_openai_client()
        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": """You are a professional fitness and wellness coach. Provide personalized advice based on the user's information, goals, and current body metrics. Be encouraging, specific, and actionable in your recommendations."""
                },
                {
                    "role": "user",
                    "content": user_context
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating AI response: {str(e)}")


@app.post("/process-fitness-input", response_model=SuccessResponse)
async def process_fitness_input(user_data: UserInput):
    """
    Main endpoint that processes user fitness input.
    
    Flow:
    1. Validate if the input is fitness-related
    2. If not fitness-related, return error
    3. If fitness-related, generate personalized AI response using user data
    
    Args:
        user_data: UserInput model containing user name, goals, body info, and input
        
    Returns:
        SuccessResponse with AI-generated response and fitness score
        
    Raises:
        HTTPException: If input is not fitness-related or other errors occur
    """
    # Step 1: Validate fitness input
    validation_result = validate_fitness_input(user_data.user_input)
    
    # Step 2: Check validation result
    if not validation_result.is_fitness_related or validation_result.score < 0.5:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Input is not fitness-related",
                "details": f"The provided input does not appear to be related to fitness, health, or wellness. Confidence score: {validation_result.score:.2f}"
            }
        )
    
    # Step 3: Generate AI response with user information
    ai_response = generate_ai_response(
        user_name=user_data.user_name,
        user_goals=user_data.user_goals,
        user_body_info=user_data.user_body_info,
        user_input=user_data.user_input
    )
    
    return SuccessResponse(
        response=ai_response,
        fitness_score=validation_result.score
    )


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Fitness AI API",
        "version": "1.0.0",
        "endpoints": {
            "POST /process-fitness-input": "Process and validate fitness-related user input"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
