import tempfile
import shutil

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User


class PostViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title="Заголовок тестовой группы",
            description="Описание группы",
            slug="test-group"
        )
        cls.post = Post.objects.create(
            text="Текст сообщения",
            pub_date="2020-12-15",
            author=User.objects.create(username="testuser"),
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create(username="StasBasov")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.new_user = Client()

    def test_pages_uses_correct_template(self):
        """PostViewsTest страницы используют правильный шаблон"""
        templates_pages_names = {
            "index.html": reverse("index"),
            "group.html": reverse("group", kwargs={"slug": "test-group"}),
            "post_edit.html": reverse("new_post"),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """PostViewsTest  Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("index"))
        page_context = response.context["page"][0]
        context_test_expectation = {
            page_context.text: PostViewsTest.post.text,
            page_context.author: PostViewsTest.post.author,
            page_context.group: PostViewsTest.post.group,
        }
        for context, test_expectation in context_test_expectation.items():
            with self.subTest():
                self.assertEqual(context, test_expectation)

    def test_group_page_show_correct_context(self):
        """PostViewsTest Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("group", kwargs={"slug": PostViewsTest.group.slug}))
        page_context = response.context["page"][0]
        context_test_expectation = {
            page_context.text: PostViewsTest.post.text,
            page_context.author: PostViewsTest.post.author,
            page_context.group: PostViewsTest.post.group,
            page_context.pub_date: PostViewsTest.post.pub_date,
        }
        for context, test_expectation in context_test_expectation.items():
            with self.subTest():
                self.assertEqual(context, test_expectation)

    def test_create_post_with_group_index(self):
        """PostViewsTest создания поста index.html"""
        cache.clear()
        new_post = Post.objects.create(
            text="Новый Текст сообщения",
            author=self.user,
            group=PostViewsTest.group,
        )
        response = self.new_user.get(reverse("index"))
        self.assertContains(response, new_post)

    def test_create_content_group(self):
        """PostViewsTest создания поста group.html"""
        new_post = Post.objects.create(
            text="Новый текст сообщения",
            author=self.user,
            group=PostViewsTest.group
        )
        response = self.new_user.get(
            reverse("group", args=["test-group"]))
        self.assertContains(response, new_post)


class PostImgTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем временную папку для медиа-файлов
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.small_gif = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                         b'\x01\x00\x80\x00\x00\x00\x00\x00'
                         b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                         b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                         b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                         b'\x0A\x00\x3B')

        cls.uploaded = SimpleUploadedFile(
            name="small.gif",
            content=cls.small_gif,
            content_type="image/gif"
        )

        cls.group = Group.objects.create(
            title="Заголовок тестовой группы",
            description="Описание группы",
            slug="test-group"
        )
        cls.post = Post.objects.create(
            text="Текст сообщения",
            pub_date="2020-12-15",
            author=User.objects.create(username="testuser"),
            group=cls.group,
            image=cls.uploaded
        )

    @classmethod
    def tearDownClass(cls):
        # Модуль shutil
        # создание, удаление, копирование, перемещение, изменение папок, файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()

    def test_index_page_show_correct_context_img(self):
        """PostImgTest Index с картинкой передаётся в словаре context"""
        response = self.guest_client.get(reverse("index"))
        context_test_expectation = "posts/small.gif"
        test_expectation = response.context.get("page")[0].image
        self.assertEqual(context_test_expectation, test_expectation,
                         "Index img сформирован с неправильным контекстом")

    def test_group_page_show_correct_context_img(self):
        """PostImgTest Group с картинкой передаётся в словаре context"""
        response = self.authorized_client.get(
            reverse("group", kwargs={"slug": self.group.slug}))
        context_test_expectation = "posts/small.gif"
        test_expectation = response.context.get("page")[0].image
        self.assertEqual(context_test_expectation, test_expectation,
                         "Group img сформирован с неправильным контекстом")

    def test_post_page_show_correct_context_img(self):
        """PostImgTest Post с картинкой передаётся в словаре context"""
        form_data = {
            "group": PostImgTest.group,
            "text": PostImgTest.post.text,
            "image": PostImgTest.uploaded,
        }
        context_test_expectation = "posts/small.gif"
        test_expectation = Post.objects.get(text=form_data["text"]).image
        # Почему к text обращение не понятно совсем
        self.assertEqual(context_test_expectation, test_expectation,
                         "Post img сформирован с неправильным контекстом")

    def test_profile_page_show_correct_context_img(self):
        """PostImgTest Profile с картинкой передаётся в словаре context"""
        response = self.authorized_client.get(
            reverse("profile", args=["testuser"])
        )
        context_test_expectation = "posts/small.gif"
        test_expectation = response.context.get("page")[0].image
        self.assertEqual(context_test_expectation, test_expectation,
                         "Profile img сформирован с неправильным контекстом")

    def test_new_post_img_create(self):
        """PostImgTest создания поста с картинкой через PostForm"""
        self.small_gif_new = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                              b'\x01\x00\x80\x00\x00\x00\x00\x00'
                              b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                              b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                              b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                              b'\x0A\x00\x3B')

        self.uploaded_new = SimpleUploadedFile(
            name="small_new.gif",
            content=self.small_gif_new,
            content_type="image/gif"
        )
        posts_count = Post.objects.count()
        self.post_new = Post.objects.create(
            text="Текст сообщения_new",
            pub_date="2021-01-10",
            author=User.objects.create(username="testuser_new"),
            group=PostImgTest.group,
            image=self.uploaded_new
        )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(image='posts/small_new.gif').exists()
        )
