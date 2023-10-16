import requests
from bs4 import BeautifulSoup
from cryptoapp.models import News
from datetime import datetime, date, timedelta
from celery import shared_task
import logging


logger = logging.getLogger(__name__)


# Задача Celery для парсинга и сохранения новостей.
@shared_task
def parse_and_save_news():
    # Загрузка страницы с новостями
    url = 'https://forklog.com/news'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешный HTTP-запрос
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Парсинг новостей
    news_elements = soup.select('div.category_page_grid > div[data-entity="recent"]')

    current_date = date.today()  # Текущая дата без времени
    two_days_ago = current_date - timedelta(days=2)

    for element in news_elements:
        try:
            title = element.select_one('div.text_blk p').text.strip()
            content = element.select_one('div.text_blk span.post_excerpt').text.strip()
            pub_date_str = element.select_one('div.post_meta span.post_date').text.strip()

            # Преобразование текстовой даты в дату без времени
            pub_date = datetime.strptime(pub_date_str, '%d.%m.%Y').date()

            # Проверка, существует ли новость с таким заголовком и датой, и дата равна текущей
            if not News.objects.filter(title=title, pub_date=pub_date).exists() and two_days_ago <= pub_date <= current_date:
                News.objects.create(title=title, content=content, pub_date=pub_date)
                logger.info(f"Сохранена новость: {title}")
            else:
                logger.info(f"Новость уже существует или не соответствует текущей дате: {title}")
        except Exception as e:
            logger.error(f"Ошибка при парсинге новости: {e}")
