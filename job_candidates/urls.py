from django.urls import path

from . import views

app_name = 'job_candidates'
urlpatterns = [
    path("job_candidates", views.index, name="job_candidates_index"),
    path('list', views.JobsCandidatesListView.as_view(), name='job_candidates-list'),
    path('detail/<int:pk>', views.JobsCandidatesView.as_view(), name='job_candidate-details'),
]
