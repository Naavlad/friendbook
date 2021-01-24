from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Post, Group


class PostCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title="Лев толстой",
            slug="test-slug",
            description="Тестовое описание"
        )

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="test-user")
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_new_post_create_post_end_redirect(self):
        """PostCreateFormTest соханения данных и redirect для new_post"""
        form_data = {
            "group": PostCreateFormTest.group.id,
            "text": "Тестовый текст",
        }
        number_posts = Post.objects.count()
        new_post = reverse("new_post")
        response = self.authorized_user.post(
            new_post, data=form_data, follow=True
        )
        self.assertEqual(
            response.status_code, 200,
            "Страница post_edit.html не отвечает"
        )
        self.assertEqual(
            Post.objects.count(), number_posts + 1,
            "Количество постов меньше 1"
        )
        self.assertRedirects(response, reverse("index"))

    def test_post_edit_create_post_end_redirect(self):
        """PostCreateFormTest соханения данных и redirect для post_edit"""
        self.post = Post.objects.create(
            text="Текст поста.",
            group=PostCreateFormTest.group,
            author=self.user
        )
        form_data = {
            "group": PostCreateFormTest.group.id,
            "text": "Тестовый текст",
        }
        response = self.authorized_user.post(
            reverse("post_edit", args=[self.post.author, self.post.id]),
            data=form_data, follow=True)

        self.assertEqual(
            response.status_code, 200,
            "Страница post_new.html не отвечает")

        self.assertEqual(
            Post.objects.get(id=self.post.id).text,
            form_data["text"], "Пост не меняется.")

        self.assertRedirects(
            response,
            reverse("post", args=[self.post.author, self.post.id]))
