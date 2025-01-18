import pytest
from fastapi.testclient import TestClient
from backend_endpoints import app

client = TestClient(app)

def test_chat_endpoint():
    print("\n--- Testing /api/chat Endpoint ---")
    response = client.post("/api/chat", json={"user_message": "Add a phone bill of $50."})
    assert response.status_code == 200
    print(response.json())

def test_audio_to_text_endpoint():
    print("\n--- Testing /api/audio-to-text Endpoint ---")
    # Mock binary data for an audio file
    audio_data = b"fake_audio_data"
    response = client.post("/api/audio-to-text", data=audio_data)
    assert response.status_code == 200
    print(response.json())

def test_reset_endpoint():
    print("\n--- Testing /api/reset Endpoint ---")
    response = client.post("/api/reset")
    assert response.status_code == 200
    print(response.json())

def test_budget_summary_endpoint():
    print("\n--- Testing /api/budget-summary Endpoint ---")
    response = client.get("/api/budget-summary")
    assert response.status_code == 200
    print(response.json())

def test_check_purchase_endpoint():
    print("\n--- Testing /api/check-purchase Endpoint ---")
    response = client.post("/api/check-purchase", json={"amount": 100, "description": "New TV"})
    assert response.status_code == 200
    print(response.json())

if __name__ == "__main__":
    print("Running all tests...\n")
    
    # Run each test manually
    test_chat_endpoint()
    test_audio_to_text_endpoint()
    test_reset_endpoint()
    test_budget_summary_endpoint()
    test_check_purchase_endpoint()

    print("\nAll tests executed.")
