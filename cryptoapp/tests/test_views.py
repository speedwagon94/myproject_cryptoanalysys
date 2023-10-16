from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from cryptoapp.models import UserRequest


# class AboutViewTestCase(TestCase):
#     """
#     Проверка представления about
#     """
#
#     def test_about_view(self):
#         # Создаем GET-запрос к странице "О нас" (about) с использованием reverse
#         response = self.client.get(reverse('about'))
#
#         # Проверяем, что страница успешно загрузилась (HTTP-статус 200 OK)
#         self.assertEqual(response.status_code, 200)
#
#         # Проверяем, что используется правильный шаблон
#         self.assertTemplateUsed(response, 'cryptoapp/about.html')
#
#
# class LogoutManagerTestCase(TestCase):
#     def setUp(self):
#         # Создаем тестового пользователя
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#
#     def test_logout_view(self):
#         # Аутентифицируем пользователя (вход в систему)
#         self.client.login(username='testuser', password='testpassword')
#
#         # Создаем GET-запрос к представлению выхода (logout) с использованием reverse
#         response = self.client.get(reverse('logout'))
#
#         # Проверяем, что пользователь успешно вышел из системы (HTTP-статус 302 Redirect)
#         self.assertEqual(response.status_code, 302)
#
#         # Проверяем, что произошло перенаправление на страницу 'analyze_crypto'
#         self.assertRedirects(response, reverse('analyze_crypto'))
#
#
# class LoginManagerTestCase(TestCase):
#     def setUp(self):
#         # Создаем тестового пользователя
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#
#     def test_login_view(self):
#         # Создаем POST-запрос к странице входа с правильными учетными данными
#         response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
#
#         # Проверяем, что аутентификация прошла успешно
#         user = authenticate(username='testuser', password='testpassword')
#         self.assertTrue(user.is_authenticated)
#
#         # Проверяем, что пользователь был перенаправлен на страницу анализа криптовалюты
#         self.assertRedirects(response, reverse('analyze_crypto'))
#
#     def test_login_view_with_invalid_credentials(self):
#         # Создаем POST-запрос к странице входа с неправильными учетными данными
#         response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
#
#         # Проверяем, что аутентификация не прошла
#         user = authenticate(username='testuser', password='wrongpassword')
#         self.assertIsNone(user)
#
#         # Проверяем, что пользователь не был перенаправлен на страницу анализа криптовалюты
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'cryptoapp/login.html')
#
#
# class RegistrationManagerTestCase(TestCase):
#     """
#     Тестирование RegistrationManager
#     """
#
#     def test_registration_view(self):
#         # Создаем POST-запрос к странице регистрации
#         response = self.client.post(reverse('register'), {
#             'username': 'testuser',
#             'password1': 'testpassword123',
#             'password2': 'testpassword123',
#         })
#
#         # Проверяем, что пользователь был успешно создан
#         self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление (HTTP-статус 302)
#         self.assertTrue(
#             User.objects.filter(username='testuser').exists())  # Проверяем наличие пользователя в базе данных
#
#         # Проверяем, что пользователь вошел в систему
#         response = self.client.get(reverse('analyze_crypto'))
#         self.assertEqual(response.status_code, 200)  # Ожидаем успешный доступ к странице (HTTP-статус 200)
#
#     def test_registration_view_with_invalid_data(self):
#         # Создаем POST-запрос с неправильными данными
#         response = self.client.post(reverse('register'), {
#             'username': 'testuser',
#             'password1': 'testpassword123',
#             'password2': 'differentpassword',
#         })
#
#         # Проверяем, что пользователь не был создан
#         self.assertEqual(response.status_code, 200)  # Ожидаем успешное отображение страницы регистрации
#         self.assertFalse(
#             User.objects.filter(username='testuser').exists())  # Проверяем отсутствие пользователя в базе данных


class CryptoAnalyzerTestCase(TestCase):
    """
    Тестирование CryptoAnalyzer
    """

    def test_analyze_crypto_view(self):
        # Создаем POST-запрос к странице анализа криптовалюты
        response = self.client.post(reverse('analyze_crypto'), {
            'symbol': 'BTCUSDT',
            'interval': '1h',
        })

        # Проверяем, что страница анализа успешно загрузилась
        self.assertEqual(response.status_code, 200)

        # Проверяем, что был создан объект UserRequest в базе данных
        self.assertTrue(UserRequest.objects.filter(symbol='BTCUSDT', interval='1h').exists())
