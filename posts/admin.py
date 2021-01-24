from django.contrib import admin

from .models import Post, Group, Follow, Comment


class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description")
    empty_value_display = "-пусто-"


admin.site.register(Group, GroupAdmin)


class PostAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("pk", "text", "pub_date", "author")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("text",)
    # добавляем возможность фильтрации по дате
    list_filter = ("pub_date",)
    # дефолтное значение `-пусто-` для пустого поля
    empty_value_display = "-пусто-"


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "created", "author")
    empty_value_display = "-пусто-"


admin.site.register(Comment, CommentAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")
    empty_value_display = "-пусто-"


admin.site.register(Follow, FollowAdmin)
