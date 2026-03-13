from django.urls import path

from .views import farmer_report, home, login_view

urlpatterns = [
    path("", login_view, name="login"),
    path("home/", home, name="home"),
    path("report/farmer/", farmer_report, name="farmer_report"),
]
