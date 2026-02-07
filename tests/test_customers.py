import unittest
from app import create_app
from app.extensions import db

class TestCustomers(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            #seed for testing
            res = self.client.post("/customers/", json={
                "name": "Seed Customer",
                "email": "seed_customer@email.com",
                "phone_number": "555-123-4567",
                "password": "password123"
            })
            self.assertIn(res.status_code, (200, 201))
            self.customer_id = res.json.get("id")

    def test_create_customer(self):
        res = self.client.post("/customers/", json={
            "name": "Jane",
            "email": "jane@email.com"
        })
        self.assertIn(res.status_code, (200, 201))
        self.assertEqual(res.json["email"], "jane@email.com")

    def test_get_customers(self):
        res = self.client.get("/customers/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json, list)

    def test_get_customer(self):
        res = self.client.get(f"/customers/{self.customer_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["id"], self.customer_id)

    def test_update_customer(self):
        res = self.client.put(f"/customers/{self.customer_id}", json={"name": "Updated"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["name"], "Updated")

    def test_delete_customer(self):
        res = self.client.delete(f"/customers/{self.customer_id}")
        self.assertIn(res.status_code, (200, 204))

    def test_login_customer(self):
        res = self.client.post("/customers/login", json={"email": "seed_customer@email.com"})
        self.assertIn(res.status_code, (200, 400, 401))

    def test_get_my_tickets(self):
        res = self.client.get("/customers/my-tickets")
        self.assertIn(res.status_code, (200, 401))

#negative test cases

    def test_create_customer_missing_email(self):
        res = self.client.post("/customers/", json={"name": "No Email"})
        self.assertIn(res.status_code, (400, 422))

    def test_get_customer_not_found(self):
        res = self.client.get("/customers/999999")
        self.assertIn(res.status_code, (404, 400))
