from pprint import pprint
from itertools import groupby
from operator import attrgetter
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from tasks.models import Ticketing, TicketingResponse
from .models import Candidate, CandidateCustomFieldValue, InterviewCandidateVacancyProjectHistory, \
    CandidateProjectVacancyPlacement


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
    context_object_name = 'candidate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        candidate = get_object_or_404(Candidate, pk=self.kwargs.get('pk'))
        context['heading'] = 'Candidato'
        context['pageview'] = 'Candidato dettagli'
        context['protected_category'] = candidate.protected_category.all()
        context['descriptions'] = candidate.description.split('\n')
        context['evaluations'] = candidate.evaluation_lavoriamoci.split('\n')

        history_interview_candidate = InterviewCandidateVacancyProjectHistory.objects.filter(candidate=candidate)
        context['history_interview_candidate'] = history_interview_candidate
        history_placement_candidate = CandidateProjectVacancyPlacement.objects.filter(candidate=candidate)
        context['history_placement_candidate'] = history_placement_candidate

        custom_field_values = CandidateCustomFieldValue.objects.filter(candidate=candidate)
        custom_field_values = custom_field_values.order_by('custom_field__group__description')
        grouped_custom_field_values = {k: list(v) for k, v in
                                       groupby(custom_field_values, key=attrgetter('custom_field.group.description'))}
        split_values = {k: [item.value.split('\n') for item in v] for k, v in grouped_custom_field_values.items()}
        context['grouped_custom_field_values'] = split_values
        pprint(context['grouped_custom_field_values'])
        history = []
        for record in candidate.history.all():
            delta = None
            if record.prev_record:
                delta = record.diff_against(record.prev_record)
            history.append((record, delta))
        context['history'] = history

        for placement in history_placement_candidate:
            placement.tickets = Ticketing.objects.filter(placement=placement)

        context['history_placement_candidate'] = history_placement_candidate
        # pprint(context['history'])
        # pprint(context['protected_category'])
        pprint(context['history_interview_candidate'])
        return context
