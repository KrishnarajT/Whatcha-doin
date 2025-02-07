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
    path("get_recording", views.get_recording, name="get_recording"),
    path("get_intervals_ms", views.get_intervals_ms, name="get_intervals_ms"),
    path("get_category", views.get_category, name="get_category"),
    path(
        "get_current_app_usage",
        views.get_current_app_usage,
        name="get_current_app_usage",
    ),
    path("start_fresh", views.start_fresh, name="start_fresh"),
    path("export_data", views.export_raw, name="export_data"),
    path(
        "get_todays_app_usage", views.get_todays_app_usage, name="get_todays_app_usage"
    ),
    path("get_hourly_pc_usage", views.get_hourly_pc_usage, name="get_hourly_pc_usage"),
    ########### pages ##############
    path(
        "categories_this_week", views.categories_this_week, name="categories_this_week"
    ),
    path(
        "get_categories_this_week",
        views.get_categories_this_week,
        name="get_categories_this_week",
    ),
    path(
        "get_categories_today",
        views.get_categories_today,
        name="get_categories_today",
    ),
    path(
        "categories_this_month",
        views.categories_this_month,
        name="categories_this_month",
    ),
    path(
        "get_categories_this_month",
        views.get_categories_this_month,
        name="get_categories_this_month",
    ),
    path("categories_all_time", views.categories_all_time, name="categories_all_time"),
    path(
        "get_categories_all_time",
        views.get_categories_all_time,
        name="get_categories_all_time",
    ),
    path("top_apps_this_week", views.top_apps_this_week, name="top_apps_this_week"),
    path(
        "get_top_apps_this_week",
        views.get_top_apps_this_week,
        name="get_top_apps_this_week",
    ),
    path("top_apps_this_month", views.top_apps_this_month, name="top_apps_this_month"),
    path(
        "get_top_apps_this_month",
        views.get_top_apps_this_month,
        name="get_top_apps_this_month",
    ),
    path("top_apps_all_time", views.top_apps_all_time, name="top_apps_all_time"),
    path(
        "get_top_apps_all_time",
        views.get_top_apps_all_time,
        name="get_top_apps_all_time",
    ),
    path(
        "view_weekly_analytics",
        views.view_weekly_analytics,
        name="view_weekly_analytics",
    ),
    path(
        "get_weekly_analytics", views.get_weekly_analytics, name="get_weekly_analytics"
    ),
    path(
        "most_distracting_this_week",
        views.most_distracting_this_week,
        name="most_distracting_this_week",
    ),
    path(
        "most_distracting_all_time",
        views.most_distracting_all_time,
        name="most_distracting_all_time",
    ),
    path("most_played_games", views.most_played_games, name="most_played_games"),
    path(
        "most_active_hours_all_time",
        views.most_active_hours_all_time,
        name="most_active_hours_all_time",
    ),
    path(
        "get_most_active_hours_all_time",
        views.get_most_active_hours_all_time,
        name="get_most_active_hours_all_time",
    ),
    path(
        "least_used_this_week", views.least_used_this_week, name="least_used_this_week"
    ),
    path(
        "get_least_used_this_week",
        views.get_least_used_this_week,
        name="get_least_used_this_week",
    ),
    path(
        "least_used_this_month",
        views.least_used_this_month,
        name="least_used_this_month",
    ),
    path(
        "get_least_used_this_month",
        views.get_least_used_this_month,
        name="get_least_used_this_month",
    ),
    path("least_used_all_time", views.least_used_all_time, name="least_used_all_time"),
    path(
        "get_least_used_all_time",
        views.get_least_used_all_time,
        name="get_least_used_all_time",
    ),
]
