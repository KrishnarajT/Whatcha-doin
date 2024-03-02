from . import views
from django.urls import path

urlpatterns = [
    path("", views.load_dashboard, name="dashboard"),
]
