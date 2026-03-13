from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        remember_me = request.POST.get("rememberme") == "on"

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Kirish nomi yoki parol noto'g'ri.")
            return render(request, "login/login.html", status=401)

        login(request, user)
        if remember_me:
            request.session.set_expiry(60 * 60 * 24 * 14)
        else:
            request.session.set_expiry(0)

        return redirect("home")

    return render(request, "login/login.html")


@login_required
def home(request):
    return render(request, "query/dashboard.html")


@login_required
def farmer_report(request):
    return render(request, "query/farmer_report.html")
