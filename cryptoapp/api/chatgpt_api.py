import openai
import os
from dotenv import load_dotenv


# Загрузка настроек из переменных окружения
load_dotenv()

api_key_gpt = os.getenv('API_KEY_GPT')


def get_gpt3_analysis(prompt):
    """
    Получает анализ от GPT-3 на основе заданного текстового запроса.

    :param prompt: Текстовый запрос для GPT-3.
    :return: Результат анализа, сгенерированный GPT-3.
    """
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'Вы: ' + prompt},
        ]
    )

    analysis = response['choices'][0]['message']['content'].strip()

    return analysis


def generate_gpt3_response(analysis_result):
    """
    Генерирует ответ с использованием GPT-3 на основе результата анализа.

    :param analysis_result: Результат анализа данных криптовалюты.
    :return: Сгенерированный ответ GPT-3.
    """
    openai.api_key = api_key_gpt
    prompt = f'Прими роль трейдера с большим стажем. Ты опытный трейдер и аналитик. ' \
             f'Твоя цель: Помогать новичкам торговать. Сделай анализ пары криптовалют.' \
             f'проведи анализ, прогноз, на какой сумме можно покупать или продавать монету.' \
             f'Пиши цифрами для покупки и продажи монеты' \
             f'на этом временном интервале. пиши только анализ {analysis_result}'
    return get_gpt3_analysis(prompt)
