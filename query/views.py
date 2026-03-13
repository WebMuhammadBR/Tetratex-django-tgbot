from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render


def login_view(request):
    if request.user.is_authenticated:
        return redirect("farmer_report")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        remember_me = request.POST.get("rememberme") == "on"

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Login yoki parol noto'g'ri.")
            return render(request, "login/login.html", status=401)

        login(request, user)
        if not remember_me:
            request.session.set_expiry(0)

        return redirect("farmer_report")

    return render(request, "login/login.html")


@login_required
def home(request):
    return HttpResponse("Salom Bobur aka 👋")


@login_required
def farmer_report(request):
    return render(request, "query/farmer_report.html")
