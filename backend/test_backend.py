import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app
from fastapi.testclient import TestClient

def test_backend():
    print("Testing backend endpoints...")
    
    client = TestClient(app)

    # Test the root endpoint
    response = client.get('/')
    print(f"Root endpoint response status: {response.status_code}")
    if response.status_code == 200:
        print(f"Root endpoint response data: {response.json()}")
    else:
        print(f"Root endpoint error: {response.text}")

    # Test the health check endpoint
    response = client.get('/health')
    print(f"Health endpoint response status: {response.status_code}")
    if response.status_code == 200:
        print(f"Health endpoint response data: {response.json()}")
    else:
        print(f"Health endpoint error: {response.text}")

    print("Backend testing completed!")

if __name__ == "__main__":
    test_backend()