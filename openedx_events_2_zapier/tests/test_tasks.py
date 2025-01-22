"""This file contains all test for the tasks.py file."""

from datetime import datetime, timezone
from unittest.mock import patch

from attr import asdict
from ddt import data, ddt, unpack
from django.test import TestCase
from opaque_keys.edx.keys import CourseKey
from openedx_events.data import EventsMetadata
from openedx_events.learning.data import (
    CourseData,
    CourseEnrollmentData,
    PersistentCourseGradeData,
    UserData,
    UserPersonalData,
)
from requests.exceptions import RequestException

from openedx_events_2_zapier.tasks import send_data_to_zapier
from openedx_events_2_zapier.utils import serialize_course_key


@ddt
class SendDataToZapierTaskTest(TestCase):
    """
    Tests the registration receiver sends the correct information to Zapier.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.metadata = EventsMetadata(
            event_type="org.openedx.learning.student.registration.completed.v1",
            minorversion=0,
            source="openedx/lms/web",
            sourcehost="lms.devstack.edx",
            time=datetime(2021, 9, 21, 15, 36, 31, 311506, tzinfo=timezone.utc),
            sourcelib=(0, 6, 0),
        )

    @data(
        (
            "https://webhook.site",
            {
                "user": asdict(
                    UserData(
                        pii=UserPersonalData(
                            username="test",
                            email="test@example.com",
                            name="Test Example",
                        ),
                        id=39,
                        is_active=True,
                    )
                ),
                "event_metadata": asdict(
                    EventsMetadata(
                        event_type="org.openedx.learning.student.registration.completed.v1",
                        minorversion=0,
                        source="openedx/lms/web",
                        sourcehost="lms.devstack.edx",
                        time=datetime(
                            2021, 9, 21, 15, 36, 31, 311506, tzinfo=timezone.utc
                        ),
                        sourcelib=(0, 6, 0),
                    )
                ),
            },
            {
                "user_id": 39,
                "user_is_active": True,
                "user_pii_username": "test",
                "user_pii_email": "test@example.com",
                "user_pii_name": "Test Example",
                "event_metadata_event_type": "org.openedx.learning.student.registration.completed.v1",
                "event_metadata_minorversion": 0,
                "event_metadata_source": "openedx/lms/web",
                "event_metadata_sourcehost": "lms.devstack.edx",
                "event_metadata_sourcelib": [0, 6, 0],
            },
        ),
        (
            "https://webhook.site",
            {
                "enrollment": asdict(
                    CourseEnrollmentData(
                        user=UserData(
                            pii=UserPersonalData(
                                username="test",
                                email="test@example.com",
                                name="Test Example",
                            ),
                            id=42,
                            is_active=True,
                        ),
                        course=CourseData(
                            course_key=CourseKey.from_string("course-v1:edX+100+2021"),
                            display_name="Demonstration Course",
                        ),
                        mode="audit",
                        is_active=True,
                        creation_date=datetime(2021, 9, 21, 17, 40, 27),
                    ),
                    value_serializer=serialize_course_key,
                ),
                "event_metadata": asdict(
                    EventsMetadata(
                        event_type="org.openedx.learning.course.enrollment.created.v1",
                        minorversion=0,
                        source="openedx/lms/web",
                        sourcehost="lms.devstack.edx",
                        time=datetime(
                            2021, 9, 21, 15, 36, 31, 311506, tzinfo=timezone.utc
                        ),
                        sourcelib=(0, 6, 0),
                    )
                ),
            },
            {
                "enrollment_user_id": 42,
                "enrollment_user_is_active": True,
                "enrollment_user_pii_username": "test",
                "enrollment_user_pii_email": "test@example.com",
                "enrollment_user_pii_name": "Test Example",
                "enrollment_course_course_key": "course-v1:edX+100+2021",
                "enrollment_course_display_name": "Demonstration Course",
                "enrollment_course_start": None,
                "enrollment_course_end": None,
                "enrollment_mode": "audit",
                "enrollment_is_active": True,
                "enrollment_creation_date": datetime(2021, 9, 21, 17, 40, 27),
                "enrollment_created_by": None,
                "event_metadata_event_type": "org.openedx.learning.course.enrollment.created.v1",
                "event_metadata_minorversion": 0,
                "event_metadata_source": "openedx/lms/web",
                "event_metadata_sourcehost": "lms.devstack.edx",
                "event_metadata_sourcelib": [0, 6, 0],
            },
        ),
        (
            "https://webhook.site",
            {
                "grade": asdict(
                    PersistentCourseGradeData(
                        user_id=42,
                        course=CourseData(
                            course_key=CourseKey.from_string("course-v1:edX+100+2021"),
                            display_name="Demonstration Course",
                        ),
                        course_edited_timestamp=datetime(2021, 9, 21, 17, 40, 27),
                        course_version="",
                        grading_policy_hash="",
                        percent_grade=80,
                        letter_grade="Great",
                        passed_timestamp=datetime(2021, 9, 21, 17, 40, 27),
                    ),
                    value_serializer=serialize_course_key,
                ),
                "event_metadata": asdict(
                    EventsMetadata(
                        event_type="org.openedx.learning.course.persistent_grade_summary.changed.v1",
                        minorversion=0,
                        source="openedx/lms/web",
                        sourcehost="lms.devstack.edx",
                        time=datetime(
                            2021, 9, 21, 15, 36, 31, 311506, tzinfo=timezone.utc
                        ),
                        sourcelib=(0, 6, 0),
                    )
                ),
            },
            {
                "grade_user_id": 42,
                "grade_course_course_key": "course-v1:edX+100+2021",
                "grade_course_display_name": "Demonstration Course",
                "grade_course_edited_timestamp": datetime(2021, 9, 21, 17, 40, 27),
                "grade_course_version": "",
                "grade_grading_policy_hash": "",
                "grade_percent_grade": 80,
                "grade_letter_grade": "Great",
                "grade_passed_timestamp": datetime(2021, 9, 21, 17, 40, 27),
                "event_metadata_event_type": "org.openedx.learning.course.persistent_grade_summary.changed.v1",
                "event_metadata_minorversion": 0,
                "event_metadata_source": "openedx/lms/web",
                "event_metadata_sourcehost": "lms.devstack.edx",
                "event_metadata_sourcelib": [0, 6, 0],
            },
        ),
    )
    @unpack
    @patch("openedx_events_2_zapier.tasks.post")
    def test_send_data_to_zapier_task_success(
        self, zap_url, payload, expected_payload, post_mock
    ):
        """
        Test that send_data_to_zapier is making the correct request to Zapier.

        Expected Behavior:
            - The request.post method is called with the correct arguments.
        """
        send_data_to_zapier(zap_url, payload)  # pylint: disable=no-value-for-parameter

        self.assertDictContainsSubset(
            expected_payload,
            post_mock.call_args.args[1],
        )
        self.assertEqual(
            post_mock.call_args.kwargs["timeout"],
            5,
        )

    @patch("openedx_events_2_zapier.tasks.post")
    def test_send_data_to_zapier_task_failure(self, post_mock):
        """
        Test that send_data_to_zapier raises an exception when the request fails.

        Expected Behavior:
            - The function raises an exception.
        """
        post_mock.side_effect = RequestException

        with self.assertRaises(RequestException):
            send_data_to_zapier(  # pylint: disable=no-value-for-parameter
                "https://webhook.site", {}
            )

        post_mock.assert_called_once()
        self.assertEqual(
            post_mock.call_args.kwargs["timeout"],
            5,
        )
