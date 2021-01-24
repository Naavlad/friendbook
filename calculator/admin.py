from django.contrib import admin

from .models import PostCalc


class PostCalcAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'amount', 'text_comment', 'created')
    empty_value_display = '-пусто-'


admin.site.register(PostCalc, PostCalcAdmin)
