def test_create_product(client, admin_token):
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "price": 9.99,
            "stock": 10
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 9.99
    assert data["stock"] == 10

def test_get_products(client, admin_token):
    # First create a product
    client.post(
        "/products/",
        json={"name": "Test Product", "price": 9.99, "stock": 10},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Test Product"

def test_update_product(client, admin_token):
    # First create a product
    create_response = client.post(
        "/products/",
        json={"name": "Test Product", "price": 9.99, "stock": 10},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    product_id = create_response.json()["id"]
    
    response = client.put(
        f"/products/{product_id}",
        json={"price": 19.99},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 19.99