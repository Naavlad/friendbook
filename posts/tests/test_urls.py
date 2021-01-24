from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user1 = User.objects.create(username="Leo")
        cls.user2 = User.objects.create(username="Alex")
        cls.guest_client = Client()
        cls.creator_user = Client()
        cls.creator_user.force_login(cls.user1)
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.user2)

        cls.group = Group.objects.create(
            title="Заголовок группы",
            slug="test-slug",
            description="Тестовый текст группы"
        )

        cls.post = Post.objects.create(
            text="Текст Post",
            author=cls.user1,
            group=cls.group
        )

        cls.list_pages = {
            reverse("index"): "index.html",
            reverse("profile",
                    kwargs={"username": cls.user1.username}): "profile.html",
            reverse("group",
                    kwargs={"slug": cls.group.slug}): "group.html",
            reverse("post",
                    kwargs={
                        "username": cls.user1.username,
                        "post_id": cls.post.id}): "post.html",
        }

    def test_other_pages_guest_client_status_code_200(self):
        """StaticURLTests Проверки страниц guest_client код 200"""
        for page, template in StaticURLTests.list_pages.items():
            response = StaticURLTests.guest_client.get(page)
            self.assertEqual(
                response.status_code, 200,
                f"Страница {page} не отвечает"
            )

    def test_other_pages_authorized_client_status_code_200(self):
        """StaticURLTests Проверки страниц authorized_user код 200"""
        for page, template in StaticURLTests.list_pages.items():
            response = StaticURLTests.guest_client.get(page)
            self.assertEqual(
                response.status_code, 200,
                f"Страница {page} не отвечает"
            )

    def test_other_pages_guest_client_templates(self):
        """StaticURLTests Проверка шаблонов guest_client"""
        for page, template in StaticURLTests.list_pages.items():
            response = StaticURLTests.guest_client.get(page)
            self.assertTemplateUsed(
                response, template,
                f"{page} шаблон {template} не работает"
            )

    def test_other_pages_authorized_user_templates(self):
        """StaticURLTests Проверка шаблонов authorized_user"""
        for page, template in StaticURLTests.list_pages.items():
            response = StaticURLTests.authorized_user.get(page)
            self.assertTemplateUsed(
                response, template,
                f"{page} шаблон {template} не работает"
            )

    def test_post_edit_guest_client_200(self):
        """StaticURLTests Проверки для страницы post_edit(post_new.html)"""
        username = StaticURLTests.user1.username
        response = StaticURLTests.guest_client.get(
            reverse("post_edit",
                    kwargs={"username": username, "post_id": 1}), follow=True)
        self.assertEqual(
            response.status_code, 200,
            "post_edit пользователь гость не может зайти."
        )

    def test_post_edit_authorized_user_200(self):
        username = StaticURLTests.user1.username
        response = StaticURLTests.authorized_user.get(
            reverse("post_edit",
                    kwargs={"username": username, "post_id": 1}), follow=True)
        self.assertEqual(
            response.status_code, 200,
            "post_edit авторизованный пользователь не может зайти."
        )

    def test_post_edit_creator_user_200(self):
        username = StaticURLTests.user1.username
        response = StaticURLTests.creator_user.get(
            reverse("post_edit",
                    kwargs={"username": username, "post_id": 1}), follow=True)
        self.assertEqual(
            response.status_code, 200,
            "post_edit неавторизованный пользователь не может зайти."
        )

    def test_post_edit_template(self):
        username = StaticURLTests.user1.username
        response = StaticURLTests.creator_user.get(
            reverse("post_edit", kwargs={"username": username, "post_id": 1}))
        self.assertTemplateUsed(
            response, "post_edit.html",
            "post_edit не возвращает post_new.html"
        )

    def test_post_edit_authorized_user_redirect(self):
        username = StaticURLTests.user1.username
        response = StaticURLTests.authorized_user.get(
            reverse(
                "post_edit", kwargs={"username": username, "post_id": 1}))
        self.assertRedirects(
            response,
            reverse("post", args=[username, StaticURLTests.post.id]))

    def test_new_url_exists_at_desired_location(self):
        """StaticURLTests Страница /new доступна любому пользователю."""
        response = StaticURLTests.guest_client.get("/new/")
        self.assertEqual(response.status_code, 302)

    def test_new_url_exists_at_desired_location_authorized(self):
        """StaticURLTests /new доступна авторизованному пользователю."""
        response = StaticURLTests.authorized_user.get("/new/")
        self.assertEqual(response.status_code, 200)

    def test_error_404_cod_exist(self):
        """StaticURLTests Возвращает сервер 404, если страница не найдена"""
        response = StaticURLTests.guest_client.get("/qwerty/")
        self.assertEqual(
            response.status_code, 404,
            "Сервер не возвращает код 404 если страница не найдена"
        )

    def test_error_404_cod_Template_exist(self):
        """U Возвращает ли сервер шаблон 404, если страница не найдена"""
        response = StaticURLTests.guest_client.get("page_not_found")
        self.assertTemplateUsed(
            response, "misc/404.html",
            "page_not_found не возвращает misc/404.html"
        )
