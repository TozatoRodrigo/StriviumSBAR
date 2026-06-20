from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_roles_should_return_200() -> None:
    response = client.get("/tenant-user/v1/roles")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) > 0
    role = data[0]
    assert role["id"] is not None
    assert role["name"] is not None
    assert role["description"] is not None
