"""
Where handlers for Open edX Events are defined.
"""
import attr
import requests

from django.conf import settings

from openedx_events_2_zapier.utils import flatten_dict, serialize_course_key


def send_user_data_to_webhook(**kwargs):
    """
    Handler that POST user's data after STUDENT_REGISTRATION_COMPLETED event is sent.

    The data sent to the webhook is, for example:
    {
        'user_id': 39,
        'user_is_active': True,
        'user_pii_username': 'test',
        'user_pii_email': 'test@example.com',
        'user_pii_name': 'test',
        'event_metadata_id': UUID('b1be2fac-1af1-11ec-bdf4-0242ac12000b'),
        'event_metadata_event_type': 'org.openedx.learning.student.registration.completed.v1',
        'event_metadata_minorversion': 0,
        'event_metadata_source': 'openedx/lms/web',
        'event_metadata_sourcehost': 'lms.devstack.edx',
        'event_metadata_time': datetime.datetime(2021, 9, 21, 15, 36, 31, 311506),
        'event_metadata_sourcelib': [0, 6, 0]
    }

    This format is convenient for Zapier to read.
    """
    user_info = attr.asdict(kwargs.get("user"))
    event_metadata = attr.asdict(kwargs.get("metadata"))
    zapier_payload = {
        "user": user_info,
        "event_metadata": event_metadata,
    }
    requests.post(
        settings.ZAPIER_REGISTRATION_WEBHOOK,
        flatten_dict(zapier_payload),
    )
    )
