from __future__ import absolute_import, division, unicode_literals

import datetime
import dateutil.parser
import shutil
import subprocess
import tempfile
import unittest

class AtTestCase(unittest.TestCase):
    repodir = None

    def _cmd(self, *args, **kwds):
        kwds.setdefault('cwd', self.repodir)
        return subprocess.check_output(args, **kwds)

    def setUp(self):
        self.repodir = tempfile.mkdtemp()
        self._cmd('git', 'init')
        self._cmd('git', 'config', 'user.name', 'Test')
        self._cmd('git', 'config', 'user.email', 'test@localhost')
        self._cmd('git', 'commit', '--allow-empty', '-m', 'Initial commit')

    def tearDown(self):
        if self.repodir is not None:
            shutil.rmtree(self.repodir)

    def testMessageSimple(self):
        """
        Static tag with simple script resulting in a message.
        """

        script = 'echo Tag message'
        output = self._cmd('git', 'gau-at', 'some-tag', '/bin/sh', '-c', script)
        self.assertEqual(output, b'Tag message\n')

        tags = self._cmd('git', 'tag', '--format=%(refname:short) %(contents)')

        self.assertEqual(tags, b'some-tag Tag message\n\n')

    def testTagWithBranchAndDate(self):
        """
        Dynamic tag with branch and date and a simple script resulting in a message.
        """

        script = 'echo Tag message'
        output = self._cmd('git', 'gau-at', 'build/%b/%d', '/bin/sh', '-c', script)
        self.assertEqual(output, b'Tag message\n')

        tags = self._cmd('git', 'tag', '--format=%(refname:short) %(contents)')

        date = dateutil.parser.parse(self._cmd('git', 'tag', '--format=%(taggerdate)'))
        datestr = date.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        branch = self._cmd('git', 'rev-parse', '--abbrev-ref', '--symbolic', 'HEAD')

        expected_tag = b'/'.join([b'build', branch.rstrip(), datestr.encode()])
        self.assertEqual(tags, expected_tag + b' Tag message\n\n')

    def testFailOnExitStatusNonZero(self):
        """
        Command with non-zero status will not result in a commit.
        """

        script = 'echo hello > test.txt; echo Commit subject; /bin/false'
        self.assertRaises(subprocess.CalledProcessError, self._cmd,
                          'git', 'gau-ac', '/bin/sh', '-c', script)

        tags = self._cmd('git', 'tag', '--format="%(refname:short) %(contents)"')

        self.assertEqual(tags, b'')
