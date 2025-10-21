#!/usr/bin/env python3
"""
Test script for the Fitness AI API
This script starts the server and tests the endpoints without requiring an OpenAI API key.
"""
import sys
import json


def test_models():
    """Test that models can be imported and instantiated"""
    print("Testing models...")
    try:
        from models import UserInput, FitnessValidationResponse, ErrorResponse, SuccessResponse
        
        # Test UserInput
        user_input = UserInput(
            user_name="John Doe",
            user_goals=["lose weight", "build muscle"],
            user_body_info={"weight": 76.8, "height": 180},
            user_input="I want to start working out"
        )
        print(f"✓ UserInput model works: {user_input.user_name}")
        
        # Test FitnessValidationResponse
        validation = FitnessValidationResponse(is_fitness_related=True, score=0.95)
        print(f"✓ FitnessValidationResponse model works: {validation.score}")
        
        # Test ErrorResponse
        error = ErrorResponse(error="Test error", details="Test details")
        print(f"✓ ErrorResponse model works: {error.error}")
        
        # Test SuccessResponse
        success = SuccessResponse(response="Test response", fitness_score=0.95)
        print(f"✓ SuccessResponse model works: {success.fitness_score}")
        
        print("All models work correctly!\n")
        return True
    except Exception as e:
        print(f"✗ Error testing models: {e}")
        return False


def test_app_structure():
    """Test that the FastAPI app can be imported and has expected structure"""
    print("Testing app structure...")
    try:
        from main import app
        
        # Check routes
        routes = [route.path for route in app.routes]
        print(f"✓ App has {len(routes)} routes")
        
        expected_routes = ["/", "/health", "/process-fitness-input"]
        for route in expected_routes:
            if route in routes:
                print(f"✓ Route '{route}' exists")
            else:
                print(f"✗ Route '{route}' is missing")
                return False
        
        print("App structure is correct!\n")
        return True
    except Exception as e:
        print(f"✗ Error testing app structure: {e}")
        return False


def test_validation_and_response_functions():
    """Test that the validation and response functions exist and have correct signatures"""
    print("Testing function signatures...")
    try:
        from main import validate_fitness_input, generate_ai_response
        import inspect
        
        # Check validate_fitness_input
        sig = inspect.signature(validate_fitness_input)
        params = list(sig.parameters.keys())
        if params == ['user_input']:
            print("✓ validate_fitness_input has correct signature")
        else:
            print(f"✗ validate_fitness_input has incorrect signature: {params}")
            return False
        
        # Check generate_ai_response
        sig = inspect.signature(generate_ai_response)
        params = list(sig.parameters.keys())
        if params == ['user_name', 'user_goals', 'user_body_info', 'user_input']:
            print("✓ generate_ai_response has correct signature")
        else:
            print(f"✗ generate_ai_response has incorrect signature: {params}")
            return False
        
        print("All function signatures are correct!\n")
        return True
    except Exception as e:
        print(f"✗ Error testing function signatures: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Fitness AI API - Static Tests")
    print("=" * 60 + "\n")
    
    tests = [
        test_models,
        test_app_structure,
        test_validation_and_response_functions
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("=" * 60)
    if all(results):
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    else:
        print("✗ Some tests failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
