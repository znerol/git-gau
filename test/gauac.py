from __future__ import absolute_import, division, unicode_literals

import os
import shutil
import subprocess
import tempfile
import unittest

class AcTestCase(unittest.TestCase):
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

    def testCommitSimple(self):
        """
        Simple script resulting in modified file and log message.
        """

        script = 'echo hello > test.txt; echo Commit subject'
        output = self._cmd('git', 'gau-ac', '/bin/sh', '-c', script)
        self.assertEqual(output, b'Commit subject\n')

        logs = self._cmd('git', 'log', '--format=%s')

        self.assertEqual(logs, b'Commit subject\nInitial commit\n')

        self._cmd('git', 'clean', '-dxf')
        with open(os.path.join(self.repodir, 'test.txt'), 'rb') as f:
            content = f.read()
            self.assertEqual(content, b'hello\n')

    def testCommitStderr(self):
        """
        Simple script resulting in modified file and log message.
        """

        script = 'echo hello > test.txt; echo Stderr subject >&2'
        output = self._cmd('git', 'gau-ac', '/bin/sh', '-c', script)
        self.assertEqual(output, b'Stderr subject\n')

        logs = self._cmd('git', 'log', '--format=%s')

        self.assertEqual(logs, b'Stderr subject\nInitial commit\n')

        self._cmd('git', 'clean', '-dxf')
        with open(os.path.join(self.repodir, 'test.txt'), 'rb') as f:
            content = f.read()
            self.assertEqual(content, b'hello\n')

    def testCommitOnNewBranch(self):
        """
        Create and checkout a new branch before committing new file and log message.
        """

        env = os.environ.copy()
        env.update({
            'GAU_CHECKOUT_ARGS': '--quiet -b newbranch master'
        })

        script = 'echo hello > test.txt; echo Commit subject'
        output = self._cmd('git', 'gau-ac', '/bin/sh', '-c', script, env=env)
        self.assertEqual(output, b'Commit subject\n')

        logs = self._cmd('git', 'log', '--format=%s')

        self.assertEqual(logs, b'Commit subject\nInitial commit\n')

        self._cmd('git', 'clean', '-dxf')
        with open(os.path.join(self.repodir, 'test.txt'), 'rb') as f:
            content = f.read()
            self.assertEqual(content, b'hello\n')

        curbranch = self._cmd('git', 'rev-parse', '--abbrev-ref', 'HEAD')
        self.assertEqual(curbranch, b'newbranch\n')

        self._cmd('git', 'checkout', 'master')

        logs = self._cmd('git', 'log', '--format=%s')
        self.assertEqual(logs, b'Initial commit\n')

    def testCommitSelectedFiles(self):
        """
        Create and checkout a new branch before committing new file and log message.
        """

        env = os.environ.copy()
        env.update({
            'GAU_ADD_ARGS': 'other.txt'
        })

        script = 'echo hello > test.txt; echo world > other.txt; echo Commit subject'
        output = self._cmd('git', 'gau-ac', '/bin/sh', '-c', script, env=env)
        self.assertEqual(output, b'Commit subject\n')

        logs = self._cmd('git', 'log', '--format=%s')

        self.assertEqual(logs, b'Commit subject\nInitial commit\n')

        self._cmd('git', 'clean', '-dxf')
        with open(os.path.join(self.repodir, 'other.txt'), 'rb') as f:
            content = f.read()
            self.assertEqual(content, b'world\n')

        self.assertFalse(os.path.exists(os.path.join(self.repodir, 'test.txt')))

    def testCommitWithCustomAuthor(self):
        """
        Perform a commit with custom arguments.
        """

        env = os.environ.copy()
        env.update({
            'GAU_COMMIT_ARGS': '--quiet --author="Custom Author <custom-author@example.com>"'
        })

        script = 'echo hello > test.txt; echo Commit subject'
        output = self._cmd('git', 'gau-ac', '/bin/sh', '-c', script, env=env)
        self.assertEqual(output, b'Commit subject\n')

        logs = self._cmd('git', 'log', '--format=%s')

        self.assertEqual(logs, b'Commit subject\nInitial commit\n')

        self._cmd('git', 'clean', '-dxf')
        with open(os.path.join(self.repodir, 'test.txt'), 'rb') as f:
            content = f.read()
            self.assertEqual(content, b'hello\n')

        curauthor = self._cmd('git', 'show', '--no-patch', '--format=%an', 'HEAD')
        self.assertEqual(curauthor, b'Custom Author\n')
        curmail = self._cmd('git', 'show', '--no-patch', '--format=%ae', 'HEAD')
        self.assertEqual(curmail, b'custom-author@example.com\n')

        prevauthor = self._cmd('git', 'show', '--no-patch', '--format=%an', 'HEAD^')
        self.assertEqual(prevauthor, b'Test\n')
        prevmail = self._cmd('git', 'show', '--no-patch', '--format=%ae', 'HEAD^')
        self.assertEqual(prevmail, b'test@localhost\n')

    def testFailOnNoChanges(self):
        """
        Command with no effects must not result in a commit.
        """

        self.assertRaises(subprocess.CalledProcessError, self._cmd,
                          'git', 'gau-ac', '/bin/true')

        logs = self._cmd('git', 'log', '--format=%s')

        self.assertEqual(logs, b'Initial commit\n')

    def testFailOnExitStatusNonZero(self):
        """
        Command with non-zero status will not result in a commit.
        """

        script = 'echo hello > test.txt; echo Commit subject; /bin/false'
        self.assertRaises(subprocess.CalledProcessError, self._cmd,
                          'git', 'gau-ac', '/bin/sh', '-c', script)

        logs = self._cmd('git', 'log', '--format=%s')

        self.assertEqual(logs, b'Initial commit\n')
