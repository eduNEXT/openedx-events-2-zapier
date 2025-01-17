"""
Where handlers for Open edX Events are defined.
"""

import logging
import requests
from attr import asdict
from django.conf import settings
from django.dispatch import receiver
from openedx_events.learning.signals import (
    COURSE_ENROLLMENT_CREATED,
    PERSISTENT_GRADE_SUMMARY_CHANGED,
    STUDENT_REGISTRATION_COMPLETED,
)

from openedx_events_2_zapier.utils import flatten_dict, serialize_course_key

ZAPIER_REQUEST_TIMEOUT = 5
log = logging.getLogger(__name__)


@receiver(STUDENT_REGISTRATION_COMPLETED)
def send_user_data_to_webhook(
    signal, sender, user, metadata, **kwargs  # pylint: disable=unused-argument
):
    """
    POST user's data after STUDENT_REGISTRATION_COMPLETED event is sent.

    The data sent to the webhook is, for example:

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

    This format is convenient for Zapier to read.
    """
    zapier_payload = {
        "user": asdict(user),
        "event_metadata": asdict(metadata),
    }
    requests.post(
        settings.ZAPIER_REGISTRATION_WEBHOOK,
        flatten_dict(zapier_payload),
        timeout=ZAPIER_REQUEST_TIMEOUT,
    )


@receiver(COURSE_ENROLLMENT_CREATED)
def send_enrollment_data_to_webhook(
    signal, sender, enrollment, metadata, **kwargs  # pylint: disable=unused-argument
):
    """
    POST enrollment's data after COURSE_ENROLLMENT_CREATED event is sent.

    Arguments:
        signal: The signal that was sent.
        sender: The sender of the signal.
        enrollment: The enrollment data.
        metadata: The metadata of the event.
        **kwargs: Additional keyword arguments.

    The data sent to the webhook is would look this:

    'enrollment_user_id': 42,
    'enrollment_user_is_active': True,
    'enrollment_user_pii_username': 'test',
    'enrollment_user_pii_email': 'test@example.com',
    'enrollment_user_pii_name': 'test',
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

    This format is convenient for Zapier to read.
    """
    zapier_payload = {
        "enrollment": asdict(enrollment, value_serializer=serialize_course_key),
        "event_metadata": asdict(metadata),
    }

    requests.post(
        settings.ZAPIER_ENROLLMENT_WEBHOOK,
        flatten_dict(zapier_payload),
        timeout=ZAPIER_REQUEST_TIMEOUT,
    )


@receiver(PERSISTENT_GRADE_SUMMARY_CHANGED)
def send_persistent_grade_course_data_to_webhook(
    signal, sender, grade, metadata, **kwargs  # pylint: disable=unused-argument
):
    """
    POST user's data after PERSISTENT_GRADE_SUMMARY_CHANGED event is sent.

    The data sent to the webhook would look like this:

    'grade_user_id': 42,
    'grade_course_course_key': 'course-v1:edX+100+2021',
    'grade_course_display_name': 'Demonstration Course',
    'grade_course_edited_timestamp': datetime.datetime(2021, 9, 21, 17, 40, 27),
    'grade_course_version': '',
    'grade_grading_policy_hash': '',
    'grade_percent_grade': 80,
    'grade_letter_grade': 'Great',
    'grade_passed_timestamp': datetime.datetime(2021, 9, 21, 17, 40, 27),
    'event_metadata_id': UUID('b1be2fac-1af1-11ec-bdf4-0242ac12000b'),
    'event_metadata_event_type': 'org.openedx.learning.student.registration.completed.v1',
    'event_metadata_minorversion': 0,
    'event_metadata_source': 'openedx/lms/web',
    'event_metadata_sourcehost': 'lms.devstack.edx',
    'event_metadata_time': datetime.datetime(2021, 9, 21, 15, 36, 31, 311506),
    'event_metadata_sourcelib': [0, 6, 0]

    This format is convenient for Zapier to read.
    """
    zapier_payload = {
        "grade": asdict(grade, value_serializer=serialize_course_key),
        "event_metadata": asdict(metadata),
    }

    requests.post(
        settings.ZAPIER_PERSISTENT_GRADE_COURSE_WEBHOOK,
        flatten_dict(zapier_payload),
        timeout=ZAPIER_REQUEST_TIMEOUT,
    )
