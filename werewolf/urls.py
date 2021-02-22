from django.conf.urls import url
from django.urls import path
from werewolf import views

urlpatterns = [
    path("login", views.login.as_view(), name="login"),
    path("getrank", views.getRank.as_view(), name="getRank"),
    path("createroom", views.createRoom.as_view(), name="createRoom"),
    path("getroom", views.getRoomInfo.as_view(), name="getRoomInfo"),
    path("findroom", views.findRoom.as_view(), name="findRoom"),
    path("seatact", views.seatAct.as_view(), name="seatAct"),
]
