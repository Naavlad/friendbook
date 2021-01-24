import pytest

from calculator.views import get_message_cash_remained


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='TestUser',
                                                 password='1234567')


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.mark.parametrize('cash, text',
                         [
                             (500, 'На сегодня осталось 500 pуб.'),
                             (1000, 'Денег нет, держись'),
                             (1111, 'Денег нет, держись: твой долг - 111 pуб.')
                         ])
def test_get_message_cash_remained(cash, text):
    response = get_message_cash_remained(cash)
    assert response == text


def test_make_not_authorized_user(client):
    response = client.get('/new')
    assert response.status_code in (302, 301)


def test_make_authorized_user_fix(user_client):
    response = user_client.get('/new')
    assert response.status_code == 301
