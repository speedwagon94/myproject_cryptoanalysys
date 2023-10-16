import os
from celery.schedules import crontab
from celery import Celery


# Установка переменной окружения DJANGO_SETTINGS_MODULE для настройки Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptoanalysys.settings')

# Создание экземпляра Celery.
app = Celery('cryptoanalysys')

# Загрузка настроек Celery из настроек Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач (tasks) в приложении.
app.autodiscover_tasks()

# Настройка расписания для Celery Beat.
app.conf.beat_schedule = {
    'parse-and-save-news': {
        'task': 'cryptoapp.tasks.parse_and_save_news',
        'schedule': crontab(minute=0, hour=0),
    },
}
