from django.urls import path
from . import views
import dashboard.views as dv

urlpatterns = [
    path("login_user", views.login_user, name="login"),
    path("signup_user", views.signup_user, name="signup"),
    path("dashboard/", dv.index, name="dashboard_index"),
]
