from django.urls import path

from . import views

urlpatterns = [
    path("utils", views.index, name="utils_index"),
]