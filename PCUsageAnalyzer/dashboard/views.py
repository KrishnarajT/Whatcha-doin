from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import schedule
import time
import threading
from django.http import JsonResponse
import plotly.graph_objects as go
from plotly.offline import plot


# importing the main app class.
from . import MainApp

app = MainApp.MainApplication()


@login_required
def index(request):
    return render(request, "dashboard/index.html")


@login_required
def load_dashboard(request):
    if app.get_app_started() == False:
        app.set_finish(False)
        app.init_db()
        schedule.every(app.thread_interval_ms / 1000).seconds.do(app.run)
        # start the thread for core app
        t = threading.Thread(target=run_core)
        t.start()
        print("started app thread. ")
        app.set_app_started(True)

    recording = app.get_record()
    return render(request, "dashboard/dashboard.html", context={"recording": recording})


@login_required
def start_app(request):
    app.set_finish(False)
    app.init_db()
    schedule.every(app.thread_interval_ms).seconds.do(app.run)
    # start the thread for core app
    t = threading.Thread(target=run_core)
    t.start()
    app.set_record(True)
    redirect("dashboard")
    recording = app.get_record()
    return render(request, "dashboard/dashboard.html", context={"recording": recording})


@login_required
def load_homepage(request):
    return render(request, "dashboard/index.html")


@login_required
def pause_or_resume_app(request):
    app.pause_or_resume()
    print("recording is", app.get_record())
    return JsonResponse(app.get_record(), safe=False)


@login_required
def stop_app_and_logout(request):
    app.set_finish(True)
    app.cleanup()
    schedule.clear()
    logout(request)
    return redirect("login")


@login_required
def print_db(request):
    app.print_db()
    # print(app.get_db())
    return render(request, "dashboard/dashboard.html")


def run_core():
    while True:
        if app.get_record() == True:
            schedule.run_pending()
        if app.get_finish() == True:
            break
        time.sleep(app.thread_interval_ms / 1000)


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


def test(request):
    df = app.get_db()
    data = df.to_json(orient="records")
    return JsonResponse(data, safe=False)


def get_counter(request):
    # app.print_db()
    counter = app.get_counter()
    return JsonResponse(counter, safe=False)


def get_recording(request):
    recording = app.get_record()
    return JsonResponse(recording, safe=False)


def get_idle_detection(request):
    idle_detection = app.get_idle_detection()
    return JsonResponse(idle_detection, safe=False)


def get_intervals_ms(request):
    intervals_ms = app.get_intervals_ms()
    return JsonResponse(intervals_ms, safe=False)


def get_category(request):
    category = {"Code": 35, "Social Media": 10, "Entertainment": 15, "Productivity": 40}
    return JsonResponse(category, safe=False)
