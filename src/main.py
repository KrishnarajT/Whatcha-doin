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


def clean_string(string):
    # convert to utf-8
    string = string.encode("utf-8", "ignore").decode("utf-8")
    return string


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
        self.data_directory = os.path.join(
            os.path.expanduser("~\Documents"), "Whatcha Doin Data"
        )
        self.cursor_position = pag.position()
        self.cursor_counter = 0
        self.idle_detection = False
        print("Idle Detection is Disabled by default.")
        self.init_db()

    def flip_idle_detection(self):
        self.idle_detection = not self.idle_detection

    def get_idle_detection(self):
        return self.idle_detection

    def init_db(self):
        """
        Initializes the database.
        """
        self.db = pd.DataFrame(
            columns=["Title", "Start Time", "Registered End Time", "Real Duration"]
        )

        # check if the data directory exists
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        print("data directory", self.data_directory)

        # try to get data
        try:
            # if the csv file exists, import it to self.db
            if os.path.exists(os.path.join(self.data_directory, "data.csv")):
                with open(os.path.join(self.data_directory, "data.csv"), "r") as f:
                    if (
                        os.stat(os.path.join(self.data_directory, "data.csv")).st_size
                        == 0
                    ):
                        print("File is empty")
                        print("no data to import, starting fresh")
                        return
                self.db = pd.read_csv(
                    os.path.join(self.data_directory, "data.csv"),
                    dtype={
                        "Title": str,
                        "Start Time": str,
                        "Registered End Time": str,
                        "Real Duration": str,
                    },
                )
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

        except Exception as e:
            print(e)
            print("could not read csv due to some issues")
            # check json
            if os.path.exists(os.path.join(self.data_directory, "data.json")):
                # Read the JSON file
                data = pd.read_json("data.json")

                # Create a DataFrame from the JSON data
                df = pd.DataFrame(data)

                # Append the DataFrame to the existing database
                self.db = self.db.append(df, ignore_index=True)

                # convert all time values from unix time to datetime.datetime.now() object
                self.db["Start Time"] = pd.to_datetime(self.db["Start Time"], unit="s")

                # also convert duration to timedelta objects from seconds
                self.db["Real Duration"] = datetime.timedelta(
                    seconds=self.db["Real Duration"]
                )
                print("read json")
            else:
                print("no data to import, starting fresh")

    def start_fresh(self):
        """
        Starts a fresh database.
        """
        self.db = pd.DataFrame(
            columns=["Title", "Start Time", "Registered End Time", "Real Duration"]
        )
        print("Will start fresh")

    def get_active_window(self):
        """
        Gets the active window.

        Returns:
            str: The title of the active window.
        """
        try:
            active_window = gw.getActiveWindow()
            if active_window.title == "":
                return "Desktop"
            if "," in active_window.title:
                return " ".join(active_window.title.split(","))
            return active_window.title
        except Exception as e:
            print(e)
            return "Unknown"

    def run(self):
        """
        Runs the application. This runs every thread_interval_s seconds from the thread.
        """
        # Get the active window
        active_window = self.get_active_window()

        if self.idle_detection:
            if self.cursor_position == pag.position():
                self.cursor_counter += 1
            else:
                self.cursor_position = pag.position()
                self.cursor_counter = 0
            if self.cursor_counter > 300:
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

            new_row = [
                active_window,
                self.start_time_dict[active_window],
                datetime.datetime.now(),
                self.duration,
            ]

            # add next row to the dataframe
            self.db.loc[len(self.db)] = new_row
            # print("self", self.db)

            # reset the counter
            self.counter[active_window] = 0
            self.start_time_dict[active_window] = datetime.datetime.now()

            # if len of db is a multiple of 500, autosave
            if (len(self.db)) % 500 == 0 and len(self.db) != 0:
                print("Autosaving after 500 records.")
                self.export_raw()

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
        # save the data
        # Create the data directory if it does not exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        print("data directory", self.data_directory)

        # Check if the dataframe is empty
        if self.db.empty:
            print("No data to save")
            return

        # Save the dataframe to a file
        self.db.to_csv(os.path.join(self.data_directory, "data.csv"), index=False)
        print("Saved to ", os.path.join(self.data_directory, "data.csv"))

        print("cleaned up")

    # export raw data
    def export_raw(self):
        """
        Exports the database to a CSV file.
        """

        # Create the data directory if it does not exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        print("data directory", self.data_directory)

        # Check if the dataframe is empty
        if self.db.empty:
            print("No data to save")
            return

        # Save the dataframe to a file
        self.db.to_csv(os.path.join(self.data_directory, "data.csv"), index=False)
        print("Saved to ", os.path.join(self.data_directory, "data.csv"))

        # export to json
        self.db.to_json(
            os.path.join(self.data_directory, "data.json"), orient="records"
        )
        print("Saved to ", os.path.join(self.data_directory, "data.json"))

        # export to html
        self.db.to_html(os.path.join(self.data_directory, "data.html"))
        print("Saved to ", os.path.join(self.data_directory, "data.html"))

    # export collaborative data
    def export_collaborative_data(self):
        """
        Exports the database to a collaborative data file.
        """
        # Create the data directory if it does not exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        print("data directory", self.data_directory)

        # Check if the dataframe is empty
        if self.db.empty:
            print("No data to save")
            return

        new_db = pd.DataFrame(
            columns=["Title", "Start Time", "Registered End Time", "Real Duration"]
        )

        # find similar columns in self.db, and add the duration to append to newdb
        # find all unique titles in self.db
        unique_titles = self.db["Title"].unique()
        # print("unique titles", unique_titles)

        # iterate through all unique titles in self.db
        for i in unique_titles:
            # find all rows with the same title
            rows = self.db.loc[self.db["Title"] == i]
            # print("rows", rows)
            # find the sum of the duration of all rows
            duration = rows["Real Duration"].sum()
            # print("duration", duration)
            # add the duration to new_db
            # print(len(new_db), i, rows.iloc[0]["Start Time"], rows.iloc[-1]["Registered End Time"], duration)
            new_db.loc[len(new_db)] = [
                i,
                rows.iloc[0]["Start Time"],
                rows.iloc[-1]["Registered End Time"],
                duration,
            ]

        # print(new_db)
        # sort newdb by duration
        new_db = new_db.sort_values(
            by="Real Duration", ascending=False, ignore_index=True
        )
        # save new db in all formats
        new_db.to_csv(
            os.path.join(self.data_directory, "collaborative_data.csv"), index=False
        )
        new_db.to_json(
            os.path.join(self.data_directory, "collaborative_data.json"),
            orient="records",
        )
        new_db.to_html(os.path.join(self.data_directory, "collaborative_data.html"))

        print("Saved to ", os.path.join(self.data_directory, "collaborative_data.csv"))
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
        print(self.db.tail(30))
        # print("counter is", self.counter)

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
        user_input = input(
            "Enter \n'1' to Play / Pause, \n'2' to start a blank file, \n'3' to export raw data to CSV, JSON, HTML\n'4' Export Nicely to CSV, JSON, HTML \n'5' to Enable/Disable Idle Detection\n'6' to Exit: \n\n\n"
        )

        try:
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
                app.flip_idle_detection()
                print(
                    "Idle detection is",
                    (
                        "Enabled. If you cursor doesnt move for 5 mins, you are idle. "
                        if app.get_idle_detection()
                        else "Disabled"
                    ),
                )
            elif user_input == "6":
                # End the application
                app.finish = True
                break
            else:
                print("Invalid input. Please try again.")
        except Exception as e:
            print(e)
            print(e.with_traceback())
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
    print(
        Fore.BLUE
        + Style.BRIGHT
        + r"""
    /$$      /$$ /$$                   /$$               /$$                             /$$           /$$          
    | $$  /$ | $$| $$                  | $$              | $$                            | $$          |__/          
    | $$ /$$$| $$| $$$$$$$   /$$$$$$  /$$$$$$    /$$$$$$$| $$$$$$$   /$$$$$$         /$$$$$$$  /$$$$$$  /$$ /$$$$$$$ 
    | $$/$$ $$ $$| $$__  $$ |____  $$|_  $$_/   /$$_____/| $$__  $$ |____  $$       /$$__  $$ /$$__  $$| $$| $$__  $$
    | $$$$_  $$$$| $$  \ $$  /$$$$$$$  | $$    | $$      | $$  \ $$  /$$$$$$$      | $$  | $$| $$  \ $$| $$| $$  \ $$
    | $$$/ \  $$$| $$  | $$ /$$__  $$  | $$ /$$| $$      | $$  | $$ /$$__  $$      | $$  | $$| $$  | $$| $$| $$  | $$
    | $$/   \  $$| $$  | $$|  $$$$$$$  |  $$$$/|  $$$$$$$| $$  | $$|  $$$$$$$      |  $$$$$$$|  $$$$$$/| $$| $$  | $$
    |__/     \__/|__/  |__/ \_______/   \___/   \_______/|__/  |__/ \_______/       \_______/ \______/ |__/|__/  |__/                                                                                                                                                                        
    """
        + Style.RESET_ALL
    )
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
