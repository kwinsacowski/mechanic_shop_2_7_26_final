Mechanic Shop API

A RESTful API for managing customers, mechanics, service tickets, and inventory in a mechanic shop environment. This project demonstrates secure authentication using JWT, relational database design with SQLAlchemy, interactive API documentation using Swagger, and comprehensive automated testing using Python's built-in unittest framework.

-----

Live Deployment
    Render Deployment URL:
        https://mechanic-shop-2-7-26-final.onrender.com/
    Swagger Documentation
        https://mechanic-shop-2-7-26-final.onrender.com/api/docs/
    
    This deployment uses:
    - Render Web Service
    - Render PostgreSQL database
    - Gunicorn production server
    - HTTPS secure connectiion

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
        PostgreSQL (Render production)
        SQLite (local testing)

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

mechanic_shop_final/
│
├── flask_app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── .github/
│   └── workflows/
│       └── main.yaml
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   │
│   ├── utils/
│   │   └── auth.py
│   │
│   ├── static/
│   │   └── swagger.yaml
│   │
│   └── blueprints/
│       ├── customers/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       │
│       ├── mechanics/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       │
│       ├── inventory/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       │
│       └── service_tickets/
│           ├── __init__.py
│           ├── routes.py
│           └── schemas.py
│
└── tests/
    ├── __init__.py
    ├── test_customers.py
    ├── test_mechanics.py
    ├── test_inventory.py
    ├── test_service_tickets.py
    └── test_home.py


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
    https://github.com/kwinsacowski/mechanic_shop_2_7_26_final
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

Deployment (Render)

This API is deployed using Render with PostgreSQL and Gunicorn.

Deployment steps:

1. Create a Render PostgreSQL database
2. Create a Render Web Service connected to the GitHub repository
3. Set environment variables in Render:

    DATABASE_URL=<Render PostgreSQL External URL>
    SECRET_KEY=<secure random string>

4. Set Start Command in Render:

    gunicorn flask_app:app

5. Render automatically deploys on every push to main via GitHub Actions CI/CD pipeline.

-----

CI/CD Pipeline (GitHub Actions)

This project uses GitHub Actions for automated testing and deployment.

Pipeline workflow:

1. Runs unit tests automatically on every push
2. If tests pass, triggers automatic deployment to Render using Render API
3. Ensures only tested and validated code is deployed

Workflow file location:

.github/workflows/main.yaml

-----

Running the Application
    Start the Flask server:
        python flask_app.py
    Server runs at:
        http://127.0.0.1:5000
    Swagger documentation:
        Local:
            http://127.0.0.1:5000/api/docs
        Production:
            https://mechanic-shop-final.onrender.com/api/docs

-----

Security

Sensitive data is protected using:

- JWT authentication
- Environment variables for SECRET_KEY and DATABASE_URL
- HTTPS encryption via Render
- Password hashing using Werkzeug

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