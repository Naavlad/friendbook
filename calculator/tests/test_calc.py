from django.forms import forms
from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth import get_user_model

from calculator.models import PostCalc
from calculator.views import get_message_cash_remained

User = get_user_model()


class PostCalcTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user_setup')
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)
        self.not_authorized_user = Client()

        self.start_post = PostCalc.objects.create(
            author=self.user,
            text_comment='for_test_food_start',
            amount=15,
        )

    def test_calc(self):
        posts_count_before = PostCalc.objects.count()
        # Второй пост для счетчика
        PostCalc.objects.create(
            author=self.user,
            text_comment='for_test_food',
            amount=25,
        )
        posts_count_after = PostCalc.objects.count()
        self.assertEqual(posts_count_after, posts_count_before + 1)

        response = self.authorized_user.get(reverse('calc'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'for_test_food_start')
        self.assertContains(response, 'for_test_food')
        self.assertContains(response, 25)
        self.assertTemplateUsed(response, 'calc/calc.html')

    def test_new_calc_create_redirect(self):
        form_data = {
            'text_comment': 'text_comment_new_post',
            'amount': 25,
        }
        new_post_template = reverse('new_calc')
        response = self.authorized_user.post(
            new_post_template, data=form_data, follow=True
        )
        post = self.start_post
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'text_comment_new_post')
        self.assertRedirects(response, reverse('calc'))
        self.assertTemplateUsed(response, 'calc/calc.html')

    def test_get_message_cash_remained(self):
        cash_limit = 1000
        cash_list = {
            500: 'На сегодня осталось 500 pуб.',
            1000: 'Денег нет, держись',
            1111: 'Денег нет, держись: твой долг - 111 pуб.'
        }
        for cash, text in cash_list.items():
            response = get_message_cash_remained(cash)
            self.assertEqual(response, text)

    def test_make_not_authorized_user(self):
        not_response = self.not_authorized_user.get(reverse('calc'))
        self.assertEqual(not_response.status_code, 302,
                         'Закрыть доступ not_authorized_user')
        not_response = self.not_authorized_user.get(reverse('new_calc'))
        self.assertEqual(not_response.status_code, 302,
                         'Закрыть доступ not_authorized_user')
