#!/usr/bin/env python

# http://ericholscher.com/blog/2009/jun/29/enable-setuppy-test-your-django-apps/
# http://www.travisswicegood.com/2010/01/17/django-virtualenv-pip-and-fabric/
# http://code.djangoproject.com/svn/django/trunk/tests/runtests.py
import os
import sys
import django

# fix sys path so we don't need to setup PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'whippedcream.runtests.settings'

from django.conf import settings
from django.test.utils import get_runner


def main():
    TestRunner = get_runner(settings)

    test_runner = TestRunner()
    ALL_TESTS = [
        'whippedcream.tests.basic'
    ]

    if django.VERSION[0] == 1 and django.VERSION[1] >= 7:
        django.setup()

    failures = test_runner.run_tests(ALL_TESTS)

    sys.exit(failures)

if __name__ == '__main__':
    main()
