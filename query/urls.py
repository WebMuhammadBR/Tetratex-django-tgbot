from django.urls import path

from .views import farmer_report, home, login_view, logout_view

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("report/farmer/", farmer_report, name="farmer_report"),
]
