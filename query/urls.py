from django.urls import path
from django.contrib.auth import views as auth_views

from .views import farmer_report, home

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="query/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("", home, name="home"),
    path("report/farmer/", farmer_report, name="farmer_report"),
]