from __future__ import absolute_import, division, unicode_literals

import os
import shutil
import subprocess
import tempfile
import unittest

class AutomergeTestCase(unittest.TestCase):
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

    def testNoMatch(self):
        """
        Do nothing if no branch matches the pattern
        """
        file1 = os.path.join(self.repodir, 'test.txt')
        content1 = 'hello!\n'

        self._cmd('git', 'checkout', '-q', '-b', 'feature/master/file-1', 'master')
        with open(file1, 'w') as stream:
            stream.write(content1)
        self._cmd('git', 'add', file1)
        self._cmd('git', 'commit', '-q', '-m', 'add a file')

        self._cmd('git', 'checkout', '-q', 'master')

        logs = self._cmd('git', 'log', '--format=%s')
        self.assertEqual(logs, b'Initial commit\n')

        self._cmd('git', 'gau-automerge', 'feature/master/auto-*')

        logs = self._cmd('git', 'log', '--format=%s')
        self.assertEqual(logs, b'Initial commit\n')


    def testFastForwardMerge(self):
        """
        Merge of a simple fast-forward commit succeeds.
        """
        file1 = os.path.join(self.repodir, 'test.txt')
        content1 = 'hello!\n'

        self._cmd('git', 'checkout', '-q', '-b', 'feature/master/file-1', 'master')
        with open(file1, 'w') as stream:
            stream.write(content1)
        self._cmd('git', 'add', file1)
        self._cmd('git', 'commit', '-q', '-m', 'add a file')

        self._cmd('git', 'checkout', '-q', 'master')
        self._cmd('git', 'gau-automerge', 'feature/master/file-1')

        with open(file1, 'r') as stream:
            actual = stream.read()

        self.assertEqual(content1, actual)

    def testOctoMerge(self):
        """
        Merge of multiple branches succeeds if there are no conflicts.
        """
        file1 = os.path.join(self.repodir, 'test.txt')
        content1 = 'hello!\n'
        content1ext = content1 + 'world\n'

        file2 = os.path.join(self.repodir, 'other.txt')
        content2 = '42\n'

        file3 = os.path.join(self.repodir, 'on-unrelated-branch.txt')
        content3 = 'unexpected\n'

        self._cmd('git', 'checkout', '-q', '-b', 'feature/master/auto-123', 'master')
        with open(file1, 'w') as stream:
            stream.write(content1)
        self._cmd('git', 'add', file1)
        self._cmd('git', 'commit', '-q', '-m', 'add a file')

        self._cmd('git', 'checkout', '-q', '-b', 'feature/master/auto-abc', 'master')
        with open(file2, 'w') as stream:
            stream.write(content2)
        self._cmd('git', 'add', file2)
        self._cmd('git', 'commit', '-q', '-m', 'add another')

        self._cmd('git', 'checkout', '-q', '-b', 'feature/master/auto-123-extended', 'feature/master/auto-123')
        with open(file1, 'w') as stream:
            stream.write(content1ext)
        self._cmd('git', 'add', file1)
        self._cmd('git', 'commit', '-q', '-m', 'changed a file')

        self._cmd('git', 'checkout', '-q', '-b', 'feature/master/noauto', 'master')
        with open(file3, 'w') as stream:
            stream.write(content3)
        self._cmd('git', 'add', file3)
        self._cmd('git', 'commit', '-q', '-m', 'commit on an unrelated branch')

        self._cmd('git', 'checkout', '-q', 'master')
        self._cmd('git', 'gau-automerge', 'feature/master/auto-*')

        with open(file1, 'r') as stream:
            actual = stream.read()

        self.assertEqual(content1ext, actual)

        with open(file2, 'r') as stream:
            actual = stream.read()

        self.assertEqual(content2, actual)

        self.assertFalse(os.path.exists(file3))


    def testMergeArgs(self):
        """
        Merge will fail if options from environment cannot  be met.
        """
        env = os.environ.copy()
        env.update({
            'GAU_MERGE_ARGS': '--ff-only'
        })

        file1 = os.path.join(self.repodir, 'test.txt')
        content1 = 'hello!\n'
        content1ext = content1 + 'world\n'

        file2 = os.path.join(self.repodir, 'other.txt')
        content2 = '42\n'

        self._cmd('git', 'checkout', '-q', '-b', 'feature/master/auto-123', 'master')
        with open(file1, 'w') as stream:
            stream.write(content1)
        self._cmd('git', 'add', file1)
        self._cmd('git', 'commit', '-q', '-m', 'add a file')

        self._cmd('git', 'checkout', '-q', '-b', 'feature/master/auto-abc', 'master')
        with open(file2, 'w') as stream:
            stream.write(content2)
        self._cmd('git', 'add', file2)
        self._cmd('git', 'commit', '-q', '-m', 'add another')

        self._cmd('git', 'checkout', '-q', 'master')
        self.assertRaises(subprocess.CalledProcessError, self._cmd,
                          'git', 'gau-automerge', 'feature/master/auto-*', env=env)

        logs = self._cmd('git', 'log', '--format=%s')

        self.assertEqual(logs, b'Initial commit\n')
