from flask import request
from app.extensions import db, limiter, cache
from app.models import Customer, ServiceTicket
from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, login_schema
from app.utils.util import encode_token, token_required
from app.blueprints.service_tickets.schemas import service_ticket_schema

@customers_bp.post("/login")
def login_customer():
    data = request.get_json() or {}

    # Validate input using schema
    errors = login_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    email = data.get("email")
    password = data.get("password")

    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        return {"message": "Invalid credentials"}, 401

    token = encode_token(customer.id)
    return {"token": token}, 200

@customers_bp.get("/my-tickets")
@token_required
def get_my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return service_tickets_schema.dump(tickets), 200

@customers_bp.post("/")
@limiter.limit("5 per minute") # Limit to 5 customer creations per minute, considering multple users servicing multiple customers at one time
def create_customer():
    data = request.get_json() or {}
    customer = Customer(
        name=data.get("name"),
        email=data.get("email"),
        phone_number=data.get("phone_number"),
    )
    db.session.add(customer)
    db.session.commit()
    return customer_schema.dump(customer), 201

@customers_bp.get("/")
@limiter.limit("10 per minute") # Limit to 10 customer retrievals per minute, as this endpoint may be called frequently by users to view the customer list, especially if they are managing multiple customers
@cache.cached(timeout=120) # Cache the list of customers for 2 minutes to reduce database load, especially if the customer list is large and doesn't change frequently
def get_customers():
    customers = Customer.query.all()
    return customers_schema.dump(customers), 200

@customers_bp.get("/<int:id>")
@cache.cached(timeout=120) # Cache individual customer details for 2 minutes, as users may frequently view the same customer's details while managing their account, and this can help reduce database load for popular customers
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.dump(customer), 200

@customers_bp.put("/<int:id>")
@token_required
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json() or {}

    customer.name = data.get("name", customer.name)
    customer.email = data.get("email", customer.email)
    customer.phone_number = data.get("phone_number", customer.phone_number)

    db.session.commit()
    return customer_schema.dump(customer), 200

@customers_bp.delete("/<int:id>")
@token_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return {"message": f"Customer {id} deleted"}, 200
