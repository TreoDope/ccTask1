import os
import json
import tarfile
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog

class ShellEmulator:
    def __init__(self, vfs_path, log_path):
        self.vfs_path = vfs_path
        self.log_path = log_path
        self.current_dir = "/"
        self.log_data = []
        self.file_owners = {}

        with tarfile.open(vfs_path, "r") as tar:
            tar.extractall("virtual_fs")

    def log_action(self, command):
        action = {
            "command": command,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.log_data.append(action)
        with open(self.log_path, "w") as f:
            json.dump(self.log_data, f, indent=4)

    def ls(self):
        path = os.path.join("virtual_fs", self.current_dir.strip("/"))
        if os.path.exists(path):
            files = os.listdir(path)
            output = " ".join(files)
        else:
            output = "Directory not found"
        self.log_action("ls")
        return output

    def cd(self, directory):
        if directory == "..":
            if self.current_dir != "/":
                # Переход на уровень выше
                self.current_dir = os.path.dirname(self.current_dir)
            output = "Changed to parent directory"
        else:
            new_dir = os.path.join(self.current_dir, directory)
            path = os.path.join("virtual_fs", new_dir.strip("/"))
            if os.path.isdir(path):
                self.current_dir = new_dir
                output = f"Changed directory to {directory}"
            else:
                output = "No such directory"
        self.log_action(f"cd {directory}")
        return output

    def tac(self, filename):
        path = os.path.join("virtual_fs", self.current_dir.strip("/"), filename)
        try:
            with open(path, "r") as file:
                lines = file.readlines()
                output = "".join(lines)
                output = output[::-1]
        except FileNotFoundError:
            output = "File not found"
        self.log_action(f"tac {filename}")
        return output

    def chown(self, filename, owner):
        path = os.path.join("virtual_fs", self.current_dir.strip("/"), filename)
        if os.path.exists(path):
            self.file_owners[filename] = owner
            output = f"Simulated owner of {filename} changed to {owner}"
        else:
            output = "File not found"
        self.log_action(f"chown {filename} {owner}")
        return output

    def exit(self):
        output = "Exiting shell emulator."
        self.log_action("exit")
        return output


class ShellGUI:
    def __init__(self, emulator):
        self.emulator = emulator
        self.window = tk.Tk()
        self.window.title("Shell Emulator")

        self.output = tk.Text(self.window, width=60, height=20, wrap="word")
        self.output.pack()

        self.entry = tk.Entry(self.window, width=50)
        self.entry.pack()
        self.entry.bind("<Return>", self.execute_command)

    def execute_command(self, event):
        command = self.entry.get()
        self.entry.delete(0, tk.END)
        self.output.insert(tk.END, command + "\n")
        output = ""

        if command.startswith("ls"):
            output = self.emulator.ls()
        elif command.startswith("cd"):
            _, dir_name = command.split(maxsplit=1)
            output = self.emulator.cd(dir_name)
        elif command.startswith("tac"):
            _, filename = command.split(maxsplit=1)
            output = self.emulator.tac(filename)
        elif command.startswith("chown"):
            _, filename, owner = command.split(maxsplit=2)
            output = self.emulator.chown(filename, int(owner))
        elif command == "exit":
            output = self.emulator.exit()
            self.window.quit()

        self.output.insert(tk.END, output + "\n")  # Вывод результата в Text
        self.output.see(tk.END)  # Прокрутка к последнему выводу

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: shell_emulator.py <path_to_vfs_tar> <path_to_log_file>")
        sys.exit(1)

    vfs_path = sys.argv[1]
    log_path = sys.argv[2]

    emulator = ShellEmulator(vfs_path, log_path)
    gui = ShellGUI(emulator)
    gui.run()
