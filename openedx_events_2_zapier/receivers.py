"""
Where handlers for Open edX Events are defined.
"""
import attr
import requests

from django.conf import settings


def send_user_data_to_webhook(**kwargs):
    """
    Handler that POST user's data after STUDENT_REGISTRATION_COMPLETED event is sent.

    The data sent to the webhook is, for example:
    {
        "user":
            {
                'id': 25,
                'is_active': True,
                'pii':
                {
                    'username':'test_9',
                    'email': 'test_9@example.com',
                    'name': 'test_9'
                }
            },
        "event_information":
            {
                'id': UUID('e5797634-166f-11ec-9b48-0242ac13000b'),
                'event_type': 'org.openedx.learning.student.registration.completed.v1',
                'minorversion': 0,
                'source': 'openedx/lms/web',
                'sourcehost': 'lms.devstack.edx',
                'time': datetime.datetime(2021, 9, 15, 21, 57, 18, 876654),
                'sourcelib': [0, 6, 0]
            }
    }
    """
    user_info = attr.asdict(kwargs.get("user"))
    event_metadata = attr.asdict(kwargs.get("metadata"))
    requests.post(
        settings.ZAPIER_REGISTRATION_WEBHOOK,
        {
            "user": user_info,
            "event_metadata": event_metadata,
        }
    )
