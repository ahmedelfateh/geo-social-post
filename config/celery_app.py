import os
from django.conf import settings
import requests
import json
from datetime import date

from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("app")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


class BaseTaskWithRetry(app.Task):
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3}
    retry_backoff = 5
    retry_jitter = True


@app.task(bind=True, base=BaseTaskWithRetry)
def get_geo_data(self, user_id):
    from app.users.models import User

    user = User.objects.get(id=user_id)
    resp = requests.get(
        f"https://ipgeolocation.abstractapi.com/v1/?api_key={settings.ABSTRACT_API_KEY_IP}"
    )
    user.geo_data = json.loads(resp.content)
    user.save()


@app.task(bind=True, base=BaseTaskWithRetry)
def get_holiday(self, user_id):
    from app.users.models import User

    user = User.objects.get(id=user_id)
    country = user.geo_data.get("country_code")
    resp = requests.get(
        f"https://holidays.abstractapi.com/v1/?api_key={settings.ABSTRACT_API_KEY_HOLYDAY}&country={country}&year={date.today().year}&month={date.today().month}&day={date.today().day}"
    )
    # resp = requests.get(
    #     f"https://holidays.abstractapi.com/v1/?api_key={settings.ABSTRACT_API_KEY_HOLYDAY}&country={country}&year=2022&month=05&day=01"
    # )
    user.register_in_holiday = [x.get("name") for x in json.loads(resp.content)]
    user.save()
