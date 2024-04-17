# import application class
import pandas as pd
import datetime
import pygetwindow as gw
import pyautogui as pag
import os
import sys
import pytz
import psutil
from ctypes import wintypes
import ctypes
import pickle

# importing for training naive bayes model
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

training_data = {
    "code": [
        "code",
        "visual studio",
        "sublime text",
        "gcc",
        "atom",
        "pycharm",
        "notepad++",
        "intellij idea",
        "netbeans",
        "eclipse",
        "android studio",
        "xcode",
        "vim",
        "emacs",
        "brackets",
        "webstorm",
        "phpstorm",
        "rubymine",
        "textmate",
        "gedit",
        "jupyter notebook",
        "spyder",
        "r studio",
        "bluej",
        "code::blocks",
        "nano",
        "visual studio code",
        "komodo edit",
        "lighttable",
        "kate",
    ],
    "design": [
        "photoshop",
        "illustrator",
        "sketch",
        "figma",
        "adobe xd",
        "indesign",
        "coreldraw",
        "gimp",
        "affinity designer",
        "canva",
        "zeplin",
        "invision studio",
        "balsamiq",
        "figjam",
        "adobe spark",
        "autodesk sketchbook",
        "lunacy",
        "gravit designer",
        "marvel app",
        "flinto",
        "sketchbook",
        "vectr",
        "affinity photo",
        "sketchup",
        "proto.io",
        "corel painter",
        "adobe animate",
        "principle",
        "adobe captivate",
        "moqups",
    ],
    "web": [
        "chrome",
        "firefox",
        "edge",
        "safari",
        "opera",
        "brave",
        "vivaldi",
        "tor browser",
        "uc browser",
        "yandex browser",
        "maxthon",
        "avant browser",
        "epic privacy browser",
        "pale moon",
        "lynx browser",
        "dolphin browser",
        "midori browser",
        "qutebrowser",
        "seamonkey",
        "comodo dragon",
        "sleipnir",
        "waterfox",
        "cyberfox",
        "beaker browser",
        "netsurf",
        "galeon",
        "konqueror",
        "rekonq",
        "arora",
        "falkon",
    ],
    "video": [
        "vlc",
        "netflix",
        "prime video",
        "youtube",
        "hulu",
        "disney+",
        "hbomax",
        "apple tv+",
        "twitch",
        "peacock",
        "crunchyroll",
        "vimeo",
        "dailymotion",
        "funimation",
        "crackle",
        "tubi",
        "hotstar",
        "sony liv",
        "voot",
        "zee5",
        "altbalaji",
        "hoichoi",
        "mx player",
        "jio cinema",
        "eros now",
        "amazon prime video",
        "google play movies",
        "itunes",
        "youtube tv",
        "sling tv",
    ],
    "music": [
        "spotify",
        "itunes",
        "soundcloud",
        "youtube music",
        "pandora",
        "amazon music",
        "google play music",
        "tidal",
        "deezer",
        "napster",
        "jiosaavn",
        "gaana",
        "wynk music",
        "hungama music",
        "spotify lite",
        "musixmatch",
        "shazam",
        "last.fm",
        "yandex music",
        "kkbox",
        "iheartradio",
        "8tracks",
        "pocketcasts",
        "podbean",
        "stitcher",
        "castbox",
        "anchor",
        "overcast",
        "radiopublic",
        "breakermag",
    ],
    "chat": [
        "whatsapp",
        "messenger",
        "slack",
        "discord",
        "telegram",
        "signal",
        "skype",
        "viber",
        "snapchat",
        "wechat",
        "line",
        "kik",
        "telegram x",
        "groupme",
        "zulip",
        "wire",
        "rocket.chat",
        "chatwork",
        "tox",
        "kakao talk",
        "discord lite",
        "discord nitro",
        "discord plus",
        "discord classic",
        "discord alpha",
        "discord beta",
        "discord canary",
        "discord ptb",
        "discord development",
        "discord test",
    ],
    "social": [
        "facebook",
        "instagram",
        "twitter",
        "linkedin",
        "reddit",
        "tumblr",
        "pinterest",
        "snapchat",
        "tiktok",
        "youtube",
        "whatsapp",
        "messenger",
        "telegram",
        "signal",
        "discord",
        "vkontakte",
        "wechat",
        "wechat lite",
        "wechat pay",
        "wechat work",
        "wechat work lite",
        "wechat reading",
        "wechat design",
        "wechat office",
        "wechat mini program",
        "wechat mini program lite",
        "wechat scan",
        "wechat games",
        "wechat video",
    ],
    "email": [
        "gmail",
        "outlook",
        "yahoo mail",
        "thunderbird",
        "mailchimp",
        "aol mail",
        "protonmail",
        "zoho mail",
        "icloud mail",
        "roundcube",
        "yandex mail",
        "tutanota",
        "fastmail",
        "gmx mail",
        "mail.com",
        "inbox.com",
        "hushmail",
        "aol desktop gold",
        "zimbra",
        "the bat!",
        "eudora",
        "postbox",
        "sylpheed",
        "claws mail",
        "evolution mail",
        "geary",
        "nylas mail",
        "eureka mail",
        "horde",
    ],
    "productivity": [
        "word",
        "excel",
        "powerpoint",
        "onenote",
        "google docs",
        "google sheets",
        "google slides",
        "google keep",
        "microsoft office",
        "libreoffice",
        "openoffice",
        "wps office",
        "zoho workplace",
        "notion",
        "evernote",
        "todoist",
        "trello",
        "asana",
        "slack",
        "microsoft teams",
        "zoom",
        "skype for business",
        "webex",
        "gotomeeting",
        "jira",
        "confluence",
        "zendesk",
        "salesforce",
        "basecamp",
    ],
}


class MainApplication:

    def __init__(self):
        self.thread_interval_ms = 1000
        self.record = False
        self.finish = False
        self.started_app = False
        self.data_directory = os.path.join(
            os.path.expanduser("~\Documents"), "PC Usage Analyzer Data"
        )
        self.cursor_position = pag.position()
        self.cursor_counter = 0
        self.idle_detection = True
        print("Idle Detection is Enabled by default.")
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

    def fix_idle(self):
        """
        Changes the previous entries summing up to 300 seconds to "idle"
        """
        # iterate backwards upto 300 entries in the dataframe.
        total_duration = pd.Timedelta(0)
        for i in range(len(self.db) - 1, len(self.db) - 300, -1):
            # keep adding duration as we go back, until it reaches 300 seconds
            total_duration += self.db.iloc[i]["Duration"]
            # if total duration is more than 300 seconds, break
            if total_duration > pd.Timedelta(seconds=300):
                break
            # change the title to "idle"
            self.db.at[i, "Title"] = "idle"

    def init_db(self):
        """
        Initializes the database. Reads the csv file named data.csv
        """
        self.db = pd.DataFrame(
            columns=[
                "Title",
                "Process Name",
                "Current Memory Usage",
                "Start Time",
                "Registered End Time",
                "Duration",
            ]
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
                            "Process Name": str,
                            "Current Memory Usage": float,
                            "Start Time": str,
                            "Registered End Time": str,
                            "Duration": str,
                        },
                    )
                except Exception as e:
                    print(e)
                    print("could not read csv due to some issues")

                print("imported data")

                try:
                    # find sum of duration
                    self.db["Duration"] = pd.to_timedelta(self.db["Duration"])
                    print("total duration", self.db["Duration"].sum())
                except Exception as e:
                    print(e)
                    print("could not convert duration to timedelta")
            else:
                print("no data to import, starting fresh")

        except Exception as e:
            print(e)
            print("could not read csv due to some issues")

    def start_fresh(self):
        """
        Starts a fresh database.
        """
        self.db = pd.DataFrame(
            columns=[
                "Title",
                "Process Name",
                "Current Memory Usage",
                "Start Time",
                "Registered End Time",
                "Duration",
            ]
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

    def get_active_process(self):
        """
        Gets the active process.

        Returns:
            str: The name of the active process.
        """
        user32 = ctypes.windll.user32
        h_wnd = user32.GetForegroundWindow()

        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))

        p = psutil.Process(pid.value)

        # Get the name of the process
        return p

    def get_active_process_memory(self, p):
        """
        Gets the active process memory usage (uss).

        Returns:
            int: the memory in mb.
        """
        # Get the memory usage of the process
        total_memory = p.memory_full_info().uss

        # Get the child processes
        children = p.children(recursive=True)

        # Add the memory usage of each child process
        for child in children:
            total_memory += child.memory_full_info().uss

        return total_memory / (1024 * 1024)

    def run(self):
        print("running main run function")
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
                # change the previous entries summing up to 300 seconds to "idle"
                self.fix_idle()

        # get the active process
        active_process = self.get_active_process()
        active_process_name = active_process.name()

        # get the memory usage of the active process
        active_process_memory = self.get_active_process_memory(active_process)

        # check if the last entry in the db is the same as the current active window
        if len(self.db) > 0:
            if self.db.iloc[-1]["Title"] == active_window:
                # just update the end time, duration and break
                self.db.at[len(self.db) - 1, "Registered End Time"] = (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                self.db.at[len(self.db) - 1, "Duration"] = datetime.timedelta(
                    seconds=self.db.at[len(self.db) - 1, "Duration"].total_seconds()
                    + self.thread_interval_ms / 1000
                )
            else:
                new_row = [
                    active_window,
                    active_process_name,
                    active_process_memory,
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    pd.Timedelta(seconds=self.thread_interval_ms / 1000),
                ]

                # add next row to the dataframe
                self.db.loc[len(self.db)] = new_row
                # print("self", self.db)

        else:
            new_row = [
                active_window,
                active_process_name,
                active_process_memory,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                pd.Timedelta(seconds=self.thread_interval_ms / 1000),
            ]

            # add next row to the dataframe
            self.db.loc[len(self.db)] = new_row

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
            columns=[
                "Title",
                "Start Time",
                "Process Name",
                "Current Memory Usage",
                "Registered End Time",
                "Duration",
            ]
        )
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

        # Export to HTML
        self.db.to_html(os.path.join(self.data_directory, f"{current_name}.html"))
        print("Saved to ", os.path.join(self.data_directory, f"{current_name}.html"))

    # getter functions
    def get_thread_interval_ms(self):
        return self.thread_interval_ms

    def get_registration_interval_ms(self):
        return self.registration_interval_ms

    def get_checking_interval_s(self):
        return self.checking_interval_s

    def get_record(self):
        return self.record

    def get_start_time_dict(self):
        return self.start_time_dict

    def get_finish(self):
        return self.finish

    def get_app_started(self):
        return self.started_app

    def get_db(self):
        return self.db

    def print_db(self):
        print(self.get_record())
        print(self.db.tail(3))

    # setter functions

    def set_app_started(self, started_app):
        self.started_app = started_app

    def set_thread_interval_ms(self, thread_interval_ms):
        self.thread_interval_ms = thread_interval_ms

    def set_registration_interval_ms(self, registration_interval_ms):
        self.registration_interval_ms = registration_interval_ms

    def set_checking_interval_s(self, checking_interval_s):
        self.checking_interval_s = checking_interval_s

    def set_record(self, record):
        self.record = record

    def set_db(self, db):
        self.db = db

    def set_start_time_dict(self, start_time_dict):
        self.start_time_dict = start_time_dict

    def set_finish(self, finish):
        self.finish = finish

    def get_intervals_ms(self):
        return {
            "thread_intervals_ms": self.thread_interval_ms,
        }

    # calculation and data processing functions

    def get_current_app_usage(self):

        # calculate current app time by iterating over the database, and summing up duration where process name is the same as the active process

        current_process = self.get_active_process()
        current_process_name = current_process.name()

        current_process_memory = self.get_active_process_memory(current_process)

        current_app_time = pd.Timedelta(0)
        for i in range(len(self.db)):
            if self.db.iloc[i]["Process Name"] == current_process_name:
                current_app_time += self.db.iloc[i]["Duration"]

        # make current app time in human readable format from pd.timedelta
        current_app_time = str(current_app_time)

        return {
            "Title": self.get_active_window(),
            "Process Name": current_process_name,
            "Current Memory Usage": current_process_memory,
            "Time": current_app_time,
        }

    def get_todays_app_usage(self):
        # returns a dictionary with x and y values for the graph
        # x is a list for todays apps process names
        # y is a list for todays apps process durations summed
        todays_apps = {}

        # get todays date
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # iterate over the database, and sum up the duration where the date is today
        for i in range(len(self.db)):
            if self.db.iloc[i]["Start Time"].split(" ")[0] == today:
                if self.db.iloc[i]["Process Name"] in todays_apps:
                    todays_apps[self.db.iloc[i]["Process Name"]] += (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )
                else:
                    todays_apps[self.db.iloc[i]["Process Name"]] = (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )

        # convert the dictionary to a dataframe
        todays_apps = pd.DataFrame(
            list(todays_apps.items()), columns=["Process", "Time"]
        )

        # sort the dataframe by time
        todays_apps = todays_apps.sort_values(by="Time", ascending=False)

        # get the top 10 apps
        todays_apps = todays_apps.head(10)

        # convert the dataframe to a dictionary
        todays_apps = todays_apps.to_dict()

        return todays_apps

    def get_hourly_pc_usage(self):
        # returns a dictionary with x and y values for the graph
        # x is a list for hours
        # y is a list for duration summed for each hour
        hourly_pc_usage = {str(i): 0 for i in range(24)}

        # this is only for today
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # iterate over the database, and sum up the duration where the date is today
        for i in range(len(self.db)):
            if self.db.iloc[i]["Start Time"].split(" ")[0] == today:
                hour = self.db.iloc[i]["Start Time"].split(" ")[1].split(":")[0]
                if hour in hourly_pc_usage:
                    hourly_pc_usage[hour] += (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )
                else:
                    hourly_pc_usage[hour] = (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )

        # convert the dictionary to a dataframe
        hourly_pc_usage = pd.DataFrame(
            list(hourly_pc_usage.items()), columns=["Hour", "Time"]
        )

        # sort the dataframe by time
        hourly_pc_usage = hourly_pc_usage.sort_values(by="Hour")

        # convert the dataframe to a dictionary
        hourly_pc_usage = hourly_pc_usage.to_dict()

        # # for any hour from 0 to 23 not present in the dictionary, add it with 0 value
        # for i in range(24):
        #     if str(i) not in hourly_pc_usage["Hour"]:
        #         hourly_pc_usage["Hour"][str(i)] = i
        #         hourly_pc_usage["Time"][str(i)] = 0

        return hourly_pc_usage

    def get_top_apps_this_week(self):
        # returns a dictionary with x and y values for the graph
        # x is a list for top apps process names
        # y is a list for top apps process durations summed
        top_apps = {}

        # get todays date
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # get the date 7 days ago
        seven_days_ago = (
            datetime.datetime.now() - datetime.timedelta(days=7)
        ).strftime("%Y-%m-%d")

        # iterate over the database, and sum up the duration where the date is between today and 7 days ago
        for i in range(len(self.db)):
            if (
                self.db.iloc[i]["Start Time"].split(" ")[0] <= today
                and self.db.iloc[i]["Start Time"].split(" ")[0] >= seven_days_ago
            ):
                if self.db.iloc[i]["Process Name"] in top_apps:
                    top_apps[self.db.iloc[i]["Process Name"]] += (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )
                else:
                    top_apps[self.db.iloc[i]["Process Name"]] = (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )

        # convert the dictionary to a dataframe
        top_apps = pd.DataFrame(list(top_apps.items()), columns=["Process", "Time"])

        # sort the dataframe by time
        top_apps = top_apps.sort_values(by="Time", ascending=False)

        # get the top 10 apps
        top_apps = top_apps.head(10)

        # convert the dataframe to a dictionary
        top_apps = top_apps.to_dict()

        return top_apps

    def get_top_apps_this_month(self):
        # returns a dictionary with x and y values for the graph
        # x is a list for top apps process names
        # y is a list for top apps process durations summed
        top_apps = {}

        # get todays date
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # get the date 30 days ago
        thirty_days_ago = (
            datetime.datetime.now() - datetime.timedelta(days=30)
        ).strftime("%Y-%m-%d")

        # iterate over the database, and sum up the duration where the date is between today and 30 days ago
        for i in range(len(self.db)):
            if (
                self.db.iloc[i]["Start Time"].split(" ")[0] <= today
                and self.db.iloc[i]["Start Time"].split(" ")[0] >= thirty_days_ago
            ):
                if self.db.iloc[i]["Process Name"] in top_apps:
                    top_apps[self.db.iloc[i]["Process Name"]] += (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )
                else:
                    top_apps[self.db.iloc[i]["Process Name"]] = (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )

        # convert the dictionary to a dataframe
        top_apps = pd.DataFrame(list(top_apps.items()), columns=["Process", "Time"])

        # sort the dataframe by time
        top_apps = top_apps.sort_values(by="Time", ascending=False)

        # get the top 10 apps
        top_apps = top_apps.head(10)

        # convert the dataframe to a dictionary
        top_apps = top_apps.to_dict()

        return top_apps

    def get_top_apps_all_time(self):
        # returns a dictionary with x and y values for the graph
        # x is a list for top apps process names
        # y is a list for top apps process durations summed
        top_apps = {}

        # iterate over the database, and sum up the duration for each process
        for i in range(len(self.db)):
            if self.db.iloc[i]["Process Name"] in top_apps:
                top_apps[self.db.iloc[i]["Process Name"]] += (
                    self.db.iloc[i]["Duration"].total_seconds() / 3600
                )
            else:
                top_apps[self.db.iloc[i]["Process Name"]] = (
                    self.db.iloc[i]["Duration"].total_seconds() / 3600
                )

        # convert the dictionary to a dataframe
        top_apps = pd.DataFrame(list(top_apps.items()), columns=["Process", "Time"])

        # sort the dataframe by time
        top_apps = top_apps.sort_values(by="Time", ascending=False)

        # get the top 10 apps
        top_apps = top_apps.head(10)

        # convert the dataframe to a dictionary
        top_apps = top_apps.to_dict()

        return top_apps

    def get_weekly_analytics(self):
        # returns a dictionary with x and y values for the graph
        # x is a list for days
        # y is a list for duration summed for each day

        weekly_analytics = {str(i): 0 for i in range(7)}  # 0 is Monday

        # get todays date
        today = datetime.datetime.now()

        # get the date 7 days ago
        seven_days_ago = today - datetime.timedelta(days=7)

        # iterate over the database, and sum up the duration where the date is between today and 7 days ago
        for i in range(len(self.db)):
            current_date = datetime.datetime.strptime(
                self.db.iloc[i]["Start Time"].split(" ")[0], "%Y-%m-%d"
            )
            if current_date <= today and current_date >= seven_days_ago:
                day = current_date.weekday()
                if str(day) in weekly_analytics:
                    weekly_analytics[str(day)] += (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )
                else:
                    weekly_analytics[str(day)] = (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )

        # convert the dictionary to a dataframe
        weekly_analytics = pd.DataFrame(
            list(weekly_analytics.items()), columns=["Day", "Time"]
        )

        # sort the dataframe by day
        weekly_analytics = weekly_analytics.sort_values(by="Day")

        # convert the dataframe to a dictionary
        weekly_analytics = weekly_analytics.to_dict()

        return weekly_analytics

    def get_active_hours_all_time(self):
        # returns a dictionary with x and y values for the graph
        # x is a list for hours
        # y is a list for duration summed for each hour
        active_hours = {str(i): 0 for i in range(24)}

        # iterate over the database, and sum up the duration for each hour
        for i in range(len(self.db)):
            hour = self.db.iloc[i]["Start Time"].split(" ")[1].split(":")[0]
            if hour in active_hours:
                active_hours[hour] += self.db.iloc[i]["Duration"].total_seconds() / 3600
            else:
                active_hours[hour] = self.db.iloc[i]["Duration"].total_seconds() / 3600

        # convert the dictionary to a dataframe
        active_hours = pd.DataFrame(
            list(active_hours.items()), columns=["Hour", "Time"]
        )

        # sort the dataframe by time
        active_hours = active_hours.sort_values(by="Hour")

        # convert the dataframe to a dictionary
        active_hours = active_hours.to_dict()

        return active_hours

    def get_least_used_this_week(self):
        # returns a dictionary with x and y values for the graph
        # x is a list for least used apps process names
        # y is a list for least used apps process durations summed
        least_used = {}

        # get todays date
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # get the date 7 days ago
        seven_days_ago = (
            datetime.datetime.now() - datetime.timedelta(days=7)
        ).strftime("%Y-%m-%d")

        # iterate over the database, and sum up the duration where the date is between today and 7 days ago
        for i in range(len(self.db)):
            if (
                self.db.iloc[i]["Start Time"].split(" ")[0] <= today
                and self.db.iloc[i]["Start Time"].split(" ")[0] >= seven_days_ago
            ):
                if self.db.iloc[i]["Process Name"] in least_used:
                    least_used[self.db.iloc[i]["Process Name"]] += (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )
                else:
                    least_used[self.db.iloc[i]["Process Name"]] = (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )

        # convert the dictionary to a dataframe
        least_used = pd.DataFrame(list(least_used.items()), columns=["Process", "Time"])

        # sort the dataframe by time
        least_used = least_used.sort_values(by="Time")

        # get the top 10 apps
        least_used = least_used.head(10)

        # convert the dataframe to a dictionary
        least_used = least_used.to_dict()

        return least_used

    def get_least_used_this_month(self):
        # returns a dictionary with x and y values for the graph
        # x is a list for least used apps process names
        # y is a list for least used apps process durations summed
        least_used = {}

        # get todays date
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # get the date 30 days ago
        thirty_days_ago = (
            datetime.datetime.now() - datetime.timedelta(days=30)
        ).strftime("%Y-%m-%d")

        # iterate over the database, and sum up the duration where the date is between today and 30 days ago
        for i in range(len(self.db)):
            if (
                self.db.iloc[i]["Start Time"].split(" ")[0] <= today
                and self.db.iloc[i]["Start Time"].split(" ")[0] >= thirty_days_ago
            ):
                if self.db.iloc[i]["Process Name"] in least_used:
                    least_used[self.db.iloc[i]["Process Name"]] += (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )
                else:
                    least_used[self.db.iloc[i]["Process Name"]] = (
                        self.db.iloc[i]["Duration"].total_seconds() / 3600
                    )

        # convert the dictionary to a dataframe
        least_used = pd.DataFrame(list(least_used.items()), columns=["Process", "Time"])

        # sort the dataframe by time
        least_used = least_used.sort_values(by="Time")

        # get the top 10 apps
        least_used = least_used.head(10)

        # convert the dataframe to a dictionary
        least_used = least_used.to_dict()

        return least_used

    def get_least_used_all_time(self):
        # returns a dictionary with x and y values for the graph
        # x is a list for least used apps process names
        # y is a list for least used apps process durations summed
        least_used = {}

        # iterate over the database, and sum up the duration for each process
        for i in range(len(self.db)):
            if self.db.iloc[i]["Process Name"] in least_used:
                least_used[self.db.iloc[i]["Process Name"]] += (
                    self.db.iloc[i]["Duration"].total_seconds() / 3600
                )
            else:
                least_used[self.db.iloc[i]["Process Name"]] = (
                    self.db.iloc[i]["Duration"].total_seconds() / 3600
                )

        # convert the dictionary to a dataframe
        least_used = pd.DataFrame(list(least_used.items()), columns=["Process", "Time"])

        # sort the dataframe by time
        least_used = least_used.sort_values(by="Time")

        # get the top 10 apps
        least_used = least_used.head(10)

        # convert the dataframe to a dictionary
        least_used = least_used.to_dict()

        return least_used

    def train_model(self):
        # train a naive bayes classifier to predict the category of the app based on the process name
        # if a modle.pkl file exists here, load it and return
        if os.path.exists(os.path.join(self.data_directory, "model.pkl")):
            print("model exists, loading it")
            return

        # make a dataframe from the training data
        training_data_dict = {"Process Name": [], "Category": []}
        for key in training_data.keys():
            for value in training_data[key]:
                training_data_dict["Process Name"].append(value)
                training_data_dict["Category"].append(key)

        training_data_df = pd.DataFrame(training_data_dict)

        # now we will train the model

        # create a pipeline
        text_clf = Pipeline(
            [
                ("vect", CountVectorizer()),
                ("tfidf", TfidfTransformer()),
                ("clf", MultinomialNB()),
            ]
        )

        # train the model
        text_clf.fit(training_data_df["Process Name"], training_data_df["Category"])

        # save the model
        with open(os.path.join(self.data_directory, "model.pkl"), "wb") as f:
            pickle.dump(text_clf, f)

        print("model trained and saved")

        return text_clf

    def get_categories_this_week(self):
        self.train_model()
        # returns a dictionary percentage of categories. The categories are based on the process names and are tested with the loaded model.

        # get todays date
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # get the date 7 days ago
        seven_days_ago = (
            datetime.datetime.now() - datetime.timedelta(days=7)
        ).strftime("%Y-%m-%d")

        # get the dataframe for the current timeframe
        current_timeframe = self.db[
            (self.db["Start Time"].str.split(" ").str[0] <= today)
            & (self.db["Start Time"].str.split(" ").str[0] >= seven_days_ago)
        ]

        text_clf = None
        # load the model
        with open(os.path.join(self.data_directory, "model.pkl"), "rb") as f:
            text_clf = pickle.load(f)

        # now predict using the model.
        # predict the categories of the test data
        predicted = text_clf.predict(current_timeframe["Title"])

        # return the counts by percentage of predicted
        categories = {}
        for i in range(len(predicted)):
            if predicted[i] in categories:
                categories[predicted[i]] += 1
            else:
                categories[predicted[i]] = 1

        return categories

    def get_categories_this_month(self):
        self.train_model()
        # returns a dictionary percentage of categories. The categories are based on the process names and are tested with the loaded model.

        # get todays date
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # get the date 30 days ago
        thirty_days_ago = (
            datetime.datetime.now() - datetime.timedelta(days=30)
        ).strftime("%Y-%m-%d")

        # get the dataframe for the current timeframe
        current_timeframe = self.db[
            (self.db["Start Time"].str.split(" ").str[0] <= today)
            & (self.db["Start Time"].str.split(" ").str[0] >= thirty_days_ago)
        ]

        text_clf = None
        # load the model
        with open(os.path.join(self.data_directory, "model.pkl"), "rb") as f:
            text_clf = pickle.load(f)

        # now predict using the model.
        # predict the categories of the test data
        predicted = text_clf.predict(current_timeframe["Title"])

        # return the counts by percentage of predicted
        categories = {}
        for i in range(len(predicted)):
            if predicted[i] in categories:
                categories[predicted[i]] += 1
            else:
                categories[predicted[i]] = 1

        return categories

    def get_categories_all_time(self):

        self.train_model()
        # returns a dictionary percentage of categories. The categories are based on the process names and are tested with the loaded model.

        text_clf = None
        # load the model
        with open(os.path.join(self.data_directory, "model.pkl"), "rb") as f:
            text_clf = pickle.load(f)

        # now predict using the model.
        # predict the categories of the test data
        predicted = text_clf.predict(self.db["Title"])

        # return the counts by percentage of predicted
        categories = {}
        for i in range(len(predicted)):
            if predicted[i] in categories:
                categories[predicted[i]] += 1
            else:
                categories[predicted[i]] = 1

        return categories

    def get_categories_today(self):

        self.train_model()
        # returns a dictionary percentage of categories. The categories are based on the process names and are tested with the loaded model.

        # get todays date
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # get the dataframe for the current timeframe
        current_timeframe = self.db[
            self.db["Start Time"].str.split(" ").str[0] == today
        ]

        text_clf = None
        # load the model
        with open(os.path.join(self.data_directory, "model.pkl"), "rb") as f:
            text_clf = pickle.load(f)

        # now predict using the model.
        # predict the categories of the test data
        predicted = text_clf.predict(current_timeframe["Title"])

        # return the counts by percentage of predicted
        categories = {}
        for i in range(len(predicted)):
            if predicted[i] in categories:
                categories[predicted[i]] += 1
            else:
                categories[predicted[i]] = 1

        return categories
