from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("Salom Bobur aka 👋")


@login_required
def farmer_report(request):
    return render(request, "query/farmer_report.html")
