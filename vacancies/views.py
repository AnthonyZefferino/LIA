from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Vacancy


def index(request):
    return HttpResponse("Hello, world. You're at the VACANCIES index.")


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies-grid.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        queryset = Vacancy.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageview'] = 'vacancies active'
        return context


class VacancyDetailView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy-detail.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        queryset = Vacancy.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageview'] = 'vacancy detail'
        return context
