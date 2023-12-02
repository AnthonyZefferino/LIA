from aziende.models import Company
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class TargetProject(models.Model):
    description = models.CharField(_("Description"), max_length=255)
    question_lia = models.TextField(_("Question for LIA"), blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Target")
        verbose_name_plural = _("Targets")


class Project(models.Model):
    project_title = models.CharField(_("Project Title"), max_length=255, blank=True, null=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name=_("Supporting Entity"),
        limit_choices_to={'industry__id': 1},
        related_name='supported_projects'
    )
    project_type = models.CharField(
        _("Project Type"),
        max_length=10,
        choices=(('closed', _('Closed')), ('open', _('Open'))),
        default='open'
    )
    description = models.TextField(_("Description"), blank=True, null=True)
    start_date = models.DateField(_("Start Date"), default=timezone.now)
    end_date = models.DateField(_("End Date"), blank=True, null=True)
    target = models.ManyToManyField('TargetProject', verbose_name=_("Project Targets"), blank=True)
    lead_partne = models.ManyToManyField(
        Company,
        verbose_name=_("Lead Partner"),
        related_name='lead_projects',
        limit_choices_to={'industry__id': 2}
    )
    partner = models.ManyToManyField(
        Company,
        verbose_name=_("Partners"),
        related_name='partnered_projects',
        limit_choices_to={'industry__id': 2}
    )
    supporters = models.ManyToManyField(
        Company,
        verbose_name=_("Supporters"),
        related_name='supporting_projects',
        limit_choices_to={'industry__id': 4}
    )
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return f"{self.company} - {self.project_title}"

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

class BudgetYear(models.Model):
    budget_title = models.CharField(_("Budget Title"), max_length=255, blank=True, null=True)
    project = models.ForeignKey('Project', verbose_name=_("Project"), on_delete=models.CASCADE, related_name='budget_years')
    year = models.PositiveIntegerField(_("Year"), default=timezone.now().year)

    def __str__(self):
        return f"{self.project} - {self.year}"

    class Meta:
        verbose_name = _("Budget Year")
        verbose_name_plural = _("Budget Years")


class BudgetType(models.Model):
    description = models.CharField(_("Description"), max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Budget Type")
        verbose_name_plural = _("Budget Types")

class Budget(models.Model):
    budget_year = models.ForeignKey(BudgetYear, verbose_name=_("Budget Year"), on_delete=models.CASCADE, related_name='budgets')
    budget_type = models.ForeignKey(BudgetType, verbose_name=_("Budget Type"), on_delete=models.CASCADE, related_name='budgets')
    value = models.FloatField(_("Value"))  # Assuming budget is a float value

    def __str__(self):
        return f"{self.budget_year.year} - {self.budget_type.description}: {self.value}"

    class Meta:
        verbose_name = _("Budget")
        verbose_name_plural = _("Budgets")

class BudgetObjective(models.Model):
    budget = models.ForeignKey(Budget, verbose_name=_("Budget"), on_delete=models.CASCADE, related_name='objectives')
    target_value = models.FloatField(_("Target Value"))
    control_date = models.DateField(_("Control Date"))

    def __str__(self):
        return f"{self.budget.budget_type.description} ({self.control_date}): {self.target_value}"

    class Meta:
        verbose_name = _("Budget Objective")
        verbose_name_plural = _("Budget Objectives")

