from django.urls import path

from . import views

app_name = 'vacancies'
urlpatterns = [
    path("vacancies", views.index, name="vacancies_index"),
    path('grid', views.VacancyListView.as_view(), name='vacancies-grid'),
    path('detail/<int:pk>', views.VacancyDetailView.as_view(), name='vacancy-details'),
]
