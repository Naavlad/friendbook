from django import forms
from django.forms import TextInput, DecimalField

from .models import PostCalc


class PostCalcForm(forms.ModelForm):
    class Meta:
        model = PostCalc
        fields = ('text_comment', 'amount')

        widgets = {
            'text_comment': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '* Сделайте комментарий к записи'
            }),
            'amount': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '* Ведите сумму'
            }),
        }
