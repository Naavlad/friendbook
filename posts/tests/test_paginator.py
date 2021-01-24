from django.test import Client, TestCase
from django.urls import reverse

from posts.models import User, Group, Post


class PaginatorViewsTest(TestCase):
    # Здесь создаются фикстуры: клиент и 13 тестовых записей.
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(username="TestUser")
        Group.objects.create(
            title="Название группы",
            slug="test-slug",
            description="тестовый текст"
        )
        cls.group = Group.objects.first()
        for i in range(12):
            Post.objects.create(
                text=f"Тестовый текст {i}",
                pub_date="2020-12-26",
                author=user,
                group=cls.group
            )

        cls.post = Post.objects.create(
            text="Текст сообщения",
            pub_date="2020-12-15",
            author=User.objects.create(username="testuser"),
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()

    def test_first_page_containse_ten_records(self):
        """PaginatorViewsTest количество постов на первой странице равно 10"""
        response = self.client.get(reverse("index"))
        # Проверка: количество постов на первой странице равно 10.
        self.assertEqual(len(response.context.get("page").object_list), 10)

    def test_second_page_containse_three_records(self):
        """PaginatorViewsTest на второй странице должно быть три поста"""
        # Проверка: на второй странице должно быть 3 поста.
        response = self.client.get(reverse("index") + "?page=2")
        self.assertEqual(len(response.context.get("page").object_list), 3)
