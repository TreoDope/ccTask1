import tarfile
import json
import os
import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

class VirtualShell:
    def __init__(self, tar_path, log_path):
        self.tar_path = tar_path
        self.log_path = log_path
        self.tar = tarfile.open(tar_path, 'r')
        self.current_path = ''
        self.log = []

    def log_action(self, action):
        timestamp = datetime.datetime.now().isoformat()
        self.log.append({'timestamp': timestamp, 'action': action})
        with open(self.log_path, 'w') as log_file:
            json.dump(self.log, log_file, indent=4)

    def ls(self):
        members = self.tar.getmembers()
        current_dir = self.current_path.strip('/')
        if current_dir:
            current_dir += '/'
        result = [member.name.split('/')[-1] for member in members if member.name.startswith(current_dir) and '/' not in member.name[len(current_dir):]]
        return result

    def cd(self, path):
        if path == '..':
            if self.current_path:
                self.current_path = '/'.join(self.current_path.strip('/').split('/')[:-1])
        else:
            new_path = os.path.join(self.current_path, path).strip('/')
            new_path = new_path.replace('\\', '/')
            if new_path.startswith('/'):
                new_path = new_path[1:]
            if any(member.name.startswith(new_path + '/') or member.name == new_path for member in self.tar.getmembers()):
                self.current_path = new_path
            else:
                return f'Path {path} not found'
        return 'Changed directory to ' + self.current_path.split("/")[-1]

    def tac(self, file_path):
        try:
            if (self.current_path == ""):
                file_path = file_path
            else:
                file_path = "/" + file_path
            file = self.tar.extractfile(self.current_path + file_path)
            if file:
                lines = file.read().decode().splitlines()
                return lines[0][::-1]
            else:
                return f'File {file_path} not found'
        except KeyError:
            return f'File {file_path} not found'

    def chown(self, file_path, owner):
        try:
            if (self.current_path == ""):
                file_path = file_path
            else:
                file_path = "/" + file_path
            member = self.tar.getmember(self.current_path + file_path)
            member.uid = owner
            self.log_action(f'chown {file_path} {owner}')
            return f'Owner of {file_path} changed to {owner}'
        except KeyError:
            return f'File {file_path} not found'

    def exit(self):
        self.log_action('exit')
        self.tar.close()
        exit(0)

    def run(self):
        root = tk.Tk()
        root.title("Virtual Shell")
        def on_command():
            output_text.config(state=tk.NORMAL)
            command = command_entry.get()
            self.log_action(command)
            output_text.insert(tk.END, "emulatedShell@emulatedUser:~/" + self.current_path.split("/")[-1] + "$ " + command + "\n")
            if command.startswith('ls'):
                result = self.ls()
                output_text.insert(tk.END, '\n'.join(result) + '\n')
            elif command.startswith('cd'):
                _, path = command.split(maxsplit=1)
                result = self.cd(path)
                output_text.insert(tk.END, result + '\n')
            elif command.startswith('tac'):
                _, file_path = command.split(maxsplit=1)
                result = self.tac(file_path)
                output_text.insert(tk.END, result + '\n')
            elif command.startswith('chown'):
                _, file_path, owner = command.split(maxsplit=2)
                result = self.chown(owner, file_path)
                output_text.insert(tk.END, result + '\n')
            elif command.startswith('exit'):
                self.exit()
            else:
                output_text.insert(tk.END, 'Unknown command\n')
            command_entry.delete(0, tk.END)
            output_text.config(state=tk.DISABLED)
        command_entry = tk.Entry(root, width=50)
        command_entry.pack()
        command_entry.bind('<Return>', lambda event: on_command())

        output_text = tk.Text(root, height=20, width=50)
        output_text.pack()
        output_text.config(state=tk.DISABLED)
        root.mainloop()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Virtual Shell Emulator")
    parser.add_argument("tar_path", help="Path to the TAR file")
    parser.add_argument("log_path", help="Path to the log file")
    args = parser.parse_args()

    shell = VirtualShell(args.tar_path, args.log_path)
    shell.run()
