"""
Production Django settings for eox_hooks project.
"""


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.ZAPIER_REGISTRATION_WEBHOOK = getattr(settings, 'ENV_TOKENS', {}).get(
        'ZAPIER_REGISTRATION_WEBHOOK',
        settings.ZAPIER_REGISTRATION_WEBHOOK
    )
    settings.ZAPIER_ENROLLMENT_WEBHOOK = getattr(settings, 'ENV_TOKENS', {}).get(
        'ZAPIER_ENROLLMENT_WEBHOOK',
        settings.ZAPIER_ENROLLMENT_WEBHOOK
    )
