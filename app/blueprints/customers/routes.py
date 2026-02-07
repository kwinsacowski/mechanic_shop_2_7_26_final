from flask import request
from app.extensions import db
from app.models import Customer
from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema

@customers_bp.post("/")
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
def get_customers():
    customers = Customer.query.all()
    return customers_schema.dump(customers), 200

@customers_bp.get("/<int:id>")
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.dump(customer), 200

@customers_bp.put("/<int:id>")
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json() or {}

    customer.name = data.get("name", customer.name)
    customer.email = data.get("email", customer.email)
    customer.phone_number = data.get("phone_number", customer.phone_number)

    db.session.commit()
    return customer_schema.dump(customer), 200

@customers_bp.delete("/<int:id>")
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return {"message": f"Customer {id} deleted"}, 200
