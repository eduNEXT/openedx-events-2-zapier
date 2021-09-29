openedx-events-2-zapier
=============================

|ci-badge| |license-badge|

A ready-to-use repository that contains real-life use cases for Open edX Events.

Overview
---------

One common use cases for open edx instances is to connect enrollment and
registration events to custom workflows that enhance the user experience.
At edunext, we have found that sending this information to Zapier is a very
flexible and robust way to achieve this. This repository makes just that very
easy. By installing and configuring it creates receivers for the two events:

- Registration (STUDENT_REGISTRATION_COMPLETED)
  `org.openedx.learning.student.registration.completed.v1`

- Enrollment (COURSE_ENROLLMENT_CREATED)
  `org.openedx.learning.course.enrollment.created.v1`

And then formats the information in a zappier friendly way and sends it.

Checkout `receivers.py <https://github.com/eduNEXT/openedx-events-2-zapier/blob/main/openedx_events_2_zapier/receivers.py>`_ for implementation details.

For more information see `Open edX Events`_ and `Hooks framework`_.

Usage
-----

After installing the plugin, please modify the following settings in common.py
or production.py (through env-tokens) with the URL for your own zappier webhook:

.. code-block:: python


    ZAPIER_REGISTRATION_WEBHOOK = "https://hooks.zapier.com/hooks/catch/<account>/<webhook>/"
    ZAPIER_ENROLLMENT_WEBHOOK = "https://hooks.zapier.com/hooks/catch/<account>/<webhook>/"

Now, you're ready to go.

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

This project was written in the context of the `Hooks framework`_ for open edx.
If you need help with it, the best way forward would be throught the Open edX
community at https://discuss.openedx.org where you can connect with both the
authors and other users in the community.


.. _Hooks framework: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html
.. _Open edX Events: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html


.. |ci-badge| image:: https://github.com/eduNEXT/openedx-events-2-zapier/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/edx/openedx-events-2-zapier/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/openedx-events-2-zapier.svg
    :target: https://github.com/eduNEXT/openedx-events-2-zapier/blob/main/LICENSE.txt
    :alt: License
