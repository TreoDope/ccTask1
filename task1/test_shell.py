import unittest
import tempfile
import os
import tarfile
import json
from io import BytesIO
from shell_emulator import VirtualShell

class TestVirtualShell(unittest.TestCase):
    def setUp(self):
        self.tar_file = tempfile.NamedTemporaryFile(delete=False, suffix=".tar")
        self.log_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

        with tarfile.open(self.tar_file.name, 'w') as tar:
            info = tarfile.TarInfo(name="file1.txt")
            info.size = len(b"Hello World")
            tar.addfile(info, BytesIO(b"Hello World"))

            info = tarfile.TarInfo(name="dir1/file2.txt")
            info.size = len(b"Goodbye World")
            tar.addfile(info, BytesIO(b"Goodbye World"))

            info = tarfile.TarInfo(name="dir1/dir2/file3.txt")
            info.size = len(b"Another File")
            tar.addfile(info, BytesIO(b"Another File"))

        self.shell = VirtualShell(self.tar_file.name, self.log_file.name)

    def test_ls_root(self):
        result = self.shell.ls()
        self.assertIn('file1.txt', result)

    def test_ls_dir1(self):
        self.shell.cd('dir1')
        result = self.shell.ls()
        self.assertIn('file2.txt', result)

    def test_cd_root(self):
        result = self.shell.cd('..')
        self.assertEqual(result, 'Changed directory to ')

    def test_cd_dir1(self):
        result = self.shell.cd('dir1')
        self.assertEqual(result, 'Changed directory to dir1')

    def test_tac_file1(self):
        result = self.shell.tac('file1.txt')
        self.assertEqual(result, 'dlroW olleH')

    def test_tac_file2(self):
        self.shell.cd('dir1')
        result = self.shell.tac('file2.txt')
        self.assertEqual(result, 'dlroW eybdooG')

    def test_chown_file1(self):
        result = self.shell.chown('file1.txt', 1001)
        self.assertEqual(result, 'Owner of file1.txt changed to 1001')

    def test_chown_file2(self):
        self.shell.cd('dir1')
        result = self.shell.chown('file2.txt', 1002)
        self.assertEqual(result, 'Owner of file2.txt changed to 1002')

    def test_exit(self):
        with self.assertRaises(SystemExit):
            self.shell.exit()

if __name__ == '__main__':
    unittest.main()
