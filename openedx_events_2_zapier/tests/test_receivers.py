"""This file contains all test for the receivers.py file.

Classes:
    EventsToolingTest: Test events tooling.
"""
import datetime
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from opaque_keys.edx.keys import CourseKey
from openedx_events.data import EventsMetadata
from openedx_events.learning.data import CourseData, CourseEnrollmentData, UserData, UserPersonalData

from openedx_events_2_zapier.receivers import send_enrollment_data_to_webhook, send_user_data_to_webhook


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

    @patch("openedx_events_2_zapier.receivers.requests")
    def test_send_payload_success(self, request_mock):
        """
        Test that send_user_data_to_webhook sends the correct information to Zapier webhook.
        """
        expected_payload = {
            "user_id": 39,
            "user_is_active": True,
            "user_pii_username": "test",
            "user_pii_email": "test@example.com",
            "user_pii_name": "Test Example",
            "event_metadata_id": self.metadata.id,
            "event_metadata_event_type": self.metadata.event_type,
            "event_metadata_minorversion": self.metadata.minorversion,
            "event_metadata_source": self.metadata.source,
            "event_metadata_sourcehost": self.metadata.sourcehost,
            "event_metadata_time": self.metadata.time,
            "event_metadata_sourcelib": list(self.metadata.sourcelib),
        }

        send_user_data_to_webhook(user=self.user, metadata=self.metadata)

        request_mock.post.assert_called_once_with(
            settings.ZAPIER_REGISTRATION_WEBHOOK,
            expected_payload,
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
            creation_date=datetime.datetime(2021, 9, 21, 17, 40, 27),
        )
        self.metadata = EventsMetadata(
            event_type="org.openedx.learning.course.enrollment.created.v1",
            minorversion=0,
        )

    @patch("openedx_events_2_zapier.receivers.requests")
    def test_send_payload_success(self, request_mock):
        """
        Test that send_enrollment_data_to_webhook sends the correct information to Zapier webhook.
        """
        expected_payload = {
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
            "enrollment_creation_date": datetime.datetime(2021, 9, 21, 17, 40, 27),
            "enrollment_created_by": None,
            "event_metadata_id": self.metadata.id,
            "event_metadata_event_type": self.metadata.event_type,
            "event_metadata_minorversion": self.metadata.minorversion,
            "event_metadata_source": self.metadata.source,
            "event_metadata_sourcehost": self.metadata.sourcehost,
            "event_metadata_time": self.metadata.time,
            "event_metadata_sourcelib": list(self.metadata.sourcelib),
        }

        send_enrollment_data_to_webhook(enrollment=self.enrollment, metadata=self.metadata)

        request_mock.post.assert_called_once_with(
            settings.ZAPIER_ENROLLMENT_WEBHOOK,
            expected_payload,
        )
