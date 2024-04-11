from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import schedule
import time
import threading
from django.http import JsonResponse
import plotly.graph_objects as go
from plotly.offline import plot
from django.shortcuts import render, redirect


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
    print("exporting raw data")
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


def get_current_app_usage(request):
    current_app_usage = app.get_current_app_usage()
    app.print_db()
    return JsonResponse(current_app_usage, safe=False)


def start_fresh(request):
    app.start_fresh()
    return render(request, "dashboard/dashboard.html")


def get_todays_app_usage(request):
    todays_app_usage = app.get_todays_app_usage()
    return JsonResponse(todays_app_usage, safe=False)


def get_hourly_pc_usage(request):
    hourly_pc_usage = app.get_hourly_pc_usage()
    return JsonResponse(hourly_pc_usage, safe=False)


def get_top_apps_this_week(request):
    top_apps_this_week = app.get_top_apps_this_week()
    return JsonResponse(top_apps_this_week, safe=False)


def get_top_apps_this_month(request):
    top_apps_this_month = app.get_top_apps_this_month()
    return JsonResponse(top_apps_this_month, safe=False)


def get_top_apps_all_time(request):
    top_apps_all_time = app.get_top_apps_all_time()
    return JsonResponse(top_apps_all_time, safe=False)


## pages


def top_apps_this_week(request):
    return render(request, "dashboard/top_apps_this_week.html")


def top_apps_this_month(request):
    return render(request, "dashboard/top_apps_this_month.html")


def top_apps_all_time(request):
    return render(request, "dashboard/top_apps_all_time.html")


def view_weekly_analytics(request):
    return render(request, "dashboard/view_weekly_analytics.html")


def most_distracting_this_week(request):
    return render(request, "dashboard/most_distracting_this_week.html")


def most_distracting_all_time(request):
    return render(request, "dashboard/most_distracting_all_time.html")


def most_played_games(request):
    return render(request, "dashboard/most_played_games.html")


def most_active_hours_all_time(request):
    return render(request, "dashboard/most_active_hours_all_time.html")


def least_used_this_week(request):
    return render(request, "dashboard/least_used_this_week.html")


def least_used_this_month(request):
    return render(request, "dashboard/least_used_this_month.html")


def least_used_all_time(request):
    return render(request, "dashboard/least_used_all_time.html")
