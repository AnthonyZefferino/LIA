from django.urls import path

from . import views

urlpatterns = [
    path("vacancies", views.index, name="vacancies_index"),
]