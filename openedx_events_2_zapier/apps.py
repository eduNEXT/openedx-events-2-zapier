"""
openedx_events_2_zapier Django application initialization.
"""

from django.apps import AppConfig


class OpenedxEvents2ZapierConfig(AppConfig):
    """
    Configuration for the openedx_events_2_zapier Django application.
    """

    name = "openedx_events_2_zapier"

    plugin_app = {
        "settings_config": {
            "lms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
                "production": {"relative_path": "settings.production"},
            },
            "cms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
                "production": {"relative_path": "settings.production"},
            },
        },
    }

    def ready(self):
        """Perform initialization tasks required for the plugin."""
        from openedx_events_2_zapier import handlers  # pylint: disable=unused-import, import-outside-toplevel
