from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Candidate

def index(request):
    return HttpResponse("Hello, world. You're at the job candidates index.")
class JobsCandidatesListView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Candidate List"
        greeting['pageview'] = "Candidates"
        return render(request, 'job_candidates/list.html', greeting)


class JobsCandidatesView(LoginRequiredMixin, DetailView):
    model = Candidate
    template_name = 'job_candidates/candidate-detail.html'
    context_object_name = 'vacancies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'candidates'
        context['pageview'] = 'candidate detail'
        return context
