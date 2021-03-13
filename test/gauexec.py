from __future__ import absolute_import, division, unicode_literals

import os
import shutil
import subprocess
import tempfile
import unittest

class ExecTestCase(unittest.TestCase):
    repodir = None
    workdir = None

    def _cmd(self, *args, **kwds):
        kwds.setdefault('cwd', self.repodir)
        return subprocess.check_output(args, **kwds)

    def setUp(self):
        self.repodir = tempfile.mkdtemp()
        self.workdir = tempfile.mkdtemp()

        self._cmd('git', 'init', '--bare', self.repodir)
        self._cmd('git', 'clone', '--quiet', self.repodir, self.workdir)

        self._cmd('git', 'config', 'user.name', 'Test', cwd=self.workdir)
        self._cmd('git', 'config', 'user.email', 'test@localhost', cwd=self.workdir)
        self._cmd('git', 'commit', '--quiet', '--allow-empty', '-m', 'Initial commit', cwd=self.workdir)
        self._cmd('git', 'push', '--quiet', cwd=self.workdir)

    def tearDown(self):
        if self.repodir is not None:
            shutil.rmtree(self.repodir)

        if self.workdir is not None:
            shutil.rmtree(self.workdir)

    def testNoOperation(self):
        """
        Simple script no changes.
        """

        output = self._cmd('git', 'gau-exec', self.repodir, '/bin/true')
        self.assertEqual(output, b'')

        logs = self._cmd('git', 'log', '--format=%s')
        self.assertEqual(logs, b'Initial commit\n')

    def testWorkingDirectory(self):
        """
        Tests that the working directory is not changed.
        """

        args = ['git', 'gau-exec', self.repodir, '/bin/pwd']
        output = subprocess.check_output(args)
        self.assertEqual(output, '{:s}\n'.format(os.getcwd()).encode())

    def testFailOnExitStatusNonZero(self):
        """
        Command with non-zero status will not result in a push.
        """

        self.assertRaises(subprocess.CalledProcessError, self._cmd,
                          'git', 'gau-exec', self.repodir, '/bin/false')

    def testCommitAndPush(self):
        """
        Simple script no changes.
        """
        env = os.environ.copy()
        env.update({
            'GIT_COMMITTER_NAME': 'Test Committer',
            'GIT_COMMITTER_EMAIL': 'committer@localhost',
            'GIT_AUTHOR_NAME': 'Test Author',
            'GIT_AUTHOR_EMAIL': 'author@localhost',
        })

        script = 'git commit --quiet --allow-empty -m "Second commit"'
        self._cmd('git', 'gau-exec', self.repodir,
                           '/bin/sh', '-c', script, env=env)

        logs = self._cmd('git', 'log', '--format=%s')
        self.assertEqual(logs, b'Second commit\nInitial commit\n')

        curauthor = self._cmd('git', 'show', '--no-patch', '--format=%an', 'HEAD')
        self.assertEqual(curauthor, b'Test Author\n')
        curmail = self._cmd('git', 'show', '--no-patch', '--format=%ae', 'HEAD')
        self.assertEqual(curmail, b'author@localhost\n')

        prevauthor = self._cmd('git', 'show', '--no-patch', '--format=%an', 'HEAD^')
        self.assertEqual(prevauthor, b'Test\n')
        prevmail = self._cmd('git', 'show', '--no-patch', '--format=%ae', 'HEAD^')
        self.assertEqual(prevmail, b'test@localhost\n')

    def testCommitAndPushNewBranch(self):
        """
        Simple script no changes, push to new branch.
        """
        env = os.environ.copy()
        env.update({
            'GIT_COMMITTER_NAME': 'Test Committer',
            'GIT_COMMITTER_EMAIL': 'committer@localhost',
            'GIT_AUTHOR_NAME': 'Test Author',
            'GIT_AUTHOR_EMAIL': 'author@localhost',
            'GAU_PUSH_BRANCH': 'feature/master/updates-123'
        })

        script = 'git commit --quiet --allow-empty -m "Branch commit"'
        self._cmd('git', 'gau-exec', self.repodir,
                           '/bin/sh', '-c', script, env=env)

        logs = self._cmd('git', 'log', '--format=%s', 'master')
        self.assertEqual(logs, b'Initial commit\n')

        logs = self._cmd('git', 'log', '--format=%s', 'feature/master/updates-123')
        self.assertEqual(logs, b'Branch commit\nInitial commit\n')

        curauthor = self._cmd('git', 'show', '--no-patch', '--format=%an', 'feature/master/updates-123')
        self.assertEqual(curauthor, b'Test Author\n')
        curmail = self._cmd('git', 'show', '--no-patch', '--format=%ae', 'feature/master/updates-123')
        self.assertEqual(curmail, b'author@localhost\n')

        prevauthor = self._cmd('git', 'show', '--no-patch', '--format=%an', 'feature/master/updates-123^')
        self.assertEqual(prevauthor, b'Test\n')
        prevmail = self._cmd('git', 'show', '--no-patch', '--format=%ae', 'feature/master/updates-123^')
        self.assertEqual(prevmail, b'test@localhost\n')

    def testCheckoutAndPushNewBranch(self):
        """
        Simple script no changes, push to new branch.
        """

        script = 'git checkout -b feature/master/bells-and-whistles'
        self._cmd('git', 'gau-exec', self.repodir,
                           '/bin/sh', '-c', script)

        logs = self._cmd('git', 'log', '--format=%s', 'master')
        self.assertEqual(logs, b'Initial commit\n')

        logs = self._cmd('git', 'log', '--format=%s', 'feature/master/bells-and-whistles')
        self.assertEqual(logs, b'Initial commit\n')

    def testBranchSpecifiedInUrl(self):
        """
        Clone from branch specified in URL
        """

        # First step create a new branch in the repo
        script = 'git checkout -b some-other-branch'
        self._cmd('git', 'gau-exec', self.repodir, '/bin/sh', '-c', script)

        # Second step clone the new branch but specify it in the git url.
        repourl = ''.join([self.repodir, "#", 'some-other-branch'])
        script = 'git commit --quiet --allow-empty -m "Branch commit"'
        self._cmd('git', 'gau-exec', repourl, '/bin/sh', '-c', script)

        logs = self._cmd('git', 'log', '--format=%s', 'master')
        self.assertEqual(logs, b'Initial commit\n')

        logs = self._cmd('git', 'log', '--format=%s', 'some-other-branch')
        self.assertEqual(logs, b'Branch commit\nInitial commit\n')
