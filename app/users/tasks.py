from django.conf import settings
import requests
from app.utils.retry import retry


@retry
def validate_email(email):
    resp = requests.get(
        f"https://emailvalidation.abstractapi.com/v1/?api_key={settings.ABSTRACT_API_KEY_EMAIL}&email={email}"
    )
    print(resp.status_code)
    print(resp.content)
    return resp
