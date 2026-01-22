import pytest
from tests.conftest import test_client


def test_health_check(test_client):
    """Test the health check endpoint"""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_create_customer(test_client):
    """Test creating a new customer"""
    customer_data = {
        "name": "John Doe",
        "email": "john@example.com"
    }
    response = test_client.post("/customers/", json=customer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["email"] == customer_data["email"]
    assert "id" in data


def test_create_duplicate_customer(test_client):
    """Test creating a customer with duplicate email"""
    customer_data = {
        "name": "John Doe",
        "email": "john@example.com"
    }
    # Create first customer
    test_client.post("/customers/", json=customer_data)
    
    # Try to create duplicate
    response = test_client.post("/customers/", json=customer_data)
    assert response.status_code == 400


def test_get_customer(test_client):
    """Test retrieving a customer"""
    # Create customer
    customer_data = {
        "name": "Jane Doe",
        "email": "jane@example.com"
    }
    create_response = test_client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Get customer
    response = test_client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == customer_id
    assert data["email"] == customer_data["email"]


def test_get_customer_balance(test_client):
    """Test getting customer balance"""
    # Create customer
    customer_data = {
        "name": "Balance Test",
        "email": "balance@example.com"
    }
    create_response = test_client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Get balance
    response = test_client.get(f"/customers/{customer_id}/balance")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
    assert data["balance"] == 0


def test_list_customers(test_client):
    """Test listing customers"""
    # Create customers
    for i in range(3):
        test_client.post("/customers/", json={
            "name": f"Customer {i}",
            "email": f"customer{i}@example.com"
        })
    
    # List customers
    response = test_client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_create_transaction(test_client):
    """Test creating a transaction"""
    # Create customer
    customer_data = {
        "name": "Transaction Test",
        "email": "transaction@example.com"
    }
    create_response = test_client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Create transaction
    transaction_data = {
        "customer_id": customer_id,
        "amount": 100.0
    }
    response = test_client.post("/transactions/", json=transaction_data)
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 100.0
    assert data["customer_id"] == customer_id
    
    # Check cashback was applied (5% of 100 = 5)
    balance_response = test_client.get(f"/customers/{customer_id}/balance")
    balance_data = balance_response.json()
    assert balance_data["balance"] == 5.0


def test_cashback_transfer(test_client):
    """Test transferring cashback between customers"""
    # Create two customers
    customer1_data = {"name": "Customer 1", "email": "customer1@test.com"}
    customer2_data = {"name": "Customer 2", "email": "customer2@test.com"}
    
    customer1_id = test_client.post("/customers/", json=customer1_data).json()["id"]
    customer2_id = test_client.post("/customers/", json=customer2_data).json()["id"]
    
    # Give customer1 some cashback via transaction
    test_client.post("/transactions/", json={
        "customer_id": customer1_id,
        "amount": 100.0
    })
    
    # Transfer cashback
    transfer_data = {
        "from_customer_id": customer1_id,
        "to_customer_id": customer2_id,
        "amount": 2.0
    }
    response = test_client.post("/cashback-transfers/", json=transfer_data)
    assert response.status_code == 200
    
    # Check balances
    balance1 = test_client.get(f"/customers/{customer1_id}/balance").json()
    balance2 = test_client.get(f"/customers/{customer2_id}/balance").json()
    
    assert balance1["balance"] == 3.0  # 5 - 2
    assert balance2["balance"] == 2.0


def test_payout(test_client):
    """Test processing a payout"""
    # Create customer
    customer_data = {"name": "Payout Test", "email": "payout@example.com"}
    customer_id = test_client.post("/customers/", json=customer_data).json()["id"]
    
    # Give customer cashback
    test_client.post("/transactions/", json={
        "customer_id": customer_id,
        "amount": 200.0
    })
    
    # Process payout
    payout_data = {
        "customer_id": customer_id,
        "amount": 5.0
    }
    response = test_client.post("/payouts/", json=payout_data)
    assert response.status_code == 200
    
    # Check balance after payout
    balance = test_client.get(f"/customers/{customer_id}/balance").json()
    assert balance["balance"] == 5.0  # 10 - 5


def test_payout_insufficient_balance(test_client):
    """Test payout with insufficient balance"""
    # Create customer
    customer_data = {"name": "Insufficient Test", "email": "insufficient@example.com"}
    customer_id = test_client.post("/customers/", json=customer_data).json()["id"]
    
    # Try to payout without balance
    payout_data = {
        "customer_id": customer_id,
        "amount": 100.0
    }
    response = test_client.post("/payouts/", json=payout_data)
    assert response.status_code == 500  # Should fail


def test_create_ambassador(test_client):
    """Test creating an ambassador"""
    ambassador_data = {
        "name": "Ambassador Test",
        "email": "ambassador@example.com"
    }
    response = test_client.post("/ambassadors/", json=ambassador_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == ambassador_data["name"]
    assert data["email"] == ambassador_data["email"]


def test_create_group(test_client):
    """Test creating a group"""
    group_data = {"name": "Test Group"}
    response = test_client.post("/groups/", json=group_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == group_data["name"]


def test_create_qrcode(test_client):
    """Test creating a QR code"""
    # Create ambassador first
    ambassador_data = {"name": "QR Test", "email": "qr@example.com"}
    ambassador_id = test_client.post("/ambassadors/", json=ambassador_data).json()["id"]
    
    # Create QR code
    qrcode_data = {
        "code": "QR123456",
        "ambassador_id": ambassador_id
    }
    response = test_client.post("/qrcodes/", json=qrcode_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == qrcode_data["code"]


def test_create_gift_card(test_client):
    """Test creating a gift card"""
    gift_card_data = {
        "code": "GIFT123",
        "value": 50.0
    }
    response = test_client.post("/gift-cards/", json=gift_card_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == gift_card_data["code"]
    assert data["value"] == gift_card_data["value"]


def test_redeem_gift_card(test_client):
    """Test redeeming a gift card"""
    # Create customer
    customer_data = {"name": "Gift Test", "email": "gift@example.com"}
    customer_id = test_client.post("/customers/", json=customer_data).json()["id"]
    
    # Create gift card
    gift_card_data = {"code": "GIFT456", "value": 25.0}
    test_client.post("/gift-cards/", json=gift_card_data)
    
    # Redeem gift card
    response = test_client.delete(f"/gift-cards/GIFT456?customer_id={customer_id}")
    assert response.status_code == 200
    
    # Check balance
    balance = test_client.get(f"/customers/{customer_id}/balance").json()
    assert balance["balance"] == 25.0
