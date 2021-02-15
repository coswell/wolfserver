from django.conf.urls import url
from django.urls import path
from werewolf import views

urlpatterns = [
    path("login", views.login.as_view(), name="login"),
    path("getrank", views.getRank.as_view(), name="getRank"),
]
