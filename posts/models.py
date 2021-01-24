from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        "Сообщество", max_length=200, help_text="Добавьте название"
    )
    slug = models.SlugField(
        "Слаг", unique=True, help_text="Добавьте слаг"
    )
    description = models.TextField("Описание", help_text="Описание группы")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщество"
        verbose_name_plural = "Сообщества"


class Post(models.Model):
    text = models.TextField("Текст", help_text="Добавьте текст")
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True,
        help_text="Добавьте дату публикации"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="Добавьте автора",
        related_name="posts", verbose_name="Автор"
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        help_text="Добавьте сообщество", related_name="posts",
        blank=True, null=True, verbose_name="Сообщество"
    )
    image = models.ImageField(upload_to="posts/", blank=True, null=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField("Текст комментария")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Коментарии"


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    def __str__(self):
        return f"follower - {self.user} following - {self.author}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_follow"
            )
        ]
