from django.urls import path
from . import views

app_name = 'lia_project'
urlpatterns = [
    path("", views.index, name="lia_project_index"),
    path('list/', views.ProjectListView.as_view(), name='lia_project-list'),
    path('list/<str:company>/', views.ProjectListView.as_view(), name='lia_project-list'),
    path('details/<int:pk>/', views.CompanyDetailView.as_view(), name='lia_project-details'),
    path('edit/<int:pk>/', views.CompanyUpdateView.as_view(), name='lia_projec-edit'),

]
