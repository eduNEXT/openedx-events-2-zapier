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


def send_enrollment_data_to_webhook(**kwargs):
    """
    Handler that POST enrollment's data after COURSE_ENROLLMENT_CREATED event is sent.

    The data sent to the webhook is, for example:
    {
        'enrollment_user_id': 42,
        'enrollment_user_is_active': True,
        'enrollment_user_pii_username': 'majo5',
        'enrollment_user_pii_email': 'majo5@example.com',
        'enrollment_user_pii_name': 'majo5',
        'enrollment_course_course_key': 'course-v1:edX+100+2021',
        'enrollment_course_display_name':'Demonstration Course',
        'enrollment_course_start': None,
        'enrollment_course_end': None,
        'enrollment_mode':
        'audit', 'enrollment_is_active': True,
        'enrollment_creation_date': datetime.datetime(2021, 9, 21, 17, 40, 27, 401427, tzinfo=<UTC>),
        'enrollment_created_by': None,
        'event_metadata_id': UUID('02672f60-1b03-11ec-953b-0242ac12000b'),
        'event_metadata_event_type': 'org.openedx.learning.course.enrollment.created.v1',
        'event_metadata_minorversion': 0,
        'event_metadata_source': 'openedx/lms/web',
        'event_metadata_sourcehost': 'lms.devstack.edx',
        'event_metadata_time': datetime.datetime(2021, 9, 21, 17, 40, 28, 81160),
        'event_metadata_sourcelib': [0, 6, 0]
    }
    This format is convenient for Zapier to read.
    """
    enrollment_info = attr.asdict(kwargs.get("enrollment"), value_serializer=serialize_course_key)
    event_metadata = attr.asdict(kwargs.get("metadata"))
    zapier_payload = {
        "enrollment": enrollment_info,
        "event_metadata": event_metadata,
    }
    requests.post(
        settings.ZAPIER_ENROLLMENT_WEBHOOK,
        flatten_dict(zapier_payload),
    )
