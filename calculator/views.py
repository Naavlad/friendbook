import datetime as dt

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect

from calculator.models import PostCalc
from .forms import PostCalcForm

cash_limit = 1000


@login_required
def calc(request):
    calc_list = PostCalc.objects.all()
    paginator = Paginator(calc_list, 5)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    # Получаем день как int
    today = dt.datetime.today().day
    # Вернет Queryset -> {'amount__sum': Decimal('...')}
    today_sum_query = calc_list.filter(
        created__day=today).aggregate(Sum('amount'))
    # Достаем 'amount__sum'
    today_sum = today_sum_query['amount__sum']
    if today_sum is None:
        today_sum = 0
    # Получаем неделю как str и преобразовываем в int
    today_week = int(dt.datetime.today().strftime("%W"))
    # Вернет Queryset -> {'amount__sum': Decimal('413')}
    week_sum = calc_list.filter(
        created__week=today_week).aggregate(Sum('amount'))

    cash_message = get_message_cash_remained(today_sum)

    ctx = {
        'today_sum': today_sum,
        'cash_message': cash_message,
        'week_sum': week_sum,
        'cash_limit': cash_limit,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'calc/calc.html', ctx)


@login_required
def new_calc(request):
    form = PostCalcForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('calc')
    return render(request, 'calc/new_calc.html', {'form': form})


def get_message_cash_remained(today_sum):
    cash_remained = cash_limit - today_sum
    if cash_remained == 0:
        return "Денег нет, держись"
    if cash_remained > 0:
        return f'На сегодня осталось {cash_remained} pуб.'
    return f'Денег нет, держись: твой долг - {abs(cash_remained)} pуб.'
