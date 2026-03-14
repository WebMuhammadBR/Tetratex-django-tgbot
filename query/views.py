from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    return render(request, "query/dashboard.html")


@login_required
def farmer_report(request):
    return render(request, "query/farmer_report.html")
