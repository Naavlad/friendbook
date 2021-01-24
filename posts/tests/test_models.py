from django.test import TestCase

from posts.models import Group, Post, User


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title="Заголовок тестовой задачи",
            slug="test-task",
            description="Описание тестовой задачи"
        )

    def test_verbose_name_text(self):
        """GroupModelTest Verbose_name совпадает с ожидаемым."""
        group = GroupModelTest.group
        verbose_name_texts = {
            "title": "Сообщество",
            "description": "Описание",
            "slug": "Слаг"
        }
        for value, expected in verbose_name_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def test_title_help_text(self):
        """GroupModelTest help_text совпадает с ожидаемым."""
        group = GroupModelTest.group
        field_help_texts = {
            "title": "Добавьте название",
            "description": "Описание группы",
            "slug": "Добавьте слаг"
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected)

    def test_object_name_is_title_fild(self):
        """GroupModelTest __str__  содержит group.title."""
        group = GroupModelTest.group
        expected_object_name = group.title
        self.assertEquals(expected_object_name, str(group))


class PostModelTest(TestCase):
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

    def test_text_label(self):
        """PostModelTest verbose_name поля text совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verbose_name = {
            "text": "Текст",
            "pub_date": "Дата публикации",
            "author": "Автор",
            "group": "Сообщество",
        }
        for value, expected in field_verbose_name.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """PostModelTest help_text поля text совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_text = {
            "text": "Добавьте текст",
            "pub_date": "Добавьте дату публикации",
            "author": "Добавьте автора",
            "group": "Добавьте сообщество",
        }
        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)

    def test_object_name_is_title_fild(self):
        """PostModelTest __str__ это строчка с содержимым post.title."""
        post = PostModelTest.post.text
        expected_object_name = post
        self.assertEquals(expected_object_name, str(post))

    def test_object_name_is_title_field(self):
        """PostModelTest __str__  post.title меньше 15 символов."""
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEquals(expected_object_name, str(post))

    def test_long_object_name_is_title_field(self):
        """PostModelTest __str__ post.title больше 15 символов """
        post_long = Post.objects.create(
            text="123451234512345>Больше чем нужно",
            pub_date="2021-01-09",
            author=User.objects.create(username="testuser_long"),
            group=PostModelTest.group
        )
        expected_post_long_text = post_long.text[:15]
        self.assertEquals(expected_post_long_text, str(post_long))
