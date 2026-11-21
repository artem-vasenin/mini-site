from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login as django_login

from .forms import LoginForm, RegisterForm

def login(request):
    if request.user.is_authenticated:
        return redirect("home:details")

    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            django_login(request, form.get_user())
            return redirect("home:details")
        else:
            return render(request, "app_auth/login.html", {"form": form})

    return render(
        request,
        "app_auth/login.html",
        {"form": LoginForm(request=request)}
    )

def register(request):
    if request.user.is_authenticated:
        return redirect("home:details")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect("home:details")

    form = RegisterForm()
    return render(request, "app_auth/register.html", { "form": form })
