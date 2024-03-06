from . import views
from django.urls import path

urlpatterns = [
    path("", views.load_homepage, name="home"),
    path("dash", views.load_dashboard, name="dashboard"),
    path("startapp", views.start_app, name="startapp"),
    path("pauseorresume", views.pause_or_resume_app, name="pauseorresume"),
    path("printdb", views.print_db, name="printdb"),
    path("stopapp", views.stop_app_and_logout, name="stopapp"),
    path("start_fresh", views.start_fresh, name="start_fresh"),
    path("export_raw", views.export_raw, name="export_raw"),
    path(
        "export_collaborative_data",
        views.export_collaborative_data,
        name="export_collaborative_data",
    ),
    path("flip_idle_detection", views.flip_idle_detection, name="flip_idle_detection"),
    path("test", views.test, name="test"),
    path("get_counter", views.get_counter, name="get_counter"),
    path("get_recording", views.get_recording, name="get_recording"),
    path("get_intervals_ms", views.get_intervals_ms, name="get_intervals_ms"),
    path("get_category", views.get_category, name="get_category"),
]
