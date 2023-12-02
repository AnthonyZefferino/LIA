from django.urls import path
from .views import index, ActivityCreateView
from . import views

app_name = 'aziende'

urlpatterns = [
    path('companies/', views.CompanyListView.as_view(), name='company-list'),
    path('companies/<int:pk>/', views.CompanyDetailView.as_view(), name='company-detail'),
    path('companies/<int:pk>/edit/', views.CompanyUpdateView.as_view(), name='company-edit'),
    path('companies/<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company-delete'),

    path("", index, name="index"),
    path('activity/add/', ActivityCreateView.as_view(), name='aziende_activity_add'),
    path('companies/api/', views.companies_api, name='companies-api'),
    path('companies/api/delete/<int:pk>/', views.company_delete_api, name='company-delete-api'),
]
