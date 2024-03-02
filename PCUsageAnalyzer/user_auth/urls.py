from django.urls import path
from . import views
import dashboard.views as dv

urlpatterns = [
    path("", views.login_user, name="login"),
    path("signup_user", views.signup_user, name="signup"),
    path("logout_user", views.logout_user, name="logout"),
    path("profile", views.profile, name="profile"),
    path("about", views.about, name="about"),
]
