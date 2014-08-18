# coding: utf-8
import json
import logging
import os
import re
import coverage
import requests
import yaml
from sh import git

from .reporter import CoverallReporter


log = logging.getLogger('coveralls')


class CoverallsException(Exception):
    pass


class Coveralls(object):
    config_filename = '.coveralls.yml'
    api_endpoint = 'https://coveralls.io/api/v1/jobs'
    default_client = 'coveralls-python'

    def __init__(self, **kwargs):
        """ Coveralls!

        * repo_token
          The secret token for your repository, found at the bottom of your repository's
           page on Coveralls.

        * service_name
          The CI service or other environment in which the test suite was run.
          This can be anything, but certain services have special features
          (travis-ci, travis-pro, or coveralls-ruby).

        * [service_job_id]
          A unique identifier of the job on the service specified by service_name.
        """
        self._data = None
        self.config = kwargs
        file_config = self.load_config() or {}
        repo_token = self.config.get('repo_token') or file_config.get('repo_token', None)
        if repo_token:
            self.config['repo_token'] = repo_token

        if os.environ.get('TRAVIS'):
            is_travis = True
            self.config['service_name'] = file_config.get('service_name', None) or 'travis-ci'
            self.config['service_job_id'] = os.environ.get('TRAVIS_JOB_ID')
        else:
            is_travis = False
            self.config['service_name'] = file_config.get('service_name') or self.default_client

        if os.environ.get('COVERALLS_REPO_TOKEN', None):
            self.config['repo_token'] = os.environ.get('COVERALLS_REPO_TOKEN')

        if not self.config.get('repo_token') and not is_travis:
            raise CoverallsException('You have to provide either repo_token in %s, or launch via Travis' % self.config_filename)

    def load_config(self):
        try:
            return yaml.safe_load(open(os.path.join(os.getcwd(), self.config_filename)))
        except (OSError, IOError):
            log.debug('Missing %s file. Using only env variables.', self.config_filename)
            return {}

    def wear(self, dry_run=False):
        """ run! """
        try:
            data = self.create_data()
        except coverage.CoverageException as e:
            return {'message': 'Failure to gather coverage: %s' % str(e)}
        json_string = json.dumps(data)
        if not dry_run:
            response = requests.post(self.api_endpoint, files={'json_file': json_string})
            try:
                result = response.json()
            except ValueError:
                result = {'message': 'Failure to submit data. Response [%(status)s]: %(text)s' % {
                    'status': response.status_code,
                    'text': response.text}}
        else:
            result = {}
        json_string = re.sub(r'"repo_token": "(.+?)"', '"repo_token": "[secure]"', json_string)
        log.debug(json_string)
        return result

    def create_data(self):
        """ Generate object for api.
            Example json:
            {
                "service_job_id": "1234567890",
                "service_name": "travis-ci",
                "source_files": [
                    {
                        "name": "example.py",
                        "source": "def four\n  4\nend",
                        "coverage": [null, 1, null]
                    },
                    {
                        "name": "two.py",
                        "source": "def seven\n  eight\n  nine\nend",
                        "coverage": [null, 1, 0, null]
                    }
                ]
            }
        """
        if not self._data:
            self._data = {'source_files': self.get_coverage()}
            self._data.update(self.git_info())
            self._data.update(self.config)
        return self._data

    def get_coverage(self):
        workman = coverage.coverage()
        workman.load()
        workman._harvest_data()
        reporter = CoverallReporter(workman, workman.config)
        return reporter.report()

    def git_info(self):
        """ A hash of Git data that can be used to display more information to users.

            Example:
            "git": {
                "head": {
                    "id": "5e837ce92220be64821128a70f6093f836dd2c05",
                    "author_name": "Wil Gieseler",
                    "author_email": "wil@example.com",
                    "committer_name": "Wil Gieseler",
                    "committer_email": "wil@example.com",
                    "message": "depend on simplecov >= 0.7"
                },
                "branch": "master",
                "remotes": [{
                    "name": "origin",
                    "url": "https://github.com/lemurheavy/coveralls-ruby.git"
                }]
            }
        """

        git_info = {'git': {
            'head': {
                'id': gitlog('%H'),
                'author_name': gitlog('%aN'),
                'author_email': gitlog('%ae'),
                'committer_name': gitlog('%cN'),
                'committer_email': gitlog('%ce'),
                'message': gitlog('%s'),
            },
            'branch': os.environ.get('CIRCLE_BRANCH') or os.environ.get('TRAVIS_BRANCH', git('rev-parse', '--abbrev-ref', 'HEAD').strip()), 
            #origin	git@github.com:coagulant/coveralls-python.git (fetch)
            'remotes': [{'name': line.split()[0], 'url': line.split()[1]}
                        for line in git.remote('-v') if '(fetch)' in line]
        }}
        return git_info


def gitlog(format):
    return str(git('--no-pager', 'log', "-1", pretty="format:%s" % format))
