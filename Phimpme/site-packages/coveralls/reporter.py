# coding: utf-8
import logging
import sys

from coverage.misc import NoSource, NotPython
from coverage.phystokens import source_encoding
from coverage.report import Reporter


log = logging.getLogger('coveralls')


class CoverallReporter(Reporter):
    """ Custom coverage.py reporter for coveralls.io
    """
    def report(self, morfs=None):
        """ Generate a part of json report for coveralls

        `morfs` is a list of modules or filenames.
        `outfile` is a file object to write the json to.
        """
        self.source_files = []
        self.find_code_units(morfs)

        for cu in self.code_units:
            try:
                self.parse_file(cu, self.coverage._analyze(cu))
            except NoSource:
                if not self.config.ignore_errors:
                    log.warn('No source for %s', cu.name)
            except NotPython:
                # Only report errors for .py files, and only if we didn't
                # explicitly suppress those errors.
                if cu.should_be_python() and not self.config.ignore_errors:
                    log.warn('Source file is not python %s', cu.name)

        return self.source_files

    def get_hits(self, line_num, analysis):
        """ Source file stats for each line.

            * A positive integer if the line is covered,
            representing the number of times the line is hit during the test suite.
            * 0 if the line is not covered by the test suite.
            * null to indicate the line is not relevant to code coverage
              (it may be whitespace or a comment).
        """
        if line_num in analysis.missing:
            return 0
        if line_num in analysis.statements:
            return 1
        return None

    def parse_file(self, cu, analysis):
        """ Generate data for single file """
        filename = cu.file_locator.relative_filename(cu.filename)
        coverage_lines = [self.get_hits(i, analysis) for i in range(1, len(analysis.parser.lines) + 1)]
        source_file = cu.source_file()
        try:
            source = source_file.read()
            if sys.version_info < (3, 0):
                encoding = source_encoding(source)
                if encoding != 'utf-8':
                    source = source.decode(encoding).encode('utf-8')
        finally:
            source_file.close()
        self.source_files.append({
            'name': filename,
            'source': source,
            'coverage': coverage_lines
        })