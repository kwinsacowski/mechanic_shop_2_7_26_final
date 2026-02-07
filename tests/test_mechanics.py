import unittest
from app import create_app
from app.extensions import db

class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            res = self.client.post("/mechanics/", json={
                "name": "Seed Mechanic",
                "email": "seed_mechanic@email.com",
                "phone_number": "555-111-2222"
            })
            self.assertIn(res.status_code, (200, 201))
            self.mechanic_id = res.json.get("id")

    def test_create_mechanic(self):
        res = self.client.post("/mechanics/", json={"name": "M", "email": "m@email.com", "phone_number": "555-222-3333"})
        self.assertIn(res.status_code, (200, 201))

        def test_get_mechanics(self):
            res = self.client.get("/mechanics/")
        self.assertEqual(res.status_code, 200)

    def test_get_mechanic(self):
        res = self.client.get(f"/mechanics/{self.mechanic_id}")
        self.assertEqual(res.status_code, 200)

    def test_update_mechanic(self):
        res = self.client.put(f"/mechanics/{self.mechanic_id}", json={"name": "Updated"})
        self.assertEqual(res.status_code, 200)

    def test_delete_mechanic(self):
        res = self.client.delete(f"/mechanics/{self.mechanic_id}")
        self.assertIn(res.status_code, (200, 204))

    def test_leaderboard(self):
        res = self.client.get("/mechanics/leaderboard/most-tickets")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json, list)

    def test_get_mechanic_not_found(self):
        res = self.client.get("/mechanics/999999")
        self.assertIn(res.status_code, (404, 400))
