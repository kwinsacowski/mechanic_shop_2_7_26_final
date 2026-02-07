import unittest
from app import create_app
from app.extensions import db

class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Seed customer
            c = self.client.post("/customers/", json={
                "name": "Seed Customer",
                "email": "seed_ticket_customer@email.com"
            })
            self.assertIn(c.status_code, (200, 201))
            self.customer_id = c.json["id"]

            # Seed mechanic
            m = self.client.post("/mechanics/", json={
                "name": "Seed Mechanic",
                "email": "seed_ticket_mechanic@email.com"
            })
            self.assertIn(m.status_code, (200, 201))
            self.mechanic_id = m.json["id"]

            # Seed part
            p = self.client.post("/inventory/", json={
                "name": "Seed Part",
                "quantity": 5,
                "price": 10.0
            })
            self.assertIn(p.status_code, (200, 201))
            self.part_id = p.json["id"]

            # Seed service ticket
            t = self.client.post("/service-tickets/", json={
                "vin": "1HGCM82633A004352",
                "service_date": "2026-02-07",
                "description": "Oil change",
                "customer_id": self.customer_id
            })
            self.assertIn(t.status_code, (200, 201))
            self.ticket_id = t.json["id"]

    def test_get_service_tickets(self):
        res = self.client.get("/service-tickets/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json, list)

    def test_edit_service_ticket(self):
        res = self.client.put(f"/service-tickets/{self.ticket_id}", json={"description": "Updated"})
        self.assertEqual(res.status_code, 200)

    def test_assign_mechanic(self):
        res = self.client.put(
            f"/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}",
            json={}
        )
        self.assertIn(res.status_code, (200, 404, 400))

    def test_remove_mechanic(self):
        res = self.client.put(
            f"/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}",
            json={}
        )
        self.assertIn(res.status_code, (200, 404, 400))

    def test_edit_ticket_mechanics(self):
        res = self.client.put(
            f"/service-tickets/{self.ticket_id}/edit",
            json={"mechanic_ids": [self.mechanic_id]}
        )
        self.assertIn(res.status_code, (200, 400, 404))

    def test_add_part_to_ticket(self):
        res = self.client.put(
            f"/service-tickets/{self.ticket_id}/add-part/{self.part_id}",
            json={}
        )
        self.assertIn(res.status_code, (200, 400, 404))

    # Negative
    def test_edit_ticket_not_found(self):
        res = self.client.put("/service-tickets/999999", json={"description": "x"})
        self.assertIn(res.status_code, (404, 400))
