from . import views
from django.urls import path

urlpatterns = [
    path("", views.load_homepage, name="home"),
    path("dash", views.load_dashboard, name="dashboard"),
    path("startapp", views.start_app, name="startapp"),
    path("pauseorresume", views.pause_or_resume_app, name="pauseorresume"),
    path("printdb", views.print_db, name="printdb")
]
