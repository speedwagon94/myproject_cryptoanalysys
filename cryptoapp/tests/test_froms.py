from django.test import TestCase
from django.contrib.auth.models import User
from cryptoapp.forms import CustomUserCreationForm, CustomAuthenticationForm


class CustomUserCreationFormTestCase(TestCase):
    """
    Проверка формы CustomUserCreationForm
    """
    def test_form_valid(self):
        # Создание данных для заполнения формы
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = CustomUserCreationForm(data=form_data)

        # Проверка, что форма валидна (должна быть валидной)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        # Создание данных для заполнения формы
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'differentpassword',  # Пароли не совпадают
        }
        form = CustomUserCreationForm(data=form_data)

        # Проверка, что форма невалидна (должна быть невалидной)
        self.assertFalse(form.is_valid())


class CustomAuthenticationFormTestCase(TestCase):
    """
    Проверка формы CustomAuthenticationForm
    """
    def test_form_valid(self):
        # Создание тестового пользователя
        User.objects.create_user(username='testuser', password='testpassword')

        # Создание данных для заполнения формы
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        form = CustomAuthenticationForm(data=form_data)

        # Проверка, что форма валидна (должна быть валидной)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        # Создание данных для заполнения формы
        form_data = {
            'username': 'testuser',
            'password': 'incorrectpassword',  # Неверный пароль
        }
        form = CustomAuthenticationForm(data=form_data)

        # Проверка, что форма невалидна (должна быть невалидной)
        self.assertFalse(form.is_valid())
