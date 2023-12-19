from django.urls import path
from . import views

app_name = 'lai_projects'
urlpatterns = [
    path("", views.index, name="lia_project_index"),
    path('grid/', views.ProjectListView.as_view(), name='lai_project-list'),
    path('grid/<str:company>/', views.ProjectListView.as_view(), name='lai_projects-list'),
    path('detail/<int:pk>/', views.ProjectDetailView.as_view(), name='lai_project-detail'),
    path('edit/<int:pk>/', views.ProjectListView.as_view(), name='lai_project-edit'),
    path('api/view_list/', views.projects_api, name='projects-api'),
]
