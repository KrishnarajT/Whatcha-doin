from . import views
from django.urls import path
from user_auth import views as uv

urlpatterns = [
    path("", views.index, name="index"),
    path("dash/", views.load_dashboard, name="dashboard"),
    path("login_user", uv.login_user, name="login"),
    path("signup_user", uv.signup_user, name="signup"),
    path("logout_user", uv.logout_user, name="logout"),
]
