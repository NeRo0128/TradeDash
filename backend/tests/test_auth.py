def test_register(client):
    response = client.post("/auth/register", json={
        "username": "newuser",
        "password": "newpass123",
        "full_name": "New User"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert "hashed_password" not in data

def test_login(client, test_user):
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_invalid_login(client):
    response = client.post("/auth/login", data={
        "username": "wronguser",
        "password": "wrongpass"
    })
    assert response.status_code == 401