"""This file contains all test for the handlers.py file."""

from datetime import datetime
from unittest.mock import patch

from attr import asdict
from django.test import TestCase, override_settings
from opaque_keys.edx.keys import CourseKey
from openedx_events.data import EventsMetadata
from openedx_events.learning.data import (
    CourseData,
    CourseEnrollmentData,
    PersistentCourseGradeData,
    UserData,
    UserPersonalData,
)
from openedx_events.learning.signals import (
    COURSE_ENROLLMENT_CREATED,
    PERSISTENT_GRADE_SUMMARY_CHANGED,
    STUDENT_REGISTRATION_COMPLETED,
)

from openedx_events_2_zapier.handlers import (
    send_enrollment_data_to_webhook,
    send_persistent_grade_course_data_to_webhook,
    send_user_data_to_webhook,
)
from openedx_events_2_zapier.utils import serialize_course_key


class RegistrationCompletedReceiverTest(TestCase):
    """
    Tests the registration receiver sends the correct information to Zapier.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.user = UserData(
            pii=UserPersonalData(
                username="test",
                email="test@example.com",
                name="Test Example",
            ),
            id=39,
            is_active=True,
        )
        self.metadata = EventsMetadata(
            event_type="org.openedx.learning.student.registration.completed.v1",
            minorversion=0,
        )

    @override_settings(ZAPIER_REGISTRATION_WEBHOOK="https://webhook.site")
    @patch("openedx_events_2_zapier.handlers.send_data_to_zapier")
    def test_receiver_called_after_event(self, task_mock):
        """
        Test that send_user_data_to_webhook is called the correct information after sending
        STUDENT_REGISTRATION_COMPLETED event.

        Expected Behavior:
            - The task is called with the correct URL and payload.
        """
        expected_payload = {
            "user": asdict(self.user),
            "event_metadata": asdict(self.metadata),
        }
        STUDENT_REGISTRATION_COMPLETED.connect(send_user_data_to_webhook)

        STUDENT_REGISTRATION_COMPLETED.send_event(
            user=self.user,
        )

        task_mock.delay.assert_called_once()
        self.assertDictContainsSubset(
            expected_payload["user"],
            task_mock.delay.call_args[0][1]["user"],
        )
        self.assertEqual(
            task_mock.delay.call_args[0][1]["event_metadata"],
            {
                **expected_payload["event_metadata"],
                "id": task_mock.delay.call_args[0][1]["event_metadata"]["id"],
                "time": task_mock.delay.call_args[0][1]["event_metadata"]["time"],
            },
        )


class EnrollmentCreatedReceiverTest(TestCase):
    """
    Tests the registration receiver sends the correct information to Zapier.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.enrollment = CourseEnrollmentData(
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
        )
        self.metadata = EventsMetadata(
            event_type="org.openedx.learning.course.enrollment.created.v1",
            minorversion=0,
        )

    @override_settings(ZAPIER_ENROLLMENT_WEBHOOK="https://webhook.site")
    @patch("openedx_events_2_zapier.handlers.send_data_to_zapier")
    def test_receiver_called_after_event(self, task_mock):
        """
        Test that send_user_data_to_webhook is called the correct information after sending
        COURSE_ENROLLMENT_CREATED event.

        Expected Behavior:
            - The task is called with the correct URL and payload.
        """
        expected_payload = {
            "enrollment": asdict(
                self.enrollment, value_serializer=serialize_course_key
            ),
            "event_metadata": asdict(self.metadata),
        }
        COURSE_ENROLLMENT_CREATED.connect(send_enrollment_data_to_webhook)

        COURSE_ENROLLMENT_CREATED.send_event(
            enrollment=self.enrollment,
        )

        task_mock.delay.assert_called_once()
        self.assertEqual(
            expected_payload["enrollment"],
            task_mock.delay.call_args[0][1]["enrollment"],
        )
        self.assertEqual(
            task_mock.delay.call_args[0][1]["event_metadata"],
            {
                **expected_payload["event_metadata"],
                "id": task_mock.delay.call_args[0][1]["event_metadata"]["id"],
                "time": task_mock.delay.call_args[0][1]["event_metadata"]["time"],
            },
        )


class PersistentGradeEventsTest(TestCase):
    """
    Test that send_persistent_grade_course_data_to_webhook is called the correct information after sending
    COURSE_ENROLLMENT_CREATED event.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.grade = PersistentCourseGradeData(
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
        )
        self.metadata = EventsMetadata(
            event_type="org.openedx.learning.course.persistent_grade_summary.changed.v1",
            minorversion=0,
        )

    @override_settings(ZAPIER_PERSISTENT_GRADE_COURSE_WEBHOOK="https://webhook.site")
    @patch("openedx_events_2_zapier.handlers.send_data_to_zapier")
    def test_receiver_called_after_event(self, task_mock):
        """
        Test that send_persistent_grade_course_data_to_webhook is called the correct information after sending
        COURSE_ENROLLMENT_CREATED event.

        Expected Behavior:
            - The task is called with the correct URL and payload.
        """
        expected_payload = {
            "grade": asdict(self.grade, value_serializer=serialize_course_key),
            "event_metadata": asdict(self.metadata),
        }
        PERSISTENT_GRADE_SUMMARY_CHANGED.connect(
            send_persistent_grade_course_data_to_webhook
        )

        PERSISTENT_GRADE_SUMMARY_CHANGED.send_event(
            grade=self.grade,
        )

        task_mock.delay.assert_called_once()
        self.assertEqual(
            expected_payload["grade"],
            task_mock.delay.call_args[0][1]["grade"],
        )
        self.assertEqual(
            task_mock.delay.call_args[0][1]["event_metadata"],
            {
                **expected_payload["event_metadata"],
                "id": task_mock.delay.call_args[0][1]["event_metadata"]["id"],
                "time": task_mock.delay.call_args[0][1]["event_metadata"]["time"],
            },
        )
