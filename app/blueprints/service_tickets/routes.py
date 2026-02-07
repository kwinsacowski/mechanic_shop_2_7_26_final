from flask import request
from datetime import datetime

from app.extensions import db
from app.models import ServiceTicket, Mechanic, Customer
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.service_tickets.schemas import (
    service_ticket_schema,
    service_tickets_schema
)


@service_tickets_bp.post("/")
def create_service_ticket():
    data = request.get_json() or {}

    # Basic required-field validation
    required = ["vin", "service_date", "description", "customer_id"]
    missing = [field for field in required if field not in data or data[field] in (None, "")]
    if missing:
        return {"error": f"Missing required field(s): {', '.join(missing)}"}, 400

    # Parse date safely
    try:
        service_date = datetime.strptime(data["service_date"], "%Y-%m-%d").date()
    except ValueError:
        return {"error": "service_date must be in YYYY-MM-DD format"}, 400

    # FK check: customer must exist (prevents MySQL IntegrityError 500)
    customer = Customer.query.get(data["customer_id"])
    if not customer:
        return {"error": f"Customer {data['customer_id']} not found"}, 404

    ticket = ServiceTicket(
        vin=data["vin"],
        service_date=service_date,
        description=data["description"],
        customer_id=data["customer_id"],
    )

    db.session.add(ticket)
    db.session.commit()

    return service_ticket_schema.dump(ticket), 201


@service_tickets_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    # Prevent duplicates
    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()

    return service_ticket_schema.dump(ticket), 200


@service_tickets_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    # Only remove if assigned
    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()

    return service_ticket_schema.dump(ticket), 200


@service_tickets_bp.get("/")
def get_service_tickets():
    tickets = ServiceTicket.query.all()
    return service_tickets_schema.dump(tickets), 200
