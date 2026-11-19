import unittest
from datetime import datetime

from app import create_app
from app.extensions import db
from app.models import Event, User


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

    def test_calendar_page(self):
        response = self.client.get("/calendar/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Calendario", response.data)
        self.assertIn(b'id="calendar"', response.data)

    def test_calendar_api_events_empty(self):
        response = self.client.get("/calendar/api/events")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        user_events = [
            e for e in data if not e.get("extendedProps", {}).get("holiday")
        ]
        self.assertEqual(user_events, [])
        self.assertTrue(
            any(e.get("extendedProps", {}).get("holiday") for e in data)
        )

    def test_sidebar_has_calendar_link(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'href="/calendar/"', response.data)

    def test_calendar_page_has_event_modal(self):
        response = self.client.get("/calendar/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event-modal", response.data)
        self.assertIn(b"event-form", response.data)
        self.assertIn(b"btn-new-event", response.data)
        self.assertIn(b"event-dropdown", response.data)
        self.assertIn(b"event-detail-modal", response.data)
        self.assertNotIn(b"event-delete-btn", response.data)

    def test_create_event(self):
        response = self.client.post(
            "/calendar/events/",
            data={
                "title": "Reunión",
                "description": "Nota",
                "start": "2026-11-20T10:00",
                "end": "2026-11-20T11:00",
                "color": "#dcfce7",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Evento creado", response.data)
        with self.app.app_context():
            event = Event.query.filter_by(title="Reunión").first()
            self.assertIsNotNone(event)
            self.assertEqual(event.color, "#dcfce7")

        api = self.client.get("/calendar/api/events").get_json()
        user_events = [
            e for e in api if not e.get("extendedProps", {}).get("holiday")
        ]
        self.assertEqual(len(user_events), 1)
        self.assertEqual(user_events[0]["title"], "Reunión")
        self.assertIn("start", user_events[0])
        self.assertEqual(user_events[0]["color"], "#dcfce7")
        self.assertEqual(user_events[0]["textColor"], "#15803d")

    def test_create_event_requires_title(self):
        response = self.client.post(
            "/calendar/events/",
            data={"title": "", "start": "2026-11-20T10:00"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("título".encode(), response.data.lower())
        with self.app.app_context():
            self.assertEqual(Event.query.count(), 0)

    def test_create_event_end_before_start_fails(self):
        response = self.client.post(
            "/calendar/events/",
            data={
                "title": "Mal",
                "start": "2026-11-20T10:00",
                "end": "2026-11-20T09:00",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertEqual(Event.query.count(), 0)

    def test_update_event(self):
        with self.app.app_context():
            event = Event(title="Viejo", start=datetime(2026, 11, 20, 10, 0))
            db.session.add(event)
            db.session.commit()
            event_id = event.id

        response = self.client.post(
            f"/calendar/events/{event_id}",
            data={"title": "Nuevo", "start": "2026-11-21T10:00"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"actualizado", response.data)
        with self.app.app_context():
            updated = db.session.get(Event, event_id)
            self.assertEqual(updated.title, "Nuevo")

    def test_delete_event(self):
        with self.app.app_context():
            event = Event(title="Borrar", start=datetime(2026, 11, 20, 10, 0))
            db.session.add(event)
            db.session.commit()
            event_id = event.id

        response = self.client.post(
            f"/calendar/events/{event_id}/delete", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertIsNone(db.session.get(Event, event_id))

    def test_delete_missing_event_404(self):
        response = self.client.post("/calendar/events/999/delete")
        self.assertEqual(response.status_code, 404)

    def test_create_all_day_event_api_format(self):
        response = self.client.post(
            "/calendar/events/",
            data={
                "title": "Día libre",
                "all_day": "on",
                "start": "2026-11-25",
                "end": "2026-11-25",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        api = self.client.get("/calendar/api/events").get_json()
        user_events = [
            e for e in api if not e.get("extendedProps", {}).get("holiday")
        ]
        self.assertEqual(len(user_events), 1)
        self.assertTrue(user_events[0]["allDay"])
        self.assertEqual(user_events[0]["start"], "2026-11-25")
        self.assertNotIn("end", user_events[0])

    def test_invalid_color_uses_default(self):
        response = self.client.post(
            "/calendar/events/",
            data={"title": "Color malo", "start": "2026-11-20T10:00", "color": "#zzzzzz"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        api = self.client.get("/calendar/api/events").get_json()
        user_events = [
            e for e in api
            if not e.get("extendedProps", {}).get("holiday")
            and e["title"] == "Color malo"
        ]
        self.assertEqual(user_events[0]["color"], "#dbeafe")

    def test_colombian_holidays_2026(self):
        from app.holidays import colombian_holidays

        holidays = colombian_holidays(2026)
        self.assertEqual(len(holidays), 17)
        by_date = {h["date"].isoformat(): h["title"] for h in holidays}
        self.assertEqual(by_date["2026-12-25"], "Navidad")
        self.assertEqual(by_date["2026-01-01"], "Año Nuevo")
        self.assertIn("Viernes Santo", by_date.values())
        self.assertIn("Jueves Santo", by_date.values())
        self.assertIn("Ascensión del Señor", by_date.values())

    def test_api_includes_holidays(self):
        response = self.client.get(
            "/calendar/api/events?start=2026-12-01&end=2027-01-01"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        holidays = [
            e for e in data if e.get("extendedProps", {}).get("holiday") is True
        ]
        self.assertTrue(holidays)
        navidad = next(e for e in holidays if e["title"] == "Navidad")
        self.assertEqual(navidad["start"], "2026-12-25")
        self.assertTrue(navidad["allDay"])
        self.assertEqual(navidad["color"], "#f1f5f9")
        self.assertIn("fc-holiday", navidad["classNames"])

    def test_api_holidays_do_not_break_events(self):
        with self.app.app_context():
            event = Event(title="Reunión", start=datetime(2026, 12, 24, 10, 0))
            db.session.add(event)
            db.session.commit()

        response = self.client.get(
            "/calendar/api/events?start=2026-12-01&end=2027-01-01"
        )
        data = response.get_json()
        titles = [e["title"] for e in data]
        self.assertIn("Reunión", titles)
        self.assertIn("Navidad", titles)


if __name__ == "__main__":
    unittest.main()
