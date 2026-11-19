import unittest

from app import create_app
from app.extensions import db
from app.models import User


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bienvenido", response.data)

    def test_list_users_empty(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Usuarios", response.data)
        self.assertIn(b"No hay usuarios", response.data)

    def test_create_user(self):
        response = self.client.post(
            "/users/",
            data={"username": "jperez", "email": "jperez@ejemplo.com"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"jperez", response.data)
        with self.app.app_context():
            user = User.query.filter_by(username="jperez").first()
            self.assertIsNotNone(user)

    def test_edit_user(self):
        with self.app.app_context():
            user = User(username="old", email="old@ejemplo.com")
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        response = self.client.post(
            f"/users/{user_id}",
            data={"username": "new", "email": "new@ejemplo.com"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            updated = db.session.get(User, user_id)
            self.assertEqual(updated.username, "new")
            self.assertEqual(updated.email, "new@ejemplo.com")

    def test_delete_user(self):
        with self.app.app_context():
            user = User(username="borrar", email="borrar@ejemplo.com")
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        response = self.client.post(
            f"/users/{user_id}/delete", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertIsNone(db.session.get(User, user_id))

    def test_edit_missing_user_404(self):
        response = self.client.post("/users/999")
        self.assertEqual(response.status_code, 404)

    def test_list_contains_modal(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user-modal", response.data)
        self.assertIn(b"user-form", response.data)
        self.assertIn(b"confirm-modal", response.data)


if __name__ == "__main__":
    unittest.main()
