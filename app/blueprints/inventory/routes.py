from flask import request
from app.extensions import db
from app.models import Inventory
from app.blueprints.inventory import inventory_bp
from app.blueprints.inventory.schemas import inventory_schema, inventories_schema


@inventory_bp.post("/")
def create_part():
    data = request.get_json() or {}
    required = ["name", "price"]
    missing = [f for f in required if data.get(f) in (None, "")]
    if missing:
        return {"error": f"Missing field(s): {', '.join(missing)}"}, 400

    try:
        price = float(data["price"])
    except ValueError:
        return {"error": "price must be a number"}, 400

    part = Inventory(name=data["name"], price=price)
    db.session.add(part)
    db.session.commit()
    return inventory_schema.dump(part), 201


@inventory_bp.get("/")
def get_parts():
    parts = Inventory.query.all()
    return inventories_schema.dump(parts), 200


@inventory_bp.get("/<int:id>")
def get_part(id):
    part = Inventory.query.get_or_404(id)
    return inventory_schema.dump(part), 200


@inventory_bp.put("/<int:id>")
def update_part(id):
    part = Inventory.query.get_or_404(id)
    data = request.get_json() or {}

    if "name" in data:
        part.name = data["name"]
    if "price" in data:
        try:
            part.price = float(data["price"])
        except ValueError:
            return {"error": "price must be a number"}, 400

    db.session.commit()
    return inventory_schema.dump(part), 200


@inventory_bp.delete("/<int:id>")
def delete_part(id):
    part = Inventory.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()
    return {"message": f"Inventory part {id} deleted"}, 200
