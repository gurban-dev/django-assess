"""Tests are split into the working lesson example and student assessment."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Task


class DemonstrationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_lists_tasks(self):
        Task.objects.create(title="Prepare lesson")
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id": 1, "title": "Prepare lesson", "completed": False}])

    def test_post_creates_task(self):
        response = self.client.post("/api/tasks/", {"title": "Review serializers"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Review serializers")
        self.assertEqual(Task.objects.count(), 1)

    def test_post_without_required_title_returns_validation_error(self):
        response = self.client.post("/api/tasks/", {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)


class AssessmentRequirementsTests(TestCase):
    """These are intentionally failing until the student implements the brief."""

    def setUp(self):
        self.client = APIClient()
        self.alice = get_user_model().objects.create_user(username="alice", password="pass1234")
        self.bob = get_user_model().objects.create_user(username="bob", password="pass1234")

    def create_as_alice(self):
        self.client.force_authenticate(self.alice)
        return self.client.post("/api/tasks/", {"title": "Alice task"}, format="json")

    def test_task_creation_requires_authentication(self):
        response = self.client.post("/api/tasks/", {"title": "No owner"}, format="json")
        self.assertIn(response.status_code, (401, 403))

    def test_authenticated_create_assigns_owner(self):
        self.client.force_authenticate(self.alice)
        response = self.client.post("/api/tasks/", {"title": "Owned task"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["owner"], self.alice.pk)

    def test_retrieve_task(self):
        created = self.create_as_alice()
        response = self.client.get(f"/api/tasks/{created.data['id']}/")
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        self.client.force_authenticate(self.alice)
        created = self.client.post("/api/tasks/", {"title": "Owned task"}, format="json")
        response = self.client.patch(
            f"/api/tasks/{created.data['id']}/", {"completed": True}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["completed"])

    def test_delete_task(self):
        self.client.force_authenticate(self.alice)
        created = self.client.post("/api/tasks/", {"title": "Owned task"}, format="json")
        response = self.client.delete(f"/api/tasks/{created.data['id']}/")
        self.assertEqual(response.status_code, 204)

    def test_missing_task_returns_not_found(self):
        self.client.force_authenticate(self.alice)
        response = self.client.get("/api/tasks/99999/")
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_update_another_users_task(self):
        created = self.create_as_alice()
        self.client.force_authenticate(self.bob)
        response = self.client.patch(
            f"/api/tasks/{created.data['id']}/", {"title": "Changed"}, format="json"
        )
        self.assertIn(response.status_code, (403, 404))

    def test_empty_title_is_rejected(self):
        response = self.client.post("/api/tasks/", {"title": "   "}, format="json")
        self.assertEqual(response.status_code, 400)
