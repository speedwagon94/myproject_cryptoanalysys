import os
from binance.client import Client
from dotenv import load_dotenv


# Загрузка настроек из переменных окружения
load_dotenv()

api_key_binance = os.getenv('API_KEY_BINANCE')
api_secret_binance = os.getenv('API_SECRET_BINANCE')


def get_binance_client():
    """Создает и возвращает клиента Binance API."""
    return Client(api_key_binance, api_secret_binance)


def fetch_historical_data(client, symbol, binance_interval):
    """Получает исторические данные о криптовалюте с Binance."""
    return client.get_klines(symbol=symbol, interval=binance_interval)


# Словарь, который сопоставляет строковые интервалы времени
# с соответствующими константами из библиотеки Binance API.
interval_mapping = {
        "1m": Client.KLINE_INTERVAL_1MINUTE,
        "3m": Client.KLINE_INTERVAL_3MINUTE,
        "5m": Client.KLINE_INTERVAL_5MINUTE,
        "15m": Client.KLINE_INTERVAL_15MINUTE,
        "30m": Client.KLINE_INTERVAL_30MINUTE,
        "1h": Client.KLINE_INTERVAL_1HOUR,
        "2h": Client.KLINE_INTERVAL_2HOUR,
        "4h": Client.KLINE_INTERVAL_4HOUR,
        "6h": Client.KLINE_INTERVAL_6HOUR,
        "8h": Client.KLINE_INTERVAL_8HOUR,
        "12h": Client.KLINE_INTERVAL_12HOUR,
        "1d": Client.KLINE_INTERVAL_1DAY,
        "3d": Client.KLINE_INTERVAL_3DAY,
        "1w": Client.KLINE_INTERVAL_1WEEK,
        "1M": Client.KLINE_INTERVAL_1MONTH,
        }


def analyze_data(symbol, interval, historical_data):
    """
    Анализирует исторические данные криптовалюты для определения текущего тренда и уровней поддержки и сопротивления.

    :param symbol: Символ (пара монет).
    :param interval: Интервал времени.
    :param historical_data: Список исторических данных о криптовалюте.
    :return: Словарь с результатами анализа, включая тренд, цены, средний объем и уровни поддержки и сопротивления.
    """
    # Извлекаем цены закрытия, максимальные и минимальные цены из исторических данных
    closing_prices = [float(entry[4]) for entry in historical_data]
    high_prices = [float(entry[2]) for entry in historical_data]
    low_prices = [float(entry[3]) for entry in historical_data]

    # Определяем текущий тренд на основе цен закрытия
    trend = None
    if closing_prices[-1] > closing_prices[0]:
        trend = "uptrend"  # Восходящий тренд
    elif closing_prices[-1] < closing_prices[0]:
        trend = "downtrend"  # Нисходящий тренд
    else:
        trend = "sideways trend"  # Боковой тренд

    # Определяем уровни поддержки и сопротивления
    support_level = min(low_prices)
    resistance_level = max(high_prices)

    # Вычисляем средний объем торгов
    volumes = [float(entry[5]) for entry in historical_data]
    average_volume = sum(volumes) / len(volumes)

    # Создаем словарь с результатами анализа
    analysis_data = {
        "trend": trend,
        "start_price": closing_prices[0],
        "current_price": closing_prices[-1],
        "average_volume": average_volume,
        "support_level": support_level,
        "resistance_level": resistance_level
    }

    return analysis_data
