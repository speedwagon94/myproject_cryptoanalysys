from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime, timedelta
from .forms import CustomUserCreationForm
from .api.binance_api import analyze_data, get_binance_client, fetch_historical_data, interval_mapping
from .api.chatgpt_api import generate_gpt3_response
import logging
from .models import UserRequest, News

logger = logging.getLogger(__name__)


class CryptoAnalyzer:
    @staticmethod
    def analyze_crypto(request):
        """
        Анализирует криптовалюту на основе данных, полученных от пользователя.

        :param request: Запрос от пользователя с данными о символе и интервале.
        :return: HTTP-ответ с результатами анализа.
        """
        if request.method == 'POST':
            symbol = request.POST.get('symbol')
            user_interval = request.POST.get('interval')

            user_request = UserRequest(symbol=symbol, interval=user_interval)
            user_request.save()
            binance_interval = interval_mapping[user_interval]

            try:
                client = get_binance_client()
                historical_data = fetch_historical_data(client, symbol, binance_interval)
                analysis_result = analyze_data(symbol, binance_interval, historical_data)
                gpt3_response = generate_gpt3_response(analysis_result)

                return render(request, 'cryptoapp/result.html', {'analysis_result': gpt3_response})
            except Exception as e:
                logger.error(f"Необработанная ошибка: {str(e)}")
                return render(request, 'cryptoapp/error.html')

        current_date = datetime.now().date()
        two_days_ago = current_date - timedelta(days=2)
        news_list = News.objects.filter(pub_date__gte=two_days_ago, pub_date__lte=current_date)
        return render(request, 'cryptoapp/index.html', {'news_list': news_list})

    @classmethod
    def analyze_crypto_view(cls, request):
        """
        Представление для анализа криптовалюты, используется для маршрута analyze_crypto.

        :param cls: Класс CryptoAnalyzer.
        :param request: Запрос от пользователя.
        :return: HTTP-ответ с результатами анализа.
        """
        crypto_analyzer = cls()
        return crypto_analyzer.analyze_crypto(request)


class AuthManager(View):
    """
    Базовый класс для управления аутентификацией.
    """
    def process_request(self, request):
        pass

    def get(self, request):
        return self.process_request(request)

    def post(self, request):
        return self.process_request(request)


class RegistrationManager(AuthManager):
    """
    Класс для управления регистрацией пользователей.
    Наследует функциональность из базового класса AuthManager.
    """

    def process_request(self, request):
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    if user is not None:
                        login(request, user)
                        logger.info("Пользователь успешно зарегистрирован и вошел в систему.")
                    return redirect('analyze_crypto')
                except Exception as e:
                    logger.error(f"Ошибка при регистрации пользователя: {str(e)}")
        else:
            form = CustomUserCreationForm()
        return render(request, 'cryptoapp/register.html', {'form': form})


class LoginManager(AuthManager):
    """
    Класс для управления входом пользователей в систему.
    Наследует функциональность из базового класса AuthManager.
    """

    def process_request(self, request):
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                try:
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password')
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        logger.info("Пользователь успешно вошел в систему.")
                        return redirect('analyze_crypto')
                except Exception as e:
                    logger.error(f"Ошибка при входе пользователя: {str(e)}")
        else:
            form = AuthenticationForm()
        return render(request, 'cryptoapp/login.html', {'form': form})


class LogoutManager(AuthManager):
    """
    Класс для управления выходом пользователей из системы.
    Наследует функциональность из базового класса AuthManager.
    """

    def process_request(self, request):
        try:
            logout(request)
            logger.info("Пользователь успешно вышел из системы.")
        except Exception as e:
            logger.error(f"Ошибка при выходе пользователя: {str(e)}")
        return redirect('analyze_crypto')


def about(request):
    """
    Представление для отображения страницы "О нас".
    """
    return render(request, 'cryptoapp/about.html')
