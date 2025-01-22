"""Celery tasks for sending data to Zapier or another webhook."""

import logging

from celery import shared_task
from requests import exceptions, post

from openedx_events_2_zapier.utils import flatten_dict

ZAPIER_REQUEST_TIMEOUT = 5
ZAPIER_RETRY_COUNTDOWN = 3
log = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(exceptions.RequestException,),
    retry_backoff=True,
    retry_kwargs={"max_retries": ZAPIER_RETRY_COUNTDOWN},
)
def send_data_to_zapier(self, zap_url, data):  # pylint: disable=unused-argument
    """
    Send data to Zapier using a webhook.

    Arguments:
        self: The task instance.
        zap_url: The URL of the Zapier webhook.
        data: The data to send to the webhook.
    """
    flattened_data = flatten_dict(data)
    try:
        log.info("Sending data to Zapier: %s", flattened_data)
        post(zap_url, flattened_data, timeout=ZAPIER_REQUEST_TIMEOUT)
    except exceptions.RequestException as e:
        log.error("Error sending data to Zapier: %s", e)
        raise
