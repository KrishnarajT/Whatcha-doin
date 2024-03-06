from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # check if the user exists
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # if user exists, log them in
            login(request, user)
            return redirect("/dashboard/dash")
        else:
            # if user does not exist, show error message
            messages.error(request, "Invalid username or password.")
            return render(
                request,
                "user_auth/login.html",
                {"message": "Invalid username or password."},
            )
    return render(request, "user_auth/login.html")


def signup_user(request):
    if request.method == "POST":
        print(request.POST)
        # get form data
        username = request.POST.get("username", "")
        password = request.POST.get("users_pass", "")
        password_confirm = request.POST.get("users_pass_again", "")

        # dont do anything if they are empty
        if not username or not password or not password_confirm:
            messages.error(request, f"Please fill all the Fields")
            return render(request, "user_auth/signup.html")
        else:
            password = password.strip()
            password_confirm = password_confirm.strip()
            username = username.strip()
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("login")
        # create user
        if password == password_confirm:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect("login")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, "user_auth/signup.html")


def logout_user(request):
    logout(request)
    return redirect("login")

def about(request):
    return render(request, "user_auth/about.html")

@login_required
def profile(request):
    return render(request, "user_auth/profile.html")
