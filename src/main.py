# import application class
import pandas as pd
import datetime
import pygetwindow as gw
import schedule
import time
import threading 
from colorama import init, Fore, Style
import os
from collections import Counter
class MainApplication:

    def __init__(self):
        self.thread_interval_s = 10
        self.checking_interval_s = 1
        self.record = False
        self.counter = Counter()
        self.start_time_dict = {}
        self.db = pd.DataFrame(columns=["Title", "Start Time", "Registerd End Time", "Real Duration"])
    
    def get_active_window(self):
        """
        Gets the active window.

        Returns:
            str: The title of the active window.
        """
        active_window = gw.getActiveWindow()
        return active_window.title

    def run(self):
        """
        Runs the application. This runs every thread_interval_s seconds from the thread. 
        """
        # Get the active window
        active_window = self.get_active_window()
        print(active_window)
        # Update the counter
        if self.counter.get(active_window, 0) == 0:
            self.counter[active_window] = 0
            self.start_time_dict[active_window] = datetime.datetime.now()
        else:
            self.counter[active_window] += 1
        print(self.counter)
        # check if the counter value is more than checking_interval_s
        if self.counter[active_window] > self.checking_interval_s:
            # convert counter seconds into datetime object
            self.duration = datetime.timedelta(seconds=self.counter[active_window])
            
            # append to dateframe
            self.db = self.db.append({"Title": active_window, "Start Time": self.start_time_dict[active_window], "Registerd End Time": datetime.datetime.now(), "Real Duration": self.duration}, ignore_index=True)
            
            # reset the counter
            self.counter[active_window] = 0
                
    def pause_or_resume(self):
        """
        Pauses or resumes the application.
        """
        if self.record == True:
            self.record = False
        else:
            self.record = True

    def cleanup(self):
        """
        Cleans up the application.
        """
        pass
    
    # getter functions
    def get_thread_interval_s(self):
        return self.thread_interval_s
    
    def get_checking_interval_s(self):
        return self.checking_interval_s
    
    def get_record(self):
        return self.record
    
    def get_counter(self):
        return self.counter
    
    def get_start_time_dict(self):
        return self.start_time_dict
    
    def get_db(self):
        return self.db
    
    def print_db(self):
        print(self.db)
    
    # setter functions
    def set_thread_interval_s(self, thread_interval_s):
        self.thread_interval_s = thread_interval_s
        
    def set_checking_interval_s(self, checking_interval_s):
        self.checking_interval_s = checking_interval_s
    
    def set_record(self, record):
        self.record = record
    
    def set_counter(self, counter):
        self.counter = counter
    
    def set_db(self, db):
        self.db = db
    
    def set_start_time_dict(self, start_time_dict):
        self.start_time_dict = start_time_dict
    
app = MainApplication()

def user_io():
    """
    Manages user input and output.
    """
    while True:
        # Initialize colorama
        init()

        # Print welcome message in ASCII art
        print(Fore.BLUE + Style.BRIGHT + r"""

        ░  ░░░░  ░░        ░░  ░░░░░░░░░      ░░░░      ░░░  ░░░░  ░░        ░
        ▒  ▒  ▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒   ▒▒   ▒▒  ▒▒▒▒▒▒▒
        ▓        ▓▓      ▓▓▓▓  ▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓        ▓▓      ▓▓▓
        █   ██   ██  ████████  ████████  ████  ██  ████  ██  █  █  ██  ███████
        █  ████  ██        ██        ███      ████      ███  ████  ██        █
                                                                            
        """ + Style.RESET_ALL)

        user_input = input("Enter \n'1' to begin \n'2' to end, \n'3' to start a blank file, \n'4' to export to CSV, \n'5' to export to JSON, \n'6' to export to HTML, or \n'7' to end: ")
        
        if user_input == "0":
            app.print_db()
        elif user_input == "1":
            app.run()
        elif user_input == "2":
            app.pause_or_resume()
        elif user_input == "3":
            # Start a blank file
            # Code to start a blank file
            pass
        elif user_input == "4":
            # Export to CSV
            # Code to export to CSV
            pass
        elif user_input == "5":
            # Export to JSON
            # Code to export to JSON
            pass
        elif user_input == "6":
            # Export to HTML
            # Code to export to HTML
            pass
        elif user_input == "7":
            # End the application
            break
        else:
            print("Invalid input. Please try again.")
            
    app.cleanup()
    
def core():
    """
    Manages the core logic of the application.
    """
    
    while True:
        if app.get_record() == True:
            schedule.run_pending()
        time.sleep(app.thread_interval_s)

if __name__ == "__main__":
    schedule.every(app.thread_interval_s).seconds.do(app.run)
    # manage threads
    # thread 1 for running user io
    user_thread = threading.Thread(target=user_io)
    # thread 2 for running core logic
    core_thread = threading.Thread(target=core)

    # Start the threads
    user_thread.start()
    core_thread.start()
