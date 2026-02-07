Mechanic Shop API

A RESTful API for managing customers, mechanics, service tickets, and inventory in a mechanic shop environment. This project demonstrates secure authentication using JWT, relational database design with SQLAlchemy, interactive API documentation using Swagger, and comprehensive automated testing using Python's built-in unittest framework.

-----
Features
- Customer account creation and authentication
- JWT token authentication for protected routes
- Create, view, update, and delete customers, mechanics, inventory, and service tickets
- Assign mechanics and inventory items to service tickets
- Swagger UI documentation for all endpoints
- Automated unit tests for every API route, including negative test cases
- Relational database structure using SQLAlchemy ORM
- Secure password hashing using Werkzeug

-----

Technology Stack

    Backend
        Python 3
        Flask
        SQLAlchemy
        Marshmallow
        MySQL (or SQLite for testing)

    Authentication
        JWT (python-jose)
        Werkzeug password hashing

    Documentation
        Flask-Swagger
        Flask-Swagger-UI

    Testing
        unittest

-----

Project Structure

mechanic_shop/
│
├── app/
│   ├── blueprints/
│   │   ├── customers/
│   │   ├── mechanics/
│   │   ├── inventory/
│   │   └── service_tickets/
│   │
│   ├── static/
│   │   └── swagger.yaml
│   │
│   ├── utils/
│   │   └── util.py
│   │
│   ├── models.py
│   ├── extensions.py
│   └── __init__.py
│
├── tests/
│   ├── test_customers.py
│   ├── test_mechanics.py
│   ├── test_inventory.py
│   ├── test_service_tickets.py
│   └── test_home.py
│
├── run.py
├── requirements.txt
└── README.md

-----

Database Models
    Customer
        id (Primary Key)
        name
        email (Unique)
        phone_number
        password (hashed)

    Mechanic
        id
        name
        email (Unique)
        phone_number
        salary

    Inventory
        id
        name
        price

    ServiceTicket
        id
        vin
        service_date
        description
        customer_id
        pickup_date

    Relationships:
        Many-to-many between ServiceTicket and Mechanic
        Many-to-many between ServiceTicket and Inventory
        One-to-many between Customer and ServiceTicket

-----

Authentication
- JWT authentication is used to protect sensitive routes.
- Protected routes require the Authorization header:
    Authorization: Bearer <your_token_here>
- Token is obtained via:
    POST /customers/login

-----

API Documentation (Swagger)

Swagger UI provides interactive documentation.

Start the server, then open:
    http://127.0.0.1:5000/api/docs

Swagger includes:
- All endpoints
- Request body schemas
- Response schemas
- Authentication requirements
- Example inputs and outputs

-----

Installation Instructions
1. Clone the repository
    git clone https://github.com/kwinsacowski/mechanic_shop_2_7_26_part3
    cd mechanic_shop

2. Create virtual environment
    Windows:
        python -m venv venv
        venv\Scripts\activate

    Mac/Linux:
        python3 -m venv venv
        source venv/bin/activate

3. Install dependencies
    pip install -r requirements.txt

-----   

Running the Application
    Start the Flask server:
        python run.py
    Server runs at:
        http://127.0.0.1:5000
    Swagger documentation:
        http://127.0.0.1:5000/api/docs

-----

Running Tests

Run all unit tests:
    Windows / Mac / Linux:
        python -m unittest discover tests

Tests include:
- One test per endpoint
- Positive tests
- Negative tests
- Authentication tests
- Validation tests

-----

Testing Coverage
    Every route includes:
    - Success test
    - Failure test
    - Authentication test (where applicable)
    - Validation test

    Ensures production-level reliability.

-----

Author
Kayla Salmon

Mechanic Shop API Project
Built using Flask, SQLAlchemy, Swagger, and unittest