from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_products_router_list():
    response = client.get("/api/products")
    assert response.status_code == 200
