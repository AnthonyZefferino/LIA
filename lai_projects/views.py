from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from .models import Project, BudgetYear
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import get_object_or_404


def index(request):
    return HttpResponse("Hello, world. You're at the PROJECTS index.")


class ProjectListView(ListView):
    model = Project
    template_name = 'lia_projectc/projects_list.html'
    context_object_name = 'companies'

    def get_queryset(self):
        company = self.kwargs.get('company', None)
        if company is not None:
            queryset = Project.objects.filter(Q(company__name=company))
        else:
            queryset = Project.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.kwargs.get('company', None)
        if company is not None:
            context['pageview'] = company
            context['company'] = company
        else:
            context['pageview'] = "Tutte i progetti"
            context['company'] = None
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'lia_projectc/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        context['heading'] = _("Detail") + " " + str(Project.name)
        context['files'] = project.files.all()
        context['budget_year'] = project.budget_years.all()
        return context
