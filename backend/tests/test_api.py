from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_insights():
    response = client.post(
        "/api/insights",
        json={"search_term": "test", "num_results": 2}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    # Check structure of each insight
    for insight in data:
        assert "insight" in insight
        assert "source_title" in insight
        assert "source_link" in insight

def test_invalid_search_term():
    response = client.post(
        "/api/insights",
        json={"search_term": "", "num_results": 2}
    )
    assert response.status_code == 200
    assert response.json() == [] 