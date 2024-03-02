from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def load_settings(request):
    return render(request, "settings/index.html")
