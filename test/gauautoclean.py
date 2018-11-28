from __future__ import absolute_import, division, unicode_literals

import os
import shutil
import subprocess
import tempfile
import unittest

class AutocleanTestCase(unittest.TestCase):
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

    def testNoBranches(self):
        """
        No action if there is no branch.
        """
        branches = self._cmd('git', 'branch', '--list', '--all')
        self.assertEqual(['* master'], branches.decode().splitlines())

        self._cmd('git', 'gau-autoclean', 'master')

        branches = self._cmd('git', 'branch', '--list', '--all')
        self.assertEqual(['* master'], branches.decode().splitlines())

    def testMergedBranch(self):
        """
        A merged branch should be removed.
        """
        file1 = os.path.join(self.repodir, 'test.txt')
        content1 = 'hello!\n'

        self._cmd('git', 'checkout', '-q', '-b', 'feature/master/file-1', 'master')
        with open(file1, 'w') as stream:
            stream.write(content1)
        self._cmd('git', 'add', file1)
        self._cmd('git', 'commit', '-q', '-m', 'add a file')

        branches = self._cmd('git', 'branch', '--list', '--all')
        self.assertEqual(['  master', '* feature/master/file-1'], sorted(branches.decode().splitlines()))

        self._cmd('git', 'checkout', '-q', 'master')
        self._cmd('git', 'merge', '-q', 'feature/master/file-1')

        self._cmd('git', 'gau-autoclean', 'master')

        branches = self._cmd('git', 'branch', '--list', '--all')
        self.assertEqual(['* master'], branches.decode().splitlines())

    def testUnmergedBranch(self):
        """
        An unmerged branch should be left alone.
        """
        file1 = os.path.join(self.repodir, 'test.txt')
        content1 = 'hello!\n'

        self._cmd('git', 'checkout', '-q', '-b', 'feature/master/file-1', 'master')
        with open(file1, 'w') as stream:
            stream.write(content1)
        self._cmd('git', 'add', file1)
        self._cmd('git', 'commit', '-q', '-m', 'add a file')

        branches = self._cmd('git', 'branch', '--list', '--all')
        self.assertEqual(['  master', '* feature/master/file-1'], sorted(branches.decode().splitlines()))

        self._cmd('git', 'checkout', '-q', 'master')

        self._cmd('git', 'gau-autoclean', 'master')

        branches = self._cmd('git', 'branch', '--list', '--all')
        self.assertEqual(['  feature/master/file-1', '* master'], branches.decode().splitlines())
