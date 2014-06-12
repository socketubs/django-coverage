"""
Copyright 2009 55 Minutes (http://www.55minutes.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from optparse import make_option

from django.conf import settings
from django.core.management.commands import test

from django_coverage import settings as coverage_settings


class Command(test.Command):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.option_list += (
            make_option(
                '--with-coverage',
                action="store_true", dest="with_coverage", default=False,
                help="Use Coverage TestRunner to generate coverage."), )

    def handle(self, *args, **kwargs):
        """
        Replaces the original test runner with the coverage test runner, but
        keeps track of what the original runner was so that the coverage
        runner can inherit from it.  Then, call the test command. This
        plays well with apps that override the test command, such as South.
        """
        if kwargs.get('with_coverage'):
            coverage_settings.ORIG_TEST_RUNNER = settings.TEST_RUNNER
            settings.TEST_RUNNER = coverage_settings.COVERAGE_TEST_RUNNER
        super(Command, self).handle(*args, **kwargs)
