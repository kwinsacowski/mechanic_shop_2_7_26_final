import unittest
from app import create_app
from app.extensions import db

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            res = self.client.post("/inventory/", json={
                "name": "Seed Part",
                "quantity": 5,
                "price": 10.0
            })
            self.assertIn(res.status_code, (200, 201))
            self.part_id = res.json.get("id")

    def test_create_part(self):
        res = self.client.post("/inventory/", json={"name": "Rotor", "quantity": 2, "price": 50.0})
        self.assertIn(res.status_code, (200, 201))

    def test_get_parts(self):
        res = self.client.get("/inventory/")
        self.assertEqual(res.status_code, 200)

    def test_get_part(self):
        res = self.client.get(f"/inventory/{self.part_id}")
        self.assertEqual(res.status_code, 200)

    def test_update_part(self):
        res = self.client.put(f"/inventory/{self.part_id}", json={"quantity": 99})
        self.assertEqual(res.status_code, 200)

    def test_delete_part(self):
        res = self.client.delete(f"/inventory/{self.part_id}")
        self.assertIn(res.status_code, (200, 204))

    def test_create_part_missing_fields(self):
        res = self.client.post("/inventory/", json={"name": "Bad"})
        self.assertIn(res.status_code, (400, 422))
