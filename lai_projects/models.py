from aziende.models import Company
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from vacancies.models import ProtectedCategory


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
        verbose_name=_("Ente"),
        limit_choices_to={'industry__id': 1},
        related_name='company_project'
    )
    status = models.CharField(
        _("Status Project"),
        max_length=10,
        choices=(('closed', _('Closed')), ('pending', _('Pending')), ('open', _('Open'))),
        default='open'
    )
    description = models.TextField(_("Description"), blank=True, null=True)
    start_date = models.DateField(_("Start Date"), default=timezone.now)
    amount = models.IntegerField(_("Amount"), default=0)
    end_date = models.DateField(_("End Date"), blank=True, null=True)
    target = models.ManyToManyField('TargetProject', verbose_name=_("Project Targets"), blank=True)
    lead_partner = models.ManyToManyField(
        Company,
        verbose_name=_("Lead Partner"),
        related_name='lead_projects',
        limit_choices_to={'industry__id': 2}, blank=True
    )
    partner = models.ManyToManyField(
        Company,
        verbose_name=_("Partners"),
        related_name='partnered_projects',
        limit_choices_to={'industry__id': 2}, blank=True
    )
    supporters = models.ManyToManyField(
        Company,
        verbose_name=_("Supporters"),
        related_name='supporting_projects',
        limit_choices_to={'industry__id': 4}, blank=True
    )

    protected_category = models.ManyToManyField(ProtectedCategory, verbose_name=_("Protected Category"))
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return f"{self.company} - {self.project_title}"

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class ProjectFileType(models.Model):
    tipo = models.CharField(_("Type"), max_length=50, unique=True)
    description = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = _("Project File Type")
        verbose_name_plural = _("Project File Types")


class ProjectFile(models.Model):
    def project_file_upload_to(instance, filename):
        # Upload to 'files_aziende/<company_id>/' directory
        return f'files_project/{instance.project.id}/{filename}'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_("Project Files")
    )
    tipo_file = models.ForeignKey(
        ProjectFileType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vacancy_files',
        verbose_name=_("File Type")
    )
    file = models.FileField(_("File"), upload_to=project_file_upload_to)
    description = models.CharField(_("Description"), max_length=255, blank=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    def __str__(self):
        return self.description or self.file.name


class BudgetYear(models.Model):
    budget_title = models.CharField(_("Budget Title"), max_length=255, blank=True, null=True)
    project = models.ForeignKey('Project', verbose_name=_("Project"), on_delete=models.CASCADE,
                                related_name='budget_years')
    year = models.PositiveIntegerField(_("Year"), default=timezone.now().year)
    start_date = models.DateField(_("Start Date"), default=timezone.now)
    end_date = models.DateField(_("End Date"), blank=True, null=True)

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
    budget_year = models.ForeignKey(BudgetYear, verbose_name=_("Budget Year"), on_delete=models.CASCADE,
                                    related_name='budgets')
    budget_type = models.ForeignKey(BudgetType, verbose_name=_("Budget Type"), on_delete=models.CASCADE,
                                    related_name='budgets')
    value_type = models.FloatField(_("Value type"))
    value_consolidate = models.FloatField(_("Value Consolidate"), blank=True, null=True)
    value_consolidate_percentage = models.FloatField(_("Value Consolidate percentage"), blank=True, null=True)

    def __str__(self):
        return f"{self.budget_year.year} - {self.budget_type.description}: {self.value_type}"

    class Meta:
        verbose_name = _("Budget")
        verbose_name_plural = _("Budgets")


class BudgetObjective(models.Model):
    budget_year = models.ForeignKey(BudgetYear, on_delete=models.CASCADE, blank=True, null=True)
    target_value = models.FloatField(_("Target Value"))
    control_date = models.DateField(_("Control Date"))
    control_result = models.FloatField(_("Control Result"), blank=True, null=True)
    control_result_percentage = models.FloatField(_("Control Result Percentage"), blank=True, null=True)

    def __str__(self):
        return f"{self.budget_year.budget_title} ({self.control_date}): {self.target_value}"

    class Meta:
        verbose_name = _("Budget Objective")
        verbose_name_plural = _("Budget Objectives")


