import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from ..main import app
from ..database import get_session
from ..models import User, Order
from ..hashing import Hash

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    # Create user with properly hashed password
    plain_password = "testpass123"
    user = User(
        username="testuser",
        email="test@example.com",
        password=Hash.bcrypt(plain_password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user, plain_password

def test_create_order(client: TestClient, test_user: tuple[User, str]):
    user, plain_password = test_user
    # Login with plain password
    login_response = client.post(
        "/login",
        data={
            "username": user.email,
            "password": plain_password
        }
    )
    token = login_response.json()["access_token"]

def test_update_order_status(client: TestClient, test_user: tuple[User, str], session: Session):
    user, plain_password = test_user
    # Login with plain password
    login_response = client.post(
        "/login",
        data={
            "username": user.email,
            "password": plain_password
        }
    )

def test_get_orders(client: TestClient, test_user: tuple[User, str], session: Session):
    user, plain_password = test_user
    
    # First login to get the token
    login_response = client.post(
        "/login",
        data={
            "username": user.email,
            "password": plain_password
        }
    )
    token = login_response.json()["access_token"]
    
    # Create a test order
    order = Order(
        product="Test Product",
        quantity=2,
        address="Test Address",
        buyer_id=user.user_id,
        status="pending"
    )
    session.add(order)
    session.commit()
    
    # Get all orders
    response = client.get(
        "/orders/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    orders = response.json()
    assert len(orders) == 1
    assert orders[0]["product"] == "Test Product"
    assert orders[0]["quantity"] == 2
    assert orders[0]["address"] == "Test Address"
    assert orders[0]["status"] == "pending"
    assert orders[0]["buyer_id"] == user.user_id 