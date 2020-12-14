from django.urls import path
from . import views
urlpatterns = [
   path("index", views.index, name="index"),
   path("enter", views.enter, name="enter"),
]
