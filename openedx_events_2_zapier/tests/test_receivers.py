"""This file contains all test for the receivers.py file.

Classes:
    EventsToolingTest: Test events tooling.
"""
import datetime
from unittest.mock import patch

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
from openedx_events.learning.signals import (
    COURSE_ENROLLMENT_CREATED,
    PERSISTENT_GRADE_SUMMARY_CHANGED,
    STUDENT_REGISTRATION_COMPLETED,
)

from openedx_events_2_zapier.receivers import (
    send_enrollment_data_to_webhook,
    send_persistent_grade_course_data_to_webhook,
    send_user_data_to_webhook,
)


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
    def test_receiver_called_after_event(self, request_mock):
        """
        Test that send_user_data_to_webhook is called the correct information after sending
        STUDENT_REGISTRATION_COMPLETED event.
        """
        expected_payload_subset = {
            "user_id": 39,
            "user_is_active": True,
            "user_pii_username": "test",
            "user_pii_email": "test@example.com",
            "user_pii_name": "Test Example",
            "event_metadata_event_type": self.metadata.event_type,
            "event_metadata_minorversion": self.metadata.minorversion,
            "event_metadata_source": self.metadata.source,
            "event_metadata_sourcehost": self.metadata.sourcehost,
            "event_metadata_sourcelib": list(self.metadata.sourcelib),
        }
        STUDENT_REGISTRATION_COMPLETED.connect(send_user_data_to_webhook)

        STUDENT_REGISTRATION_COMPLETED.send_event(
            user=self.user,
        )

        self.assertDictContainsSubset(
            expected_payload_subset,
            request_mock.post.call_args.args[1],
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
    def test_receiver_called_after_event(self, request_mock):
        """
        Test that send_user_data_to_webhook is called the correct information after sending
        COURSE_ENROLLMENT_CREATED event.
        """
        expected_payload_subset = {
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
            "event_metadata_event_type": self.metadata.event_type,
            "event_metadata_minorversion": self.metadata.minorversion,
            "event_metadata_source": self.metadata.source,
            "event_metadata_sourcehost": self.metadata.sourcehost,
            "event_metadata_sourcelib": list(self.metadata.sourcelib),
        }
        COURSE_ENROLLMENT_CREATED.connect(send_enrollment_data_to_webhook)

        COURSE_ENROLLMENT_CREATED.send_event(
            enrollment=self.enrollment,
        )

        self.assertDictContainsSubset(
            expected_payload_subset,
            request_mock.post.call_args.args[1],
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
                display_name="Demonstration Course"
            ),
            course_edited_timestamp=datetime.datetime(2021, 9, 21, 17, 40, 27),
            course_version="",
            grading_policy_hash="",
            percent_grade=80,
            letter_grade="Great",
            passed_timestamp=datetime.datetime(2021, 9, 21, 17, 40, 27)
        )
        self.metadata = EventsMetadata(
            event_type="org.openedx.learning.course.persistent_grade_summary.changed.v1",
            minorversion=0,
        )

    @patch("openedx_events_2_zapier.receivers.requests")
    def test_receiver_called_after_event(self, request_mock):
        """
        Test that send_persistent_grade_course_data_to_webhook is called the correct information after sending
        COURSE_ENROLLMENT_CREATED event.
        """
        expected_payload_subset = {
            "grade_user_id": 42,
            "grade_course_course_key": "course-v1:edX+100+2021",
            "grade_course_display_name": "Demonstration Course",
            "grade_course_edited_timestamp": datetime.datetime(2021, 9, 21, 17, 40, 27),
            "grade_course_version": "",
            "grade_grading_policy_hash": "",
            "grade_percent_grade": 80,
            "grade_letter_grade": "Great",
            "grade_passed_timestamp": datetime.datetime(2021, 9, 21, 17, 40, 27),
            "event_metadata_event_type": self.metadata.event_type,
            "event_metadata_minorversion": self.metadata.minorversion,
            "event_metadata_source": self.metadata.source,
            "event_metadata_sourcehost": self.metadata.sourcehost,
            "event_metadata_sourcelib": list(self.metadata.sourcelib),
        }
        PERSISTENT_GRADE_SUMMARY_CHANGED.connect(send_persistent_grade_course_data_to_webhook)

        PERSISTENT_GRADE_SUMMARY_CHANGED.send_event(
            grade=self.grade,
        )

        self.assertDictContainsSubset(
            expected_payload_subset,
            request_mock.post.call_args.args[1],
        )
