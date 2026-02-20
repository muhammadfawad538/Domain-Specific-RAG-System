"""
Test script for Domain-Specific RAG System endpoints without API keys.

This script demonstrates how to test the system using the mock LLM service
that was implemented for testing without OpenAI or Anthropic API keys.
"""

import requests
import json
import time
import os
from threading import Thread
import subprocess
import sys

def start_api_server():
    """Start the API server in a separate process"""
    print("Starting API server...")
    # Create a simple .env file for testing if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("# Test environment file - no API keys for mock service\n")

    # Start the server using uvicorn
    server_cmd = [sys.executable, "-c",
                 "from uvicorn import run; from src.api.main import app; run(app, host='0.0.0.0', port=8000, log_level='info')"]

    process = subprocess.Popen(server_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Give the server a moment to start
    time.sleep(3)

    return process

def test_endpoints():
    """Test the API endpoints"""
    base_url = "http://localhost:8000/api"

    print("\n" + "="*50)
    print("TESTING DOMAIN-SPECIFIC RAG SYSTEM ENDPOINTS")
    print("="*50)

    # Test 1: Health Check
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   Overall Status: {health_data.get('status', 'unknown')}")
            components = health_data.get('components', {})
            print(f"   LLM Service: {components.get('llm_service', 'unknown')}")
            print(f"   Vector DB: {components.get('vector_db', 'unknown')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {str(e)}")

    # Test 2: Query Processing (Medical)
    print("\n2. Testing Medical Query Endpoint...")
    medical_query = {
        "content": "What are the current medical guidelines for treating hypertension?",
        "user_id": "test_user_123",
        "domain": "UNKNOWN"
    }

    try:
        response = requests.post(f"{base_url}/query", json=medical_query, timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Query Status: {result.get('status', 'unknown')}")
            print(f"   Response Preview: {result.get('content', '')[0:100]}...")
            print(f"   Citations: {len(result.get('citations', []))}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {str(e)}")

    # Test 3: Query Processing (Legal)
    print("\n3. Testing Legal Query Endpoint...")
    legal_query = {
        "content": "What is the statute of limitations for medical malpractice in New York?",
        "user_id": "test_user_123",
        "domain": "UNKNOWN"
    }

    try:
        response = requests.post(f"{base_url}/query", json=legal_query, timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Query Status: {result.get('status', 'unknown')}")
            print(f"   Response Preview: {result.get('content', '')[0:100]}...")
            print(f"   Citations: {len(result.get('citations', []))}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {str(e)}")

    # Test 4: Query with Insufficient Evidence
    print("\n4. Testing Insufficient Evidence Query...")
    impossible_query = {
        "content": "What is the meaning of life according to extraterrestrial sources?",
        "user_id": "test_user_123",
        "domain": "UNKNOWN"
    }

    try:
        response = requests.post(f"{base_url}/query", json=impossible_query, timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Query Status: {result.get('status', 'unknown')}")
            print(f"   Response: {result.get('content', '')[0:150]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {str(e)}")

    # Test 5: Liveness Check
    print("\n5. Testing Liveness Endpoint...")
    try:
        response = requests.get(f"{base_url}/live", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Liveness: {response.json()}")
    except Exception as e:
        print(f"   Error: {str(e)}")

    # Test 6: Readiness Check
    print("\n6. Testing Readiness Endpoint...")
    try:
        response = requests.get(f"{base_url}/ready", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Readiness: {response.json()}")
    except Exception as e:
        print(f"   Error: {str(e)}")

def test_with_curl_commands():
    """Print out curl commands that can be used to test the endpoints"""
    print("\n" + "="*50)
    print("CURL COMMANDS FOR MANUAL TESTING")
    print("="*50)

    print("\nHealth Check:")
    print("curl -X GET \"http://localhost:8000/api/health\"")

    print("\nMedical Query:")
    print("curl -X POST \"http://localhost:8000/api/query\" \\")
    print("  -H \"Content-Type: application/json\" \\")
    print("  -d '{")
    print("    \"content\": \"What are the current medical guidelines for treating hypertension?\",")
    print("    \"user_id\": \"test_user_123\",")
    print("    \"domain\": \"UNKNOWN\"")
    print("  }'")

    print("\nLegal Query:")
    print("curl -X POST \"http://localhost:8000/api/query\" \\")
    print("  -H \"Content-Type: application/json\" \\")
    print("  -d '{")
    print("    \"content\": \"What is the statute of limitations for medical malpractice in New York?\",")
    print("    \"user_id\": \"test_user_123\",")
    print("    \"domain\": \"UNKNOWN\"")
    print("  }'")

    print("\nAPI Documentation:")
    print("Swagger UI: http://localhost:8000/docs")
    print("ReDoc:       http://localhost:8000/redoc")

def main():
    """Main function to run the tests"""
    print("Domain-Specific RAG System - Endpoint Testing")
    print("Using Mock LLM Service (no API keys required)")

    # Start the API server
    server_process = start_api_server()

    try:
        # Wait a moment for the server to be ready
        time.sleep(3)

        # Test the endpoints
        test_endpoints()

        # Show curl commands for manual testing
        test_with_curl_commands()

        print(f"\n{'='*50}")
        print("TESTING COMPLETE")
        print("Note: Server is still running. Press Ctrl+C to stop.")
        print("You can continue testing with curl or API tools.")
        print(f"{'='*50}")

    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        # Terminate the server process
        server_process.terminate()
        server_process.wait()
        print("Server stopped.")

if __name__ == "__main__":
    main()