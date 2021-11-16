from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Snack

class TestSnacks(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", email="admin@admin.com", password="secretpassword"
        )

        self.snack = Snack.objects.create(
            title="choccymilk", description="Heavenly.", purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "choccymilk")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "choccymilk")
        self.assertEqual(f"{self.snack.purchaser}", "admin")
        self.assertEqual(self.snack.description, "Heavenly.")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "choccymilk")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "admin")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "Kinder",
                "description": "Little kids scam",
                "purchaser": self.user.id,
            }, follow=True
        )
        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "Kinder")

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "Updated name","description":"Elixir of life.","reviewer":self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)