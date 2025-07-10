def test_create_order(client, test_token, admin_token):
    # First create a product
    product_response = client.post(
        "/products/",
        json={"name": "Test Product", "price": 9.99, "stock": 10},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    product_id = product_response.json()["id"]
    
    response = client.post(
        "/orders/",
        json={
            "products": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "price_at_time": 9.99
                }
            ]
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_amount"] == 19.98
    assert data["status"] == "pending"

def test_complete_order(client, test_token, admin_token):
    # Create product and order first
    product_response = client.post(
        "/products/",
        json={"name": "Test Product", "price": 9.99, "stock": 10},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    product_id = product_response.json()["id"]
    
    order_response = client.post(
        "/orders/",
        json={
            "products": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "price_at_time": 9.99
                }
            ]
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    order_id = order_response.json()["id"]
    
    response = client.put(
        f"/orders/{order_id}/complete",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None