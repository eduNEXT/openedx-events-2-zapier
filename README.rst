openedx-events-2-zapier
=============================

|ci-badge| |license-badge|

A ready-to-use repository demonstrating how to use Open edX Events for building workflows and automating integrations. It serves as a starting point for more advanced use cases. Explore `Real-Life Use Cases for Open edX Events`_ to see more complex implementations from the Open edX Community

This repository is currently being maintained by the eduNEXT team.

Overview
---------

This repository demonstrates how to connect Open edX registration, enrollment, and grade change events to external tools via Zapier, enabling easier automation workflows through this third-party service.

Open edX Events are a powerful feature that allows developers to listen to key events in the Open edX platform and trigger custom actions based on them. This can be useful for a variety of use cases, such as:

- Sending welcome emails to new users
- Logging new enrollments to external CRMs
- Triggering events like email follow-ups for grade updates

By sending key event data to Zapier, Open edX users can leverage the integration ecosystem of Zapier without additional development effort.

Features
---------

- **Event Handlers**: Listen to Open edX Events using Django signals and send data to Zapier.
- **Webhook Integration**: Send event data to Zapier webhooks for further processing.
- **Customizable**: Easily extend the repository to handle additional events or integrate with other services.
- **Ready-to-Use**: Install the package and configure webhooks to start sending events to Zapier.

Supported Events
-----------------

+-------------------------------------+------------------------------------------------------------+---------------------------------------------------------------------+
| **Event Name**                      | **Event Type**                                             | **Description**                                                     |
+=====================================+============================================================+=====================================================================+
| `STUDENT_REGISTRATION_COMPLETED`_   | org.openedx.learning.student.registration.completed.v1     | Triggered when a user completes registration in the LMS.            |
+-------------------------------------+------------------------------------------------------------+---------------------------------------------------------------------+
| `COURSE_ENROLLMENT_CREATED`_        | org.openedx.learning.course.enrollment.created.v1          | Triggered upon successful course enrollment.                        |
+-------------------------------------+------------------------------------------------------------+---------------------------------------------------------------------+
| `PERSISTENT_GRADE_SUMMARY_CHANGED`_ | org.openedx.learning.course.persistent_grade.summary.v1    | Triggered when a persistent grade summary is updated. This happens  |
|                                     |                                                            | when a grade changes in a course.                                   |
+-------------------------------------+------------------------------------------------------------+---------------------------------------------------------------------+

How Does it Work?
-----------------

Each of the above events is handled by Django Signal handlers. When these signals are emitted, they are intercepted by handlers defined in the repository, which transform and forward the event data to a `Zapier webhook`_.

Django Signal Handlers
~~~~~~~~~~~~~~~~~~~~~~

In the file `handlers.py`_, handlers listen to Django signals using the standard `receiver`_ decorator:

.. code-block:: python

    from django.dispatch import receiver
    from openedx_events.signals import STUDENT_REGISTRATION_COMPLETED

    @receiver(STUDENT_REGISTRATION_COMPLETED)
    def send_user_data_to_webhook(signal, sender, user, metadata, **kwargs):
        zapier_payload = {
            "user": asdict(user),
            "event_metadata": asdict(metadata),
        }
        requests.post(
            settings.ZAPIER_REGISTRATION_WEBHOOK,
            flatten_dict(zapier_payload),
            timeout=ZAPIER_REQUEST_TIMEOUT,
        )

- The ``receiver`` decorator listens to the ``STUDENT_REGISTRATION_COMPLETED`` signal.
- The handler function ``send_user_data_to_webhook`` extracts the user and metadata from the signal.
- The ``ZAPIER_REGISTRATION_WEBHOOK`` URL is configured as a Django settings by using a `Tutor plugin`_.
- The extracted data is formatted into a payload and sent to the Zapier webhook for further processing.

App Configuration (`apps.py`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Django app is configured using an `AppConfig` to automatically register handlers on startup.

.. code-block:: python

    class OpenedxEvents2ZapierConfig(AppConfig):
        name = "openedx_events_2_zapier"

        def ready(self):
            from openedx_events_2_zapier import handlers

Usage
-----

To use this plugin, follow these steps:

1. Install the plugin in your Open edX image using Tutor's `OPENEDX_EXTRA_PIP_REQUIREMENTS` configuration setting:

.. code-block:: yaml

    OPENEDX_EXTRA_PIP_REQUIREMENTS:
    - git+https://github.com/edunext/openedx-events-2-zapier.git@main

2. Launch the Open edX platform to apply the changes:

.. code-block:: bash

     tutor local launch

3. Create and enable an Inline Tutor plugin to configure the Zapier webhooks:

   .. code-block:: python

        # Location plugins/zapier.py
        from tutor import hooks

        hooks.Filters.ENV_PATCHES.add_item(
            (
                "openedx-lms-common-settings",
        """
        ZAPIER_REGISTRATION_WEBHOOK = "https://hooks.zapier.com/hooks/catch/<account>/<webhook>/"
        ZAPIER_ENROLLMENT_WEBHOOK = "https://hooks.zapier.com/hooks/catch/<account>/<webhook>/"
        ZAPIER_GRADE_WEBHOOK = "https://hooks.zapier.com/hooks/catch/<account>/<webhook>/"
        """
            )
        )

 .. code-block:: bash

      tutor plugins enable zapier

4. Configure Zapier webhooks to receive the event data, follow the instructions available in the Zapier documentation.
5. Trigger the events by registering a new user, enrolling in a course, or updating a grade in the Open edX platform.

To send event data to other services or APIs, simply configure more webhooks in the Django settings. The handlers are intentionally generic, ensuring they work seamlessly with different kinds of services. You can also add more event handlers to the `handlers.py`_ file to listen to additional events.

How to Extend this Repository
-----------------------------

This repository is a starting point for Open edX developers:

- You can add new event handlers by following the structure in `handlers.py`_.
- Custom logic can be implemented to fit your organization's data flow requirements using Zapier, third-party APIs, or internal services.

For details on extending Open edX with Open edX Events, see:

- `Open edX Events Documentation`_
- `Hooks Extension Framework`_

The openedx-events-2-zapier repository is here to make integrations simple and sustainable, giving developers the tools to create effective Open edX workflows with external services like Zapier.

Development Workflow
--------------------

One Time Setup
~~~~~~~~~~~~~~
.. code-block::

  # Clone the repository
  git clone git@github.com:edx/openedx-events-2-zapier.git
  cd openedx-events-2-zapier

  # Set up a virtualenv using virtualenvwrapper with the same name as the repo and activate it
  mkvirtualenv -p python3.8 openedx-events-2-zapier


Every time you develop something in this repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

  # Activate the virtualenv
  workon openedx-events-2-zapier

  # Grab the latest code
  git checkout master
  git pull

  # Install/update the dev requirements
  make requirements

  # Run the tests and quality checks (to verify the status before you make any changes)
  make validate

  # Make a new branch for your changes
  git checkout -b <your_github_username>/<short_description>

  # Using your favorite editor, edit the code to make your change.
  vim …

  # Run your new tests
  pytest ./path/to/new/tests

  # Run all the tests and quality checks
  make validate

  # Commit all your changes
  git commit …
  git push

  # Open a PR and ask for review.

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

How To Contribute
-----------------

Contributions are very welcome.

The pull request description template should be automatically applied if you are
creating a pull request from GitHub. Otherwise you can find it at
`PULL_REQUEST_TEMPLATE.md <.github/PULL_REQUEST_TEMPLATE.md>`_.

The issue report template should be automatically applied if you are creating
an issue on GitHub as well. Otherwise you can find it at
`ISSUE_TEMPLATE.md <.github/ISSUE_TEMPLATE.md>`_.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edunext.co.

Getting Help
------------

This project was written in the context of the `Hooks Extension Framework`_ for Epen edX.
If you need help with it, the best way forward would be throught the Open edX
community at https://discuss.openedx.org where you can connect with both the
authors and other users in the community.


.. _Hooks Extension Framework: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html
.. _Open edX Events Documentation: https://docs.openedx.org/projects/openedx-events/en/latest/
.. _STUDENT_REGISTRATION_COMPLETED: https://docs.openedx.org/projects/openedx-events/en/latest/reference/events.html#openedxevent-org.openedx.learning.student.registration.completed.v1
.. _COURSE_ENROLLMENT_CREATED: https://docs.openedx.org/projects/openedx-events/en/latest/reference/events.html#openedxevent-org.openedx.learning.course.enrollment.created.v1
.. _PERSISTENT_GRADE_SUMMARY_CHANGED: https://docs.openedx.org/projects/openedx-events/en/latest/reference/events.html#openedxevent-org.openedx.learning.course.persistent_grade.summary.v1
.. _handlers.py: openedx_events_2_zapier/handlers.py
.. _receiver: https://docs.djangoproject.com/en/4.2/topics/signals/#connecting-receiver-functions
.. _Zapier webhook: https://zapier.com/
.. _Real-Life Use Cases for Open edX Events: https://docs.openedx.org/projects/openedx-events/en/latest/reference/real-life-use-cases.html
.. _Tutor plugin: https://docs.tutor.edly.io/plugins/intro.html#plugins

.. |ci-badge| image:: https://github.com/eduNEXT/openedx-events-2-zapier/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT/openedx-events-2-zapier/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/openedx-events-2-zapier.svg
    :target: https://github.com/eduNEXT/openedx-events-2-zapier/blob/main/LICENSE.txt
    :alt: License
