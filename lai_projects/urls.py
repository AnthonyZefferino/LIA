from django.urls import path
from . import views

urlpatterns = [
    path("progetti", views.index, name="project_index"),

]
