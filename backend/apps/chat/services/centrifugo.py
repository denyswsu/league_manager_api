import json

import requests
from requests.adapters import HTTPAdapter, Retry
import logging

from django.conf import settings


def broadcast(broadcast_payload: dict):
    """
    Using Centrifugo HTTP API is the simplest way to send real-time message, and usually
    it provides the best latency. The trade-off here is that error here may result in
    lost real-time event. Depending on the application requirements this may be fine or not.

    params:
    - broadcast_payload: A dictionary containing the data to be broadcasted.
        {
            'channels': channels,  # A list of channels to broadcast the message to.
            'data': {
                'type': 'user_left',  # The type of the message.
                'body': body  # The data to be broadcast.
            },
            'idempotency_key': f'user_left_{pk}'  # A unique key to prevent duplicate messages.
        }
    """
    session = requests.Session()
    retries = Retry(total=1, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    try:
        session.post(
            "http://centrifugo:8000/api/broadcast",
            data=json.dumps(broadcast_payload),
            headers={
                'Content-type': 'application/json',
                'X-API-Key': settings.CENTRIFUGO_HTTP_API_KEY,
                'X-Centrifugo-Error-Mode': 'transport'
            }
        )
    except requests.exceptions.RequestException as e:
        logging.error(e)
