#  Order Management API

A FastAPI-based REST API for managing e-commerce orders with user authentication and email notifications.

## Project Description

This project implements a secure and scalable order management system with the following features:
- User registration and authentication using JWT tokens
- Order creation and management
- Email notifications for order status updates
- SQLite database for data persistence
- Docker containerization for easy deployment

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Docker and Docker Compose (for containerized deployment)

### Local Development Setup

0.create your own .env file in the app directory with the following parameters
SECRET_KEY=Your secret key
MAIL_USERNAME=Your mail@gmail.com
MAIL_PASSWORD=Your gmail app password
MAIL_FROM=Your mail@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

1. Clone the repository:
```bash
git clone <repository-url>
cd app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
4.import  the local files as from app.filename import filenames

5. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Running with Docker

0.create your own .env file in the app directory with the following parameters
SECRET_KEY=Your secret key
MAIL_USERNAME=Your mail@gmail.com
MAIL_PASSWORD=Your gmail app password
MAIL_FROM=Your mail@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

1. Build and start the containers:
```bash
docker-compose up --build
```

2. The application will be available at `http://localhost:8000` for docs `http://localhost:8000/docs`

## API Endpoints

### Authentication

#### Register User
- **POST** `/users/register`
- **Request Body:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword"
}
```

#### Login
- **POST** `/login`
- **Form Data:**
  - username: email
  - password: password
- **Response:** JWT access token

### Orders

#### Get All Orders
- **GET** `/orders/`
- **Headers:** Authorization: Bearer {token}
- **Response:** List of orders for the authenticated user

#### Create Order
- **POST** `/orders/`
- **Headers:** Authorization: Bearer {token}
- **Request Body:**
```json
{
    "product": "Product Name",
    "quantity": 2,
    "address": "Delivery Address"
}
```

#### Update Order Status
- **PATCH** `/orders/{order_id}/status`
- **Headers:** Authorization: Bearer {token}
- **Request Body:**
```json
{
    "status": "completed"
}
```

## Design Decisions and Assumptions

1. **Authentication:**
   - JWT-based authentication for secure API access
   - Password hashing using bcrypt for security
   - Token-based session management

2. **Database:**
   - SQLite database for simplicity and ease of deployment
   - SQLModel for type-safe database operations
   - Automatic database table creation on startup

3. **Email Notifications:**
   - Email notifications sent for order creation and status updates
   - Asynchronous email sending to prevent blocking API responses

4. **Security:**
   - Password hashing for user credentials
   - JWT token expiration for session management
   - Input validation using Pydantic models

5. **API Design:**
   - RESTful API design principles
   - Clear separation of concerns with modular routing
   - Comprehensive error handling and status codes

## Testing

The project includes a test suite using pytest. To run tests:

```bash
pytest
```

## Environment Variables

The following environment variables can be configured:
- `DATABASE_URL`: Database connection string (default: sqlite:///./app.db)
- `PYTHONPATH`: Python path for module resolution (default: /app) 
