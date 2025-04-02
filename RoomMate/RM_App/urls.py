from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("preferences/", views.set_preferences, name="set_preferences"),
    path("matches/", views.find_matches, name="find_matches"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]