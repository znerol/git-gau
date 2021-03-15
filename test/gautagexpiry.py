from __future__ import absolute_import, division, unicode_literals

import os
import datetime
import shutil
import subprocess
import tempfile
import unittest

class TagExpiryTestCase(unittest.TestCase):
    repodir = None
    t3 = datetime.datetime.now()-datetime.timedelta(days=3)
    t7 = datetime.datetime.now()-datetime.timedelta(days=7)
    t10 = datetime.datetime.now()-datetime.timedelta(days=10)

    def _cmd(self, *args, **kwds):
        kwds.setdefault('cwd', self.repodir)
        return subprocess.check_output(args, **kwds)

    def setUp(self):
        self.repodir = tempfile.mkdtemp()
        self._cmd('git', 'init')
        self._cmd('git', 'config', 'user.name', 'Test')
        self._cmd('git', 'config', 'user.email', 'test@localhost')
        self._cmd('git', 'commit', '--allow-empty', '-m', 'Initial commit')

        # Create annotated tag seven days ago with defaults from git-gau-at.
        branch = self._cmd('git', 'rev-parse', '--abbrev-ref', '--symbolic', 'HEAD')
        datestr = self.t7.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        tagname = "/".join(['build', branch.rstrip().decode(), datestr])

        env = os.environ.copy()
        env.update({
            'GIT_COMMITTER_DATE': self.t7.isoformat()
        })
        self._cmd('git', 'tag', '--annotate', '--message', 'Most recent build', tagname, env=env)

        # Create another tag three days ago with different pattern.
        env = os.environ.copy()
        env.update({
            'GIT_COMMITTER_DATE': self.t3.isoformat()
        })
        self._cmd('git', 'tag', '--annotate', '--message', 'Most recent release', 'release/v2.0.3', env=env)

        # Create another tag ten days ago with different pattern.
        env = os.environ.copy()
        env.update({
            'GIT_COMMITTER_DATE': self.t10.isoformat()
        })
        self._cmd('git', 'tag', '--annotate', '--message', 'Most recent release', 'release/v2.0.2')

    def tearDown(self):
        if self.repodir is not None:
            shutil.rmtree(self.repodir)

    def testExpirySimple(self):
        """
        Static tag with simple script resulting in a message.
        """

        script = 'echo Build expired!'

        branch = self._cmd('git', 'rev-parse', '--abbrev-ref', '--symbolic', 'HEAD')
        pattern = '/'.join(['build', branch.rstrip().decode(), '*'])

        # with ttl=two days, no expiry expected
        d2 = int(datetime.timedelta(days=2).total_seconds())
        output = self._cmd('git', 'gau-tag-expiry', pattern, str(d2), '/bin/sh', '-c', script)
        self.assertEqual(output, b'')

        # with ttl=six days, no expiry expected
        d6 = int(datetime.timedelta(days=6).total_seconds())
        output = self._cmd('git', 'gau-tag-expiry', pattern, str(d6), '/bin/sh', '-c', script)
        self.assertEqual(output, b'')

        # with ttl=eight days, expiry expected
        d8 = int(datetime.timedelta(days=8).total_seconds())
        output = self._cmd('git', 'gau-tag-expiry', pattern, str(d8), '/bin/sh', '-c', script)
        self.assertEqual(output, b'Build expired!\n')

    def testExpiryBranchPlaceholder(self):
        """
        Tag pattern with branch placeholder with simple script resulting in a message.
        """

        script = 'echo Build expired!'

        pattern = 'build/%b/*'

        # with ttl=two days, no expiry expected
        d2 = int(datetime.timedelta(days=2).total_seconds())
        output = self._cmd('git', 'gau-tag-expiry', pattern, str(d2), '/bin/sh', '-c', script)
        self.assertEqual(output, b'')

        # with ttl=six days, no expiry expected
        d6 = int(datetime.timedelta(days=6).total_seconds())
        output = self._cmd('git', 'gau-tag-expiry', pattern, str(d6), '/bin/sh', '-c', script)
        self.assertEqual(output, b'')

        # with ttl=eight days, expiry expected
        d8 = int(datetime.timedelta(days=8).total_seconds())
        output = self._cmd('git', 'gau-tag-expiry', pattern, str(d8), '/bin/sh', '-c', script)
        self.assertEqual(output, b'Build expired!\n')

    def testExpiryNoMatchingTag(self):
        """
        Static tag with simple script resulting in a message.
        """

        script = 'echo Build expired!'

        pattern = 'no-matching-category/*'

        # with ttl=two days, expiry expected
        d2 = int(datetime.timedelta(days=2).total_seconds())
        output = self._cmd('git', 'gau-tag-expiry', pattern, str(d2), '/bin/sh', '-c', script)
        self.assertEqual(output, b'Build expired!\n')

        # with ttl=six days, expiry expected
        d6 = int(datetime.timedelta(days=6).total_seconds())
        output = self._cmd('git', 'gau-tag-expiry', pattern, str(d6), '/bin/sh', '-c', script)
        self.assertEqual(output, b'Build expired!\n')

        # with ttl=eight days, expiry expected
        d8 = int(datetime.timedelta(days=8).total_seconds())
        output = self._cmd('git', 'gau-tag-expiry', pattern, str(d8), '/bin/sh', '-c', script)
        self.assertEqual(output, b'Build expired!\n')

    def testFailOnExitStatusNonZero(self):
        """
        Command with non-zero status will propagate.
        """

        script = 'echo Expiry check failed; /bin/false'
        self.assertRaises(subprocess.CalledProcessError, self._cmd,
                          'git', 'gau-tag-expiry', '*', '-c', script)
