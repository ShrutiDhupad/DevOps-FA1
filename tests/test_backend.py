import os
import sys
import pytest

# Ensure backend module can be imported regardless of execution working directory
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docker", "backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app import app, items_db

@pytest.fixture
def client():
    """Create a configured Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Verify GET / returns 200 and backend running message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert "Backend API is running" in data.get("message", "")
    assert "environment" in data

def test_hello_endpoint(client):
    """Verify GET /api/hello returns 200 and the FA1 greeting."""
    response = client.get("/api/hello")
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert "Hello from the DevOps Backend!" in data.get("message", "")

def test_health_endpoint(client):
    """Verify GET /health returns 200 and healthy status for k8s probes."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert data.get("status") == "healthy"
    assert data.get("service") == "backend"

def test_api_health_alias(client):
    """Verify GET /api/health also returns 200 for reverse proxy compatibility."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("status") == "healthy"

def test_get_items(client):
    """Verify GET /api/items returns item list and accurate count."""
    response = client.get("/api/items")
    assert response.status_code == 200
    data = response.get_json()
    assert "items" in data
    assert "count" in data
    assert isinstance(data["items"], list)
    assert data["count"] >= 2

def test_create_item_success(client):
    """Verify POST /api/items creates an item and returns 201 Created."""
    initial_count = len(items_db)
    payload = {
        "name": "Automated Pipeline Test Item",
        "description": "Created during pytest validation"
    }
    response = client.post("/api/items", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data is not None
    assert data.get("name") == "Automated Pipeline Test Item"
    assert data.get("description") == "Created during pytest validation"
    assert "id" in data
    assert len(items_db) == initial_count + 1

def test_create_item_missing_name_returns_400(client):
    """Verify input validation fails with 400 when 'name' is omitted."""
    payload = {
        "description": "Item without name should fail"
    }
    response = client.post("/api/items", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "name" in data["error"].lower()

def test_create_item_empty_name_returns_400(client):
    """Verify input validation fails with 400 when 'name' is blank."""
    payload = {
        "name": "   ",
        "description": "Item with only whitespace"
    }
    response = client.post("/api/items", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_create_item_non_json_returns_400(client):
    """Verify sending non-JSON payload returns 400 Bad Request."""
    response = client.post(
        "/api/items",
        data="plain text body",
        content_type="text/plain"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_metrics_endpoint_availability(client):
    """Verify GET /metrics returns Prometheus formatted exposition."""
    response = client.get("/metrics")
    assert response.status_code == 200
    content = response.get_data(as_text=True)
    assert "http_requests_total" in content
    assert "http_request_duration_seconds" in content
    assert "items_created_total" in content
    assert "app_info" in content

def test_metrics_records_request(client):
    """Verify that calling an endpoint updates http_requests_total."""
    # Call an endpoint
    client.get("/api/hello")
    # Fetch metrics
    response = client.get("/metrics")
    assert response.status_code == 200
    content = response.get_data(as_text=True)
    assert 'endpoint="hello"' in content or 'endpoint="api/hello"' in content or 'http_requests_total' in content

def test_not_found_endpoint(client):
    """Verify non-existent route returns 404 JSON."""
    response = client.get("/api/nonexistent-route-xyz")
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None
    assert "error" in data
