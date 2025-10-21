# demo-structured-output

FastAPI application for validating fitness-related user inputs and generating personalized AI responses.

## Features

- **Fitness Input Validation**: Uses OpenAI's structured output to determine if user input is fitness-related
- **Personalized AI Responses**: Generates tailored fitness advice based on user information
- **Two-step Processing**: 
  1. Validates input relevance (fitness-related or not)
  2. Generates personalized response using user data

## Requirements

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/lightningcell/demo-structured-output.git
cd demo-structured-output
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Start the server

```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### POST /process-fitness-input

Processes user fitness input with validation.

**Request Body:**
```json
{
  "user_name": "John Doe",
  "user_goals": ["lose weight", "build muscle", "improve stamina"],
  "user_body_info": {
    "weight": 76.8,
    "height": 180,
    "age": 30
  },
  "user_input": "I want to start a workout routine"
}
```

**Success Response (200):**
```json
{
  "response": "Based on your goals and current metrics...",
  "fitness_score": 0.95
}
```

**Error Response (400):**
```json
{
  "detail": {
    "error": "Input is not fitness-related",
    "details": "The provided input does not appear to be related to fitness, health, or wellness. Confidence score: 0.25"
  }
}
```

### Example with curl

```bash
curl -X POST "http://localhost:8000/process-fitness-input" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John Doe",
    "user_goals": ["lose weight", "build muscle"],
    "user_body_info": {"weight": 76.8, "height": 180},
    "user_input": "What exercises should I do to lose weight?"
  }'
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
.
├── main.py           # FastAPI application with endpoints
├── models.py         # Pydantic models for request/response
├── requirements.txt  # Python dependencies
├── .env.example      # Example environment variables
└── README.md         # This file
```

## Implementation Details

### Step 1: Fitness Validation
Uses OpenAI's structured output feature to parse responses into a `FitnessValidationResponse` model with:
- `is_fitness_related`: Boolean indicating if input is fitness-related
- `score`: Confidence score (0-1) for the classification

### Step 2: Response Generation
If validation passes (score >= 0.5):
- User information (name, goals, body info) is included in the prompt
- OpenAI generates a personalized fitness response
- Response is returned to the client

If validation fails:
- HTTP 400 error with details about why the input was rejected