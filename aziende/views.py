from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from .models import RoleHistory, Company, Industry, Activity
from django.views.generic.edit import CreateView
from django.contrib.admin.utils import quote
from django.contrib.admin.options import IS_POPUP_VAR
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .forms import CompanyForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from functools import wraps
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .api import CompanySerializer
from django.utils.translation import gettext_lazy as _
from pprint import pprint
from django.db.models import Q


def ajax_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)

    return _wrapped_view


@ajax_login_required
@require_POST
def company_delete_api(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    return JsonResponse({'status': 'success', 'message': 'Company deleted successfully.'})


@api_view(['GET'])
@ajax_login_required
def companies_api(request):
    industry = request.GET.get('industry')
    if industry is not None:
        companies = Company.objects.filter(industry__name=industry)
    else:
        companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)


def index(request):
    return HttpResponse("Hello, world. You're at the AZIENDE index.")


def filtered_companies(request, industry_id):
    # Ottieni l'oggetto Industry corrispondente all'ID fornito o None se non esiste
    industry = Industry.objects.filter(id=industry_id).first()

    # Filtra le istanze di Company in base all'Industry ottenuto
    companies = Company.objects.filter(industry=industry) if industry else Company.objects.none()

    # Invia le companies filtrate al template
    context = {'companies': companies, 'industry': industry}
    return render(request, 'list_company.html', context)


class RoleHistoryCreateView(CreateView):
    model = RoleHistory

    fields = ['company_representative', 'role', 'date_from', 'date_to']
    template_name = 'admin/aziende/role_history_form.html'

    def get_initial(self):
        initial_data = super(RoleHistoryCreateView, self).get_initial()
        company_representative_id = self.request.GET.get('company_representative')
        if company_representative_id:
            initial_data['company_representative'] = company_representative_id
        else:
            # Qui puoi impostare un valore predefinito o gestire l'assenza del parametro
            pass
        return initial_data

    def form_valid(self, form):
        obj = form.save()
        if self.request.GET.get('_popup'):
            return HttpResponse(
                f'<script>opener.dismissAddAnotherPopup(window, "{obj.pk}", "{obj}");</script>'
            )
        else:
            return super(RoleHistoryCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_label'] = 'aziende'
        # Aggiungi al context se si tratta di una popup view
        context['is_popup'] = IS_POPUP_VAR in self.request.GET
        # Gestione dei rolehistories se company_representative è passato come parametro GET
        rep_id = self.request.GET.get('company_representative')
        if rep_id:
            context['rolehistories'] = RoleHistory.objects.filter(company_representative=rep_id)
            # Se vuoi preselezionare il company_representative nel form, puoi farlo qui
            context['selected_company_representative'] = quote(rep_id)
        return context


class ActivityCreateView(CreateView):
    model = Activity
    fields = ['description', 'date', 'alert', 'visible_to_all', 'activity_type',
              'company_representative']  # Aggiorna con i campi reali del tuo modello
    template_name = 'admin/aziende/activity_form.html'  # Aggiorna con il percorso al tuo template del form

    def get_initial(self):
        initial_data = super().get_initial()
        company_representative_id = self.request.GET.get('company_representative')
        if company_representative_id:
            initial_data['company_representative'] = company_representative_id
        return initial_data


class CompanyListView(ListView):
    model = Company
    template_name = 'aziende/company_list.html'
    context_object_name = 'companies'

    def get_queryset(self):
        industry = self.kwargs.get('industry', None)
        if industry is not None:
            queryset = Company.objects.filter(Q(industry__name=industry))
        else:
            queryset = Company.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        industry = self.kwargs.get('industry', None)
        if industry is not None:
            context['pageview'] = industry
            context['industry'] = industry
        else:
            context['pageview'] = "Tutte le industrie"
            context['industry'] = None
        return context




class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'aziende/company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, pk=self.kwargs.get('pk'))
        context['heading'] = _("Detail") + " " + str(company.name)
        context['files'] = company.files.all()
        context['offices'] = company.offices.all()
        context['representatives'] = company.companyrepresentative_set.all()
        context['activities'] = Activity.objects.filter(company_representative__company=company)

        return context


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'aziende/company_form.html'
    success_url = reverse_lazy('aziende:company-list')


class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'aziende/company_confirm_delete.html'
    success_url = reverse_lazy('aziende:company-list')
