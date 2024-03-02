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


@login_required
def load_homepage(request):
    return render(request, "dashboard/index.html")


@login_required
def start_app(request):
    app.set_finish(False)
    app.init_db()
    schedule.every(app.thread_interval_s).seconds.do(app.run)
    # start the thread for core app
    t = threading.Thread(target=run_core)
    t.start()
    app.set_record(True)
    redirect("dashboard")
    return redirect("dashboard")

@login_required
def pause_or_resume_app(request):
    app.pause_or_resume()
    print(app.get_record())
    return render(request, "dashboard/dashboard.html")


@login_required
def stop_app(request):
    app.set_finish(True)
    app.cleanup()
    schedule.clear()
    return render(request, "dashboard/index.html")


@login_required
def print_db(request):
    app.print_db()
    # print(app.get_db())
    return render(request, "dashboard/index.html")


def run_core():
    while True:
        if app.get_record() == True:
            schedule.run_pending()
            # print("next job", schedule.next_run())
        if app.get_finish() == True:
            break
        time.sleep(app.thread_interval_s)

def start_fresh(request):
    app.start_fresh()
    return render(request, "dashboard/dashboard.html")

def export_raw(request):
    app.export_raw()
    return render(request, "dashboard/dashboard.html")

def export_collaborative_data(request):
    app.export_collaborative_data()
    return render(request, "dashboard/dashboard.html")

def flip_idle_detection(request):
    app.flip_idle_detection()
    return render(request, "dashboard/dashboard.html")
