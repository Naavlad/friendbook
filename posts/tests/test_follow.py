from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User, Comment


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title="Название группы",
            slug="test-slug",
            description="тестовый текст"
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
        self.follower_user = User.objects.create(username="FollowerUser")
        self.follower_user_authorized = Client()
        self.follower_user_authorized.force_login(self.follower_user)

    def test_profile_follow(self):
        """FollowTest authorized_client может подписываться"""
        users_follower_before = self.user.follower.count()
        follower_username = self.follower_user.username
        self.authorized_client.get(reverse(
            "profile_follow", kwargs={"username": follower_username}))
        users_follower_after = self.user.follower.count()
        self.assertEqual(users_follower_after, users_follower_before + 1)

    def test_profile_unfollow(self):
        """FollowTest authorized_client может удалять из подписок"""
        self.authorized_client.get(reverse(
            "profile_follow",
            kwargs={"username": self.follower_user.username})
        )
        users_follower_before = self.user.follower.count()
        self.authorized_client.get(reverse(
            "profile_unfollow",
            kwargs={"username": self.follower_user.username})
        )
        users_follower_after = self.user.follower.count()
        self.assertEqual(users_follower_after, users_follower_before - 1)

    def test_follow_index(self):
        """FollowTest Запись появляется в ленте подписчиков"""
        self.authorized_client.get(
            reverse("profile_follow",
                    kwargs={"username": self.follower_user.username}))
        self.follower_user_authorized.post(
            reverse("new_post"),
            {"text": "Текст публикации пользователя",
             "group": FollowTest.group.id
             }
        )
        response = self.authorized_client.get(reverse("follow_index"))
        self.assertContains(
            response, "Текст публикации пользователя")

    def test_view_post_without_follow(self):
        """FollowTest Запись не появляется в ленте подписчиков"""
        self.follower_user_authorized.post(
            reverse("new_post"),
            {"text": "Текст публикации пользователя",
             "group": FollowTest.group.id
             }
        )
        response = self.follower_user_authorized.get(reverse("follow_index"))
        self.assertNotContains(
            response, "Текст публикации пользователя")

    def test_authorized_user_may_add_comment(self):
        """FollowTest authorized_client может комментировать"""
        post = Post.objects.create(author=self.user, text="Текст сообщения")
        response = self.authorized_client.post(
            reverse("add_comment", args=[self.user.username, post.id]),
            {"text": "Текст комментария"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)

    def test_unauthorized_user_not_comment(self):
        """FollowTest guest_client не может комментировать"""
        post = Post.objects.create(author=self.user, text="Текст сообщения")
        response = self.guest_client.post(
            reverse("add_comment", args=[self.user.username, post.id]),
            {"text": "Текст комментария"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)
