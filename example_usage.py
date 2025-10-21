"""
Example usage of the Fitness AI API

This file demonstrates how to interact with the API endpoints.
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"


def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_process_fitness_input_success():
    """Test the main endpoint with a fitness-related input"""
    print("Testing process-fitness-input with fitness-related input...")
    
    payload = {
        "user_name": "John Doe",
        "user_goals": ["lose weight", "build muscle", "improve stamina"],
        "user_body_info": {
            "weight": 76.8,
            "height": 180,
            "age": 30,
            "gender": "male"
        },
        "user_input": "I want to start a workout routine to lose weight and build muscle"
    }
    
    response = requests.post(
        f"{BASE_URL}/process-fitness-input",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_process_fitness_input_failure():
    """Test the main endpoint with a non-fitness-related input"""
    print("Testing process-fitness-input with non-fitness-related input...")
    
    payload = {
        "user_name": "Jane Smith",
        "user_goals": ["learn programming", "read more books"],
        "user_body_info": {
            "weight": 65.0,
            "height": 170
        },
        "user_input": "What's the weather like today?"
    }
    
    response = requests.post(
        f"{BASE_URL}/process-fitness-input",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def main():
    """Run all example tests"""
    print("=" * 70)
    print("Fitness AI API - Example Usage")
    print("=" * 70 + "\n")
    
    try:
        test_root_endpoint()
        test_health_endpoint()
        test_process_fitness_input_success()
        test_process_fitness_input_failure()
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API.")
        print("Make sure the server is running with: python main.py")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1
    
    print("=" * 70)
    print("Examples completed!")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
