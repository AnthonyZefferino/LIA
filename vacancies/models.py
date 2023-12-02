from aziende.models import Company, Office, CompanyRepresentative
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class JobType(models.Model):
    description = models.CharField(_("Description"), max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Job Type")
        verbose_name_plural = _("Jobs Type")


class Qualification(models.Model):
    description = models.CharField(_("Description"), max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Qualification")
        verbose_name_plural = _("Qualifications")


class InsertionType(models.Model):
    description = models.CharField(_("Description"), max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Insertion Type")
        verbose_name_plural = _("Insertions Type")


class ProtectedCategory(models.Model):
    description = models.CharField(_("Description"), max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Protected Category")
        verbose_name_plural = _("Protected Categories")


class Vacancy(models.Model):
    insertion_title = models.CharField(_("Insertion Title"), max_length=255, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    company_representative = models.ForeignKey(CompanyRepresentative, on_delete=models.CASCADE)
    description = models.TextField(_("Description"))
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"))
    insertion_start_date = models.DateField(_("Insertion Start Date"))
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE, verbose_name=_("Job Type"))
    job_specifications = models.TextField(_("Job Specifications"))
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    positions_required = models.IntegerField(_("Number of Positions Required"))
    insertion_type = models.ForeignKey(InsertionType, on_delete=models.CASCADE, verbose_name=_("Insertion Type"))
    insertion_duration = models.CharField(_("Insertion Duration"), max_length=255)
    insertion_finalization = models.BooleanField(_("Insertion Finalization"))
    transfer_available = models.BooleanField(_("Transfer Available"))
    incentives = models.TextField(_("Incentives"))
    car_available = models.BooleanField(_("Car Available"))
    protected_category = models.ManyToManyField(ProtectedCategory, verbose_name=_("Protected Category"))
    previous_experience = models.BooleanField(_("Previous Experience"))
    experience_years = models.IntegerField(_("Experience Years"))
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return f"{self.company} - {self.insertion_title}"

    class Meta:
        verbose_name = _("Vacancy")
        verbose_name_plural = _("Vacancies")


class VacancyFileType(models.Model):
    tipo = models.CharField(_("Type"), max_length=50, unique=True)
    descrizione = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = _("Vacancy File Type")
        verbose_name_plural = _("Vacancy File Types")


class VacancyFile(models.Model):
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_("Vacancy Files")
    )
    tipo_file = models.ForeignKey(
        VacancyFileType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vacancy_files',
        verbose_name=_("File Type")
    )
    file = models.FileField(_("File"), upload_to='vacancy/')
    descrizione = models.CharField(_("Description"), max_length=255, blank=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    def __str__(self):
        return self.descrizione or self.file.name
