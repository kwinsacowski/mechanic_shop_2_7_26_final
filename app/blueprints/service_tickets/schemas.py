from marshmallow import fields
from app.extensions import ma
from app.models import ServiceTicket, Mechanic, Inventory


# --------- Mini Schemas (nested outputs) ---------

class MechanicMiniSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        fields = ("id", "name", "email", "phone_number", "salary")


class InventoryMiniSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        fields = ("id", "name", "price")


# --------- Main Service Ticket Schema ---------

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicMiniSchema, many=True)
    inventory = fields.Nested(InventoryMiniSchema, many=True)

    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True


# --------- Input Schemas (request validation) ---------

# For PUT /service-tickets/<ticket_id>/edit
class EditMechanicsSchema(ma.Schema):
    add_ids = fields.List(fields.Integer(), required=False, load_default=list)
    remove_ids = fields.List(fields.Integer(), required=False, load_default=list)


# For PUT /service-tickets/<ticket_id>
# Body: {"add_pickup_date": "YYYY-MM-DD"}
class PickupDateSchema(ma.Schema):
    add_pickup_date = fields.Date(required=True, allow_none=False)


# --------- Schema Instances ---------

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

edit_mechanics_schema = EditMechanicsSchema()
pickup_date_schema = PickupDateSchema()
