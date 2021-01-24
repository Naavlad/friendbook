from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PostCalc(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='postscalc'
    )
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    text_comment = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"text - {self.text_comment} amount - {self.amount}"

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Записи калькулятора'
        verbose_name = 'Запись калькулятора'
