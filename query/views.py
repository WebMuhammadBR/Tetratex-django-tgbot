from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


@login_required
def home(request):
    stats = {
        "welcome": f"Xush kelibsiz, {request.user.get_full_name() or request.user.username}",
        "cards": [
            {"title": "Jami shartnomalar", "value": 128, "trend": "+12%"},
            {"title": "Faol fermerlar", "value": 54, "trend": "+4%"},
            {"title": "Bugungi tushum", "value": "42 500 000 so'm", "trend": "+8%"},
        ],
    }
    return render(request, "query/dashboard.html", {"stats": stats})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")

    return render(request, "query/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def farmer_report(request):
    return render(request, "query/farmer_report.html")
