from app.extensions import ma
from app.models import ServiceTicket, Mechanic

class MechanicMiniSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        fields = ("id", "name", "email", "phone_number", "salary")

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):

    mechanics = ma.Nested(MechanicMiniSchema, many=True)

    class Meta:
        model = ServiceTicket
        load_instance = True

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
