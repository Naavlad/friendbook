from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import User


class CacheTest(TestCase):
    def setUp(self):
        self.text = "Текст поста"
        self.client = Client()
        self.user = User.objects.create_user(username="testuser")
        self.client.force_login(self.user)

    def test_index_page_cahe(self):
        """CacheTest отображение новой записи до и после cache.clear"""
        self.client.get(reverse("index"))
        self.client.post(reverse("new_post"), {"text": self.text})
        response = self.client.get(reverse("index"))
        self.assertNotContains(response, self.text)
        cache.clear()
        response = self.client.get(reverse("index"))
        self.assertContains(response, self.text)
