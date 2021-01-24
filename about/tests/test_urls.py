from django.test import TestCase, Client


class StaticPagesURLTests(TestCase):
    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_author_url_exists_at_desired_location(self):
        """StaticPagesURLTests Проверка доступности адреса author/."""
        response = self.guest_client.get("/about/author/")
        self.assertEqual(response.status_code, 200)

    def test_tech_url_exists_at_desired_location(self):
        """StaticPagesURLTests Проверка доступности адреса tech/."""
        response = self.guest_client.get("/about/tech/")
        self.assertEqual(response.status_code, 200)

    def test_tech_url_uses_correct_template(self):
        """StaticPagesURLTests Проверка шаблона для адреса /about/tech/."""
        response = self.guest_client.get("/about/tech/")
        self.assertTemplateUsed(response, "about/tech.html")

    def test_about_url_uses_correct_template(self):
        """StaticPagesURLTests Проверка шаблона для адреса /about/author/."""
        response = self.guest_client.get("/about/author/")
        self.assertTemplateUsed(response, "about/author.html")
