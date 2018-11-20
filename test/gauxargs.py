from __future__ import absolute_import, division, unicode_literals

import os
import shutil
import subprocess
import tempfile
import unittest

class XargsTestCase(unittest.TestCase):
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

    def testCallsSubcommandWithRootParam(self):
        subdir = os.path.join(self.repodir, 'subdir')
        os.mkdir(subdir)

        with open(os.path.join(self.repodir, 'toplevel.txt'), 'w') as out:
            out.write('TOP')

        output = self._cmd('git', 'gau-xargs', 'echo', cwd=subdir)
        self.assertEqual(output, '{:s}\n'.format(self.repodir).encode())

        output = self._cmd('git', 'gau-xargs', '-I{}', 'cat', '{}/toplevel.txt', cwd=subdir)
        self.assertEqual(output, b'TOP')

    def testFailsIfOutsideRepo(self):
        """
        Command fails if invoked outside of a git repository.
        """

        anywhere = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, anywhere)

        self._cmd('git', 'gau-xargs', 'true')
        self.assertRaises(subprocess.CalledProcessError, self._cmd,
                          'git', 'gau-xargs', '/bin/true', cwd=anywhere)
