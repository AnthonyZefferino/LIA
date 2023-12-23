from itertools import groupby
from operator import attrgetter
from pprint import pprint

from django.shortcuts import render, get_object_or_404
from django.utils import translation
# Create your views here.
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from utils.models import VacancyCustomFieldValue
from .models import Vacancy
from django.utils.translation import gettext_lazy as _


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
        user_language = 'it'  # Codice della lingua italiana
        translation.activate(user_language)
        context = super().get_context_data(**kwargs)
        context['pageview'] = 'Posti Vacanti Attivi'
        return context


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'vacancies/vacancy-detail.html'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs.get('pk'))
        context['heading'] = _("Detail") + " " + str(vacancy.insertion_title)
        context['company'] = vacancy.company
        context['office'] = vacancy.office
        context['representative'] = vacancy.company_representative
        context['protected_category'] = vacancy.protected_category.all()
        context['custom_field_values'] = VacancyCustomFieldValue.objects.filter(vacancy=vacancy)
        context['responsibilities'] = vacancy.responsibilities.split('\n')

        custom_field_values = VacancyCustomFieldValue.objects.filter(vacancy=vacancy)
        custom_field_values = custom_field_values.order_by('custom_field__group__description')

        # Raggruppa i valori dei campi personalizzati per CustomFieldGroup.description
        grouped_custom_field_values = {k: list(v) for k, v in
                                       groupby(custom_field_values, key=attrgetter('custom_field.group.description'))}

        # Dividi i valori dei campi personalizzati per \n
        split_values = {k: [item.value.split('\n') for item in v] for k, v in grouped_custom_field_values.items()}

        context['grouped_custom_field_values'] = split_values

        # Aggiungi la storia delle modifiche e i dettagli dei cambiamenti al contesto
        history = []
        for record in vacancy.history.all():
            delta = None
            if record.prev_record:
                delta = record.diff_against(record.prev_record)
            history.append((record, delta))
        context['history'] = history

        return context
