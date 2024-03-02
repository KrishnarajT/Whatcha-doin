from . import views
from django.urls import path
from user_auth import views as uv

urlpatterns = [
    path("", views.index, name="index"),
    path("dash/", views.load_dashboard, name="dashboard"),
]
