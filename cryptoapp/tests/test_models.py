from django.test import TestCase
from cryptoapp.models import UserRequest, News


class UserRequestModelTestCase(TestCase):
    """
    Проверка модели UserRequest
    """

    def test_user_request_creation(self):
        user_request = UserRequest.objects.create(symbol='BTC', interval='1h')
        self.assertIsInstance(user_request, UserRequest)
        self.assertEqual(user_request.symbol, 'BTC')
        self.assertEqual(user_request.interval, '1h')


class NewsModelTestCase(TestCase):
    """
    Проверка модели News
    """

    def test_news_creation(self):
        news = News.objects.create(title='Test News', content='This is a test news', pub_date='2023-09-29')
        self.assertIsInstance(news, News)
        self.assertEqual(news.title, 'Test News')
        self.assertEqual(news.content, 'This is a test news')
        self.assertEqual(news.pub_date, '2023-09-29')
