from pprint import pprint

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from .models import Project, BudgetYear, BudgetObjective,Budget
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import translation
from .api import ProjectSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from functools import wraps
from utils.models import CustomFieldChoiceProject
from itertools import groupby
from operator import attrgetter, itemgetter


def index(request):
    return HttpResponse("Hello, world. You're at the PROJECTS index.")


def ajax_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)

    return _wrapped_view


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
        user_language = 'it'  # Codice della lingua italiana
        translation.activate(user_language)
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
        user_language = 'it'  # Codice della lingua italiana
        translation.activate(user_language)
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        context['heading'] = _("Detail") + " " + str(project.project_title)
        context['files'] = project.files.all()
        context['budget_year'] = project.budget_years.all()
        context['descriptions'] = project.description.split('\n')
        custom_field_values = CustomFieldChoiceProject.objects.filter(project=project).order_by(
            'custom_field__group__description')
        custom_field_values = [
            {
                'group_description': item.custom_field.group.description,
                'field_type': item.custom_field.field_type,
                'label': item.custom_field.label,
                'value': item.value.split('\n'),
                'required_custom_value': item.required_custom_value,
            }
            for item in custom_field_values
        ]
        grouped_custom_field_values = {k: list(v) for k, v in
                                       groupby(custom_field_values, key=itemgetter('group_description'))}
        context['grouped_custom_field_values'] = grouped_custom_field_values



        budget_years = BudgetYear.objects.filter(project=project)
        context['budget_years'] = budget_years

        # Query for budget objectives related to each budget year
        budget_objectives = {}
        budgets = {}

        for budget_year in budget_years:
            budget_objectives[budget_year.id] = BudgetObjective.objects.filter(budget_year=budget_year)
            budgets[budget_year.id] = Budget.objects.filter(budget_year=budget_year)

        context['budget_objectives'] = budget_objectives
        context['budgets'] = budgets
        # pprint(context)
        return context


@api_view(['GET'])
@ajax_login_required
def projects_api(request):
    company = request.GET.get('company')
    if company is not None:
        projects = Project.objects.filter(company__name=company)
    else:
        projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)
