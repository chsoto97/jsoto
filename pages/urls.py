from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("bio/", views.bio, name="bio"),
    path("music/", views.music, name="music"),
    path("photos/", views.photos, name="photos"),
    path("contact/", views.contact, name="contact"),
]
