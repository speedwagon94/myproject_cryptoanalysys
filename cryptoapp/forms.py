from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# Создание пользовательской формы для регистрации.
class CustomUserCreationForm(UserCreationForm):
    """
    Форма для создания нового пользователя.
    """

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields  # Удаление добавления email в поля формы.


# Создание пользовательской формы для аутентификации.
class CustomAuthenticationForm(AuthenticationForm):
    """
    Форма для аутентификации пользователей.
    """

    class Meta:
        fields = ['username', 'password']  # Поля формы для ввода имени пользователя и пароля.
