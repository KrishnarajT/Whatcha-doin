# import application class
import pandas as pd
import datetime
import pygetwindow as gw
import pyautogui as pag
import schedule
import time
import threading 
from colorama import init, Fore, Style
import os
from collections import Counter
import sys

def recording_indicator():
    while app.get_record():
        print("\rRecording", end="")
        for _ in range(3):
            if not app.get_record():
                break
            print(".", end="")
            sys.stdout.flush()
            time.sleep(0.5)
        print("\rRecording   ", end="")
        sys.stdout.flush()
    print("Paused   ", end="")
    sys.stdout.flush()

        
class MainApplication:

    def __init__(self):
        self.thread_interval_s = 1
        self.registration_interval_s = 10
        self.record = False
        self.counter = Counter()
        self.start_time_dict = {}
        self.finish = False
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.data_directory = os.path.join(os.path.dirname(self.script_directory), 'data')
        self.cursor_position = pag.position()
        self.cursor_counter = 0
        self.init_db()
        
    def init_db(self):
        """
        Initializes the database.
        """
        self.db = pd.DataFrame(columns=["Title", "Start Time", "Registerd End Time", "Real Duration"])
        
        # check if the data directory exists
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        print("data directory", self.data_directory)
        
        # if the csv file exists, import it to self.db
        if os.path.exists(os.path.join(self.data_directory, "data.csv")):
            self.db = pd.read_csv(os.path.join(self.data_directory, "data.csv"), dtype={"Title": str, "Start Time": str, "Registered End Time": str, "Real Duration": str})
            print("imported data")
            
            try:
                # find sum of duration
                self.db["Real Duration"] = pd.to_timedelta(self.db["Real Duration"])
                print("imported data")
                print("total duration", self.db["Real Duration"].sum())
            except Exception as e:
                print(e)
                print("could not convert duration to timedelta")
        else:
            print("no data to import, starting fresh")
        
    def start_fresh(self):
        """
        Starts a fresh database.
        """
        self.db = pd.DataFrame(columns=["Title", "Start Time", "Registerd End Time", "Real Duration"])
        print("Will start fresh")
    
    def get_active_window(self):
        """
        Gets the active window.

        Returns:
            str: The title of the active window.
        """
        active_window = gw.getActiveWindow()
        if not active_window:
            return "Unknown"
        return active_window.title

    def run(self):
        """
        Runs the application. This runs every thread_interval_s seconds from the thread. 
        """
        # Get the active window
        active_window = self.get_active_window()
        if self.cursor_position == pag.position():
            self.cursor_counter += 1
        else:
            self.cursor_position = pag.position()
            self.cursor_counter = 0
        if self.cursor_counter > 100:
            active_window = "idle"
        # print(active_window)
        # Update the counter
        if active_window not in self.counter:
            # print("new window")
            self.counter[active_window] = 0
            self.start_time_dict[active_window] = datetime.datetime.now()
        else:
            # print("old window")
            self.counter.update([active_window])
        # print(self.counter)
        # check if the counter value is more than checking_interval_s
        if self.counter[active_window] >= self.registration_interval_s:
            # convert counter seconds into datetime object
            self.duration = datetime.timedelta(seconds=self.counter[active_window])
            
            new_row = [active_window, self.start_time_dict[active_window], datetime.datetime.now(), self.duration]
            
            # add next row to the dataframe
            self.db.loc[len(self.db)] = new_row
            # print("self", self.db)
            
            # reset the counter
            self.counter[active_window] = 0
            self.start_time_dict[active_window] = datetime.datetime.now()
                
    def pause_or_resume(self):
        """
        Pauses or resumes the application.
        """
        if self.record == True:
            self.record = False
            sys.stdout.flush()
        else:
            self.record = True

    def cleanup(self):
        """
        Cleans up the application.
        """
        # clear the schedule
        schedule.clear()
        
        print(self.script_directory)
        
        # Define the data directory
        data_directory = os.path.join(os.path.dirname(self.script_directory), 'data')
        
        # Create the data directory if it does not exist
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        print("data directory", data_directory)
        
        # Check if the dataframe is empty
        if self.db.empty:
            print("No data to save")
            return
        
        # Save the dataframe to a file
        self.db.to_csv(os.path.join(data_directory, "data.csv"), index=False)
        print("Saved to ", os.path.join(data_directory, "data.csv"))

        print("cleaned up")
    
    # export raw data
    def export_raw(self):
        """
        Exports the database to a CSV file.
        """
        # Define the data directory
        data_directory = os.path.join(os.path.dirname(self.script_directory), 'data')
        
        # Create the data directory if it does not exist
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        print("data directory", data_directory)
        
        # Check if the dataframe is empty
        if self.db.empty:
            print("No data to save")
            return
        
        # Save the dataframe to a file
        self.db.to_csv(os.path.join(data_directory, "data.csv"), index=False)
        print("Saved to ", os.path.join(data_directory, "data.csv"))
        
        # export to json
        self.db.to_json(os.path.join(data_directory, "data.json"), orient="records")
        print("Saved to ", os.path.join(data_directory, "data.json"))
        
        # export to html
        self.db.to_html(os.path.join(data_directory, "data.html"))
        print("Saved to ", os.path.join(data_directory, "data.html"))
        
    # export collaborative data
    def export_collaborative_data(self):
        """
        Exports the database to a collaborative data file.
        """
        # Define the data directory
        data_directory = os.path.join(os.path.dirname(self.script_directory), 'data')
        
        # Create the data directory if it does not exist
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        print("data directory", data_directory)
        
        # Check if the dataframe is empty
        if self.db.empty:
            print("No data to save")
            return
        
        new_db = pd.DataFrame(columns=["Title", "Start Time", "Registerd End Time", "Real Duration"])
        
        # find similar columns in self.db, and add the duration to append to newdb
        # find all unique titles in self.db
        unique_titles = self.db["Title"].unique()
        print("unique titles", unique_titles)
        
        # iterate through all unique titles in self.db
        for i in unique_titles:
            # find all rows with the same title
            rows = self.db.loc[self.db["Title"] == i]
            print("rows", rows)
            # find the sum of the duration of all rows
            duration = rows["Real Duration"].sum()
            print("duration", duration)
            # add the duration to new_db
            new_db.loc[len(new_db)] = [i, rows.iloc[0]["Start Time"], rows.iloc[-1]["Registerd End Time"], duration]

        print(new_db)
        
        # save new db in all formats
        new_db.to_csv(os.path.join(data_directory, "collaborative_data.csv"), index=False)
        new_db.to_json(os.path.join(data_directory, "collaborative_data.json"), orient="records")
        new_db.to_html(os.path.join(data_directory, "collaborative_data.html"))
        
        print("Saved to ", os.path.join(data_directory, "collaborative_data.csv"))
        print("in csv, json, and html")
    
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
        print("counter is", self.counter)
    
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
        user_input = input("Enter \n'1' to Play / Pause, \n'2' to start a blank file, \n'3' to export raw data to CSV, JSON, HTML\n'4' Export Nicely to CSV, JSON, HTML \n'5' to end: \n\n\n ")
        
        if user_input == "0":
            app.print_db()
        elif user_input == "1":
            app.pause_or_resume()
            if app.get_record() == True:
                print("Recording ...")
            else:
                print("Paused")
        elif user_input == "2":
            app.start_fresh()
        elif user_input == "3":
            app.export_raw()
        elif user_input == "4":
            app.export_collaborative_data()
        elif user_input == "5":
            # End the application
            app.finish = True
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
            # print("next job", schedule.next_run())
        if app.finish == True:
            break
        time.sleep(app.thread_interval_s)
    print("done with core logic")

if __name__ == "__main__":
    # Initialize colorama
    init()

    # Print welcome message in ASCII art
    print(Fore.BLUE + Style.BRIGHT + r"""
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░  ░░░░  ░░  ░░░░  ░░░      ░░░        ░░░      ░░░  ░░░░  ░░░      ░░░░░░░░░       ░░░░      ░░░        ░░   ░░░  ░
    ▒  ▒  ▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒▒▒▒  ▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒▒▒▒  ▒▒▒▒▒    ▒▒  ▒
    ▓        ▓▓        ▓▓  ▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓▓▓▓▓        ▓▓  ▓▓▓▓  ▓▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓▓  ▓  ▓  ▓
    █   ██   ██  ████  ██        █████  █████  ████  ██  ████  ██        ████████  ████  ██  ████  █████  █████  ██    █
    █  ████  ██  ████  ██  ████  █████  ██████      ███  ████  ██  ████  ████████       ████      ███        ██  ███   █
    ████████████████████████████████████████████████████████████████████████████████████████████████████████████████████                                                                    
    """ + Style.RESET_ALL)
    schedule.every(app.thread_interval_s).seconds.do(app.run)
    # manage threads
    # thread 1 for running user io
    user_thread = threading.Thread(target=user_io)
    # thread 2 for running core logic
    core_thread = threading.Thread(target=core)

    try:
            
        # Start the threads
        user_thread.start()
        core_thread.start()

        # print("Threads have started")
        user_thread.join()
        core_thread.join()
    except KeyboardInterrupt:
        # cleanly exit the application
        app.cleanup()
        print("Application has ended")
        os._exit(0)    
    except Exception as e:
        print(e)
        # cleanly exit the application
        app.cleanup()
        print("Application has ended")
        os._exit(0)
    # cleanly exit the application
    print("Application has ended")
    os._exit(0)