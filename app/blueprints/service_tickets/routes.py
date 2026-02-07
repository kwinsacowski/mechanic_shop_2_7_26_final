from flask import request
from datetime import datetime
from app.extensions import db
from app.models import ServiceTicket, Mechanic, Customer, service_mechanics
from app.blueprints.service_tickets import service_tickets_bp
from app.models import Inventory
from app.blueprints.service_tickets.schemas import (
    service_ticket_schema,
    service_tickets_schema,
    pickup_date_schema,
    edit_mechanics_schema
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
        pickup_date=None
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

@service_tickets_bp.put("/<int:ticket_id>")
def edit_service_ticket(ticket_id):
    data = request.get_json() or {}

    errors = pickup_date_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    ticket = ServiceTicket.query.get_or_404(ticket_id)
    ticket.pickup_date = data["add_pickup_date"]

    db.session.commit()
    return service_ticket_schema.dump(ticket), 200
    
@service_tickets_bp.put("/<int:ticket_id>/edit")
def edit_ticket_mechanics(ticket_id: int):
    """
    Body JSON:
    {
      "add_ids": [1,2,3],
      "remove_ids": [4,5]
    }
    """
    ticket = ServiceTicket.query.get_or_404(ticket_id)

    data = request.get_json() or {}
    errors = edit_mechanics_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    add_ids = data.get("add_ids", []) or []
    remove_ids = data.get("remove_ids", []) or []

    # de-dupe (remove same id in both lists)
    add_set = set(add_ids)
    remove_set = set(remove_ids)
    conflict = add_set.intersection(remove_set)
    if conflict:
        return {"error": f"IDs cannot be in both add_ids and remove_ids: {sorted(conflict)}"}, 400

    # Lookup mechanics once
    all_ids = list(add_set.union(remove_set))
    mechanics_by_id = {}
    if all_ids:
        mechanics = Mechanic.query.filter(Mechanic.id.in_(all_ids)).all()
        mechanics_by_id = {m.id: m for m in mechanics}

    missing = [mid for mid in all_ids if mid not in mechanics_by_id]
    if missing:
        return {"error": f"Mechanic(s) not found: {missing}"}, 404

    # Remove first
    for mid in remove_set:
        mech = mechanics_by_id[mid]
        if mech in ticket.mechanics:
            ticket.mechanics.remove(mech)

    # Add (avoid duplicates)
    for mid in add_set:
        mech = mechanics_by_id[mid]
        if mech not in ticket.mechanics:
            ticket.mechanics.append(mech)

    db.session.commit()
    return service_ticket_schema.dump(ticket), 200

@service_tickets_bp.put("/<int:ticket_id>/add-part/<int:inventory_id>")
def add_part_to_ticket(ticket_id, inventory_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    part = Inventory.query.get_or_404(inventory_id)

    if part not in ticket.inventory:
        ticket.inventory.append(part)
        db.session.commit()

    return service_ticket_schema.dump(ticket), 200
