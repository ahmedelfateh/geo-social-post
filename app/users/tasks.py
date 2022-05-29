import logging
import json
from django.conf import settings
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from app.utils.test_helper import mock_validate_email


_logger = logging.getLogger(__name__)


def validate_email(email):

    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504, 422],
        method_whitelist=["HEAD", "GET", "OPTIONS"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    if settings.DEPLOYMENT == "TEST":
        return mock_validate_email(email)

    try:
        resp = http.get(
            f"https://emailvalidation.abstractapi.com/v1/?api_key={settings.ABSTRACT_API_KEY_EMAIL}&email={email}"
        )
        return json.loads(resp.content).get("deliverability")
    except Exception as ex:
        print(ex)
        _logger.exception(ex)
