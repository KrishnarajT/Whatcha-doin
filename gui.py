import tkinter as tk
import subprocess
import os


class DjangoServerControl(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Django Server Control")
        self.geometry("200x150")
        self.server_process = None

        self.start_button = tk.Button(
            self, text="Start Server", command=self.start_server
        )
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(
            self, text="Stop Server", command=self.stop_server, state=tk.DISABLED
        )
        self.stop_button.pack(pady=10)

        # tell that server will start at localhost 8000
        self.label = tk.Label(self, text="Server will start at localhost:8000")
        self.label.pack(pady=10)

    def start_server(self):
        if self.server_process is None:
            os.chdir("PCUsageAnalyzer")
            print(os.getcwd())
            self.server_process = subprocess.Popen(["python", "manage.py", "runserver"])
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_server(self):
        # stop everything and exit everything
        if self.server_process is not None:
            self.server_process.terminate()
            self.server_process = None
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

        # exit this program
        self.destroy()
        # exit the main program
        os._exit(0)


if __name__ == "__main__":
    app = DjangoServerControl()
    app.mainloop()
