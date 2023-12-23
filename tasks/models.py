from django.db import models
from django.utils.translation import gettext_lazy as _

from aziende.models import Company, Office
from job_candidates.models import CandidateProjectVacancyPlacement, Candidate
from django.conf import settings
from django.utils import timezone

from lai_projects.models import Project
from vacancies.models import Vacancy


class Ticketing(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='ticketing_candidate', verbose_name=_("Candidate"),
                                  on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, related_name='ticketing_company', verbose_name=_("Company"),
                                on_delete=models.CASCADE, null=True, blank=True)
    office = models.ForeignKey(Office, related_name='ticketing_office', verbose_name=_("office"),
                               on_delete=models.CASCADE, null=True, blank=True)
    vacancy = models.ForeignKey(Vacancy, related_name='ticketing_vacancy', verbose_name=_("Vacancy"),
                                on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, related_name='ticketing_project', verbose_name=_("Project"),
                                on_delete=models.CASCADE, null=True, blank=True)
    placement = models.ForeignKey(CandidateProjectVacancyPlacement, on_delete=models.CASCADE,
                                  related_name="placement_tickets", null=True, blank=True)
    ticket_issue = models.TextField(_("Ticket Issue"))
    ticket_status = models.CharField(
        _("Ticket Status"),
        max_length=20,
        choices=(('open', _('Open')), ('pending', _('Pending')), ('closed', _('Closed')),),
        default='pending'
    )
    ticket_type = models.CharField(
        _("Ticket Type"),
        max_length=20,
        choices=(('placement', _('Placement')), ('vacancy', _('Vacancy')), ('interview', _('Interview')),
                 ('company', _('Company')), ('project', _('Project')),),
        default='interview'
    )
    alerting = models.BooleanField(_("alerting"), default=False)
    start_data= models.DateTimeField(_("start_data"), blank=True, null=True, default=timezone.now)
    data_alert = models.DateTimeField(_("data alert"), blank=True, null=True)
    end_data = models.DateTimeField(_("end_data"), blank=True, null=True)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_tickets',
        on_delete=models.CASCADE,
        null=True
    )
    user_assigned = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_tickets',
        on_delete=models.CASCADE,
        null=True
    )
    data_viewed = models.DateTimeField(_("data viewed"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    def __str__(self):
        return self.ticket_issue

    class Meta:
        verbose_name = _("Ticketing")
        verbose_name_plural = _("Ticketing")

class TicketingResponse(models.Model):
    ticket = models.ForeignKey(Ticketing, on_delete=models.CASCADE, related_name="responses")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    message = models.TextField(_("Response Message"))
    data_viewed = models.DateTimeField(_("data viewed"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    def __str__(self):
        return self.message

    class Meta:
        verbose_name = _("Ticketing Response")
        verbose_name_plural = _("Ticketing Response")