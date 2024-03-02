from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import schedule
import time
import threading

# importing the main app class.
from . import MainApp

app = MainApp.MainApplication()


@login_required
def index(request):
    return render(request, "dashboard/index.html")


@login_required
def load_dashboard(request):
    return render(request, "dashboard/dashboard.html")


def load_homepage(request):
    return render(request, "dashboard/index.html")


def start_app(request):
    # print all the variables of this request
    print(request)
    print(request.POST["start"])
    # if request is post, find variables
    if request.method == "POST":
        get_action = request.POST["start"]
        if "start" in get_action.lower():
            # schedule
            schedule.every(app.thread_interval_s).seconds.do(app.run)
            # start the thread for core app
            t = threading.Thread(target=run_core)
            t.start()
            app.set_record(True)
            redirect("dashboard")
            return redirect("dashboard")
        else:
            stop_app()
            print(app.get_finish())
            return render(request, "dashboard/index.html")
    else:
        return render(request, "dashboard/index.html")


def pause_or_resume_app(request):
    app.pause_or_resume()
    print(app.get_record())
    return render(request, "dashboard/dashboard.html")


def stop_app():
    app.set_finish(True)

@login_required
def print_db(request):
    app.print_db()
    return render(request, "dashboard/index.html")

def run_core():
    while True:
        if app.get_record() == True:
            schedule.run_pending()
            # print("next job", schedule.next_run())
        if app.get_finish() == True:
            break
        time.sleep(app.thread_interval_s)
