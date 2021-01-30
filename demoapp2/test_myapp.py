from fastapi.testclient import TestClient

from .myapp import app

test_client = TestClient(app)


# Test /
def test_get_root():
    response = test_client.get(url="/?token=jessica", headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello demo app from zigiiprens!"}


# Test /admin/
def test_get_admin():
    response = test_client.post(url="/admin/?token=jessica", headers={"Content-Type": "application/json",
                                                                      "x-token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == {"message": "Admin getting zigiiprens"}
