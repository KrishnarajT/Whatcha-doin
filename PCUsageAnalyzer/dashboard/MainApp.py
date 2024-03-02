# import application class
import pandas as pd
import datetime
import pygetwindow as gw
import pyautogui as pag
import os
from collections import Counter
import sys
import pytz


class MainApplication:

    def __init__(self):
        self.thread_interval_s = 1
        self.registration_interval_s = 10
        self.record = False
        self.counter = Counter()
        self.start_time_dict = {}
        self.finish = False
        self.data_directory = os.path.join(
            os.path.expanduser("~\Documents"), "PC Usage Analyzer Data"
        )
        self.cursor_position = pag.position()
        self.cursor_counter = 0
        self.idle_detection = False
        print("Idle Detection is Disabled by default.")
        self.init_db()

    def clean_string(self, given_string):
        if given_string == "":
            given_string = "Desktop"
        if "," in given_string:
            given_string = given_string.replace(",", " ")

        # if there are any non ascii characters, remove them
        try:
            given_string = "".join(i for i in given_string if ord(i) < 128)
        except Exception as e:
            print(e)
        return given_string

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
                try:
                    self.db = pd.read_csv(
                        os.path.join(self.data_directory, "data.csv"),
                        dtype={
                            "Title": str,
                            "Start Time": int,
                            "Registered End Time": int,
                            "Real Duration": str,
                        },
                    )
                except Exception as e:
                    print(e)
                    if (
                        self.db["Start Time"].dtype != "int64"
                        or self.db["Registered End Time"].dtype != "int64"
                    ):
                        self.db = pd.read_csv(
                            os.path.join(self.data_directory, "data.csv")
                        )
                        # convert to unix time
                        self.db["Start Time"] = (
                            pd.to_datetime(self.db["Start Time"]).astype("int64")
                            / 10**9
                        )
                        self.db["Registered End Time"] = (
                            pd.to_datetime(self.db["Registered End Time"]).astype(
                                "int64"
                            )
                            / 10**9
                        )
                    raise Exception("Could not convert time to datetime, trying json")

                print("imported data")
                # print(self.db)

                try:
                    # find sum of duration
                    self.db["Real Duration"] = pd.to_timedelta(self.db["Real Duration"])
                    print("total duration", self.db["Real Duration"].sum())
                except Exception as e:
                    print(e)
                    print("could not convert duration to timedelta")
            else:
                print("no data to import, starting fresh")
                raise Exception("Trying to find json file.")

        except Exception as e:
            print(e)
            print("could not read csv due to some issues")
            # check json
            if os.path.exists(os.path.join(self.data_directory, "data.json")):
                # Read the JSON file
                data = pd.read_json(
                    os.path.join(self.data_directory, "data.json"),
                    dtype={
                        "Title": str,
                        "Start Time": int,
                        "Registered End Time": int,
                        "Real Duration": int,
                    },
                )

                self.db = data

                print(self.db.dtypes)
                print(self.db.iloc[0])

                # also convert duration to timedelta objects from seconds
                self.db["Real Duration"] = pd.to_timedelta(
                    self.db["Real Duration"] / 1000, unit="s"
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
            active_window_title = self.clean_string(active_window.title)
            return active_window_title
        except Exception as e:
            print(e)
            return "Sleeping"

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
            self.start_time_dict[active_window] = (
                datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                .replace(microsecond=0)
                .timestamp(),
            )[0]
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
                datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                .replace(microsecond=0)
                .timestamp(),
                self.duration,
            ]

            # add next row to the dataframe
            self.db.loc[len(self.db)] = new_row
            # print("self", self.db)

            # reset the counter
            self.counter[active_window] = 0
            self.start_time_dict[active_window] = (
                datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                .replace(microsecond=0)
                .timestamp(),
            )[0]

            # if len of db is a multiple of 500, autosave
            if (len(self.db)) % 500 == 0 and len(self.db) != 0:
                print("Autosaving after 500 records.")
                self.export_raw()
                if len(self.db) == 20000:
                    print("Maximum records reached. Will start fresh.")
                    # export raw, but with a different name
                    self.export_raw(
                        new_name=True,
                        name=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
                    )
                    self.export_collaborative_data(
                        new_name=True,
                        name=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
                    )
                    # start fresh
                    self.start_fresh()

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

        # clear class variables
        self.db = pd.DataFrame(
            columns=["Title", "Start Time", "Registered End Time", "Real Duration"]
        )
        self.counter = Counter()
        self.start_time_dict = {}
        self.record = False
        self.finish = False

        print("cleaned up")

    # export raw data
    def export_raw(self, new_name=False, name="new_data"):
        """
        Exports the database to a CSV file.
        """
        # print(self.db.dtypes)
        # print(self.db.iloc[0])
        # Create the data directory if it does not exist

        if not new_name:
            current_name = "data"
        else:
            current_name = name

        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        print("data directory", self.data_directory)

        # Check if the dataframe is empty
        if self.db.empty:
            print("No data to save")
            return

        # Save the dataframe to a file
        self.db.to_csv(
            os.path.join(self.data_directory, f"{current_name}.csv"), index=False
        )
        print("Saved to ", os.path.join(self.data_directory, f"{current_name}.csv"))

        # export to json
        self.db.to_json(
            os.path.join(self.data_directory, f"{current_name}.json"), orient="records"
        )
        print("Saved to ", os.path.join(self.data_directory, f"{current_name}.json"))

        # Convert column to human-readable format
        temp_db = self.db.copy()
        temp_db["Start Time"] = temp_db["Start Time"].apply(
            lambda x: datetime.datetime.fromtimestamp(x).strftime("%d %B %Y %H:%M:%S")
        )
        temp_db["Registered End Time"] = temp_db["Registered End Time"].apply(
            lambda x: datetime.datetime.fromtimestamp(x).strftime("%d %B %Y %H:%M:%S")
        )
        # Export to HTML
        temp_db.to_html(os.path.join(self.data_directory, f"{current_name}.html"))
        print("Saved to ", os.path.join(self.data_directory, f"{current_name}.html"))

        # delete space occupied by temp_db
        del temp_db
        # print(self.db.dtypes)
        # print(self.db.iloc[0])

    # export collaborative data
    def export_collaborative_data(self, new_name=False, name="new_cdata"):
        """
        Exports the database to a collaborative data file.
        """

        if not new_name:
            current_name = "collaborative_data"
        else:
            current_name = "collaborative_data" + name

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

        # print(self.db.dtypes)

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
            os.path.join(self.data_directory, f"{current_name}.csv"), index=False
        )
        new_db.to_json(
            os.path.join(self.data_directory, f"{current_name}.json"),
            orient="records",
        )
        # convert datetime to human readable format
        new_db["Start Time"] = new_db["Start Time"].apply(
            lambda x: datetime.datetime.fromtimestamp(x).strftime("%d %B %Y %H:%M:%S")
        )
        new_db["Registered End Time"] = new_db["Registered End Time"].apply(
            lambda x: datetime.datetime.fromtimestamp(x).strftime("%d %B %Y %H:%M:%S")
        )
        new_db.to_html(os.path.join(self.data_directory, f"{current_name}.html"))

        print("Saved to ", os.path.join(self.data_directory, f"{current_name}.csv"))
        print("in csv, json, and html")
        del new_db

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

    def get_finish(self):
        return self.finish

    def get_db(self):
        return self.db

    def print_db(self):
        print(self.get_record())
        print(self.db.tail(30))
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

    def set_finish(self, finish):
        self.finish = finish
