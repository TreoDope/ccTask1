import unittest
import os
import json
import datetime
import tarfile
from shell_emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        self.vfs_path = "test_vfs.tar"
        self.log_path = "test_log.json"

        os.makedirs("test_vfs/dir1", exist_ok=True)
        with open("test_vfs/file1.txt", "w") as f:
            f.write("This is a test file.")
        with open("test_vfs/dir1/file2.txt", "w") as f:
            f.write("This is another test file.")

        with tarfile.open(self.vfs_path, "w") as tar:
            tar.add("test_vfs", arcname=".")

        self.emulator = ShellEmulator(self.vfs_path, self.log_path)

    def tearDown(self):
        if os.path.exists(self.vfs_path):
            os.remove(self.vfs_path)
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
        if os.path.exists("test_vfs"):
            os.remove("test_vfs/file1.txt")
            os.remove("test_vfs/dir1/file2.txt")
            os.rmdir("test_vfs/dir1")
            os.rmdir("test_vfs")

    def test_ls(self):
        output = self.emulator.ls()
        self.assertIn("file1.txt", output)
        self.assertIn("dir1", output)

    def test_cd(self):
        output = self.emulator.cd("dir1")
        self.assertEqual(output, "Changed directory to dir1")
        self.assertEqual(self.emulator.current_dir, "/dir1")

        output = self.emulator.cd("..")
        self.assertEqual(output, "Changed to parent directory")
        self.assertEqual(self.emulator.current_dir, "/")

        output = self.emulator.cd("nonexistent")
        self.assertEqual(output, "No such directory")

    def test_tac(self):
        output = self.emulator.tac("file1.txt")
        self.assertEqual(output, ".elif tset a si sihT")

        output = self.emulator.tac("nonexistent.txt")
        self.assertEqual(output, "File not found")

    def test_chown(self):
        output = self.emulator.chown("file1.txt", 1001)
        self.assertEqual(output, "Simulated owner of file1.txt changed to 1001")
        self.assertEqual(self.emulator.file_owners["file1.txt"], 1001)

        output = self.emulator.chown("nonexistent.txt", 1001)
        self.assertEqual(output, "File not found")

    def test_exit(self):
        output = self.emulator.exit()
        self.assertEqual(output, "Exiting shell emulator.")

    def test_log_action(self):
        self.emulator.log_action("test_command")
        with open(self.log_path, "r") as f:
            log_data = json.load(f)
        self.assertEqual(len(log_data), 1)
        self.assertEqual(log_data[0]["command"], "test_command")
        self.assertIn("timestamp", log_data[0])

if __name__ == "__main__":
    unittest.main()
