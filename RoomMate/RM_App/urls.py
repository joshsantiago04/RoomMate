from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("preferences/", views.set_preferences, name="set_preferences"),
    path("matches/", views.find_matches, name="find_matches"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path('my-matches/', views.my_matches, name='my_matches'),
    path('send-request/<int:to_user_id>/', views.send_match_request, name='send_match_request'),
    path('confirm-match/<int:from_user_id>/', views.confirm_match, name='confirm_match'),
    path('unsend-request/<int:to_user_id>/', views.unsend_match_request, name='unsend_match_request'),
    path('unmatch/<int:uid>/', views.unmatch_user, name='unmatch_user'),
]