from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("group", "text", "image")
        labels = {
            "text": "Текст публикации",
            "group": "Сообщество/группа",
            "image": "Фото/видео"
        }
        help_texts = {
            "text": "Добавьте текст публикации",
            "group": "Выберите сообщество/группу",
            "image": "Загрузите изображение или видео"
        }
        widgets = {"text": forms.Textarea({"rows": 5})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

        widgets = {
            "text": forms.TextInput(
                attrs={'placeholder': "* Добавьте текст комментария"})
        }
