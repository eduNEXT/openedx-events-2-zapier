"""
openedx_events_2_zapier Django application initialization.
"""

from django.apps import AppConfig


class OpenedxEventsSamplesConfig(AppConfig):
    """
    Configuration for the openedx_events_2_zapier Django application.
    """

    name = 'openedx_events_2_zapier'

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'test': {'relative_path': 'settings.test'},
                'production': {'relative_path': 'settings.production'},
            },
            'cms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'test': {'relative_path': 'settings.test'},
                'production': {'relative_path': 'settings.production'},
            },
        },
        'signals_config': {
            'lms.djangoapp': {
                'relative_path': 'receivers',
                'receivers': [
                    {
                        'receiver_func_name': 'send_user_data_to_webhook',
                        'signal_path': 'openedx_events.learning.signals.STUDENT_REGISTRATION_COMPLETED',
                    },
                    {
                        'receiver_func_name': 'send_enrollment_data_to_webhook',
                        'signal_path': 'openedx_events.learning.signals.COURSE_ENROLLMENT_CREATED',
                    },
                ],
            }
        },
    }
