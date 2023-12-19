from aziende.models import Company, Office, CompanyRepresentative
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from simple_history.models import HistoricalRecords
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


class StatusVacancy(models.Model):
    description = models.CharField(_("Description"), max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Vacancy Status")
        verbose_name_plural = _("Vacancies Status")

    @classmethod
    def get_default(cls):
        return cls.objects.get_or_create(description='Default')[0].id


class Vacancy(models.Model):
    insertion_title = models.CharField(_("Insertion Title"), max_length=255, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,  limit_choices_to={'industry__id': 2})
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusVacancy, on_delete=models.CASCADE, default=StatusVacancy.get_default)
    company_representative = models.ForeignKey(CompanyRepresentative, on_delete=models.CASCADE)
    description = models.TextField(_("Description") ,null=True, blank=True)
    numbers=models.IntegerField(_("Numbers"), null=True, blank=True)
    responsibilities = models.TextField(_("Responsibilities"), null=True, blank=True)
    location_vacancies = models.TextField(_("Location"), null=True, blank=True)
    insertion_start_date = models.DateField(_("Insertion Start Date"), default=timezone.now)
    insertion_end_date = models.DateField(_("Insertion End Date"), default=timezone.now)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE, verbose_name=_("Job Type"))
    job_specifications = models.TextField(_("Job Specifications"))
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    positions_required = models.IntegerField(_("Number of Positions Required"))
    insertion_type = models.ForeignKey(InsertionType, on_delete=models.CASCADE, verbose_name=_("Insertion Type"))
    insertion_duration = models.CharField(_("Insertion Duration"), max_length=255)
    insertion_finalization = models.BooleanField(_("Insertion Finalization"))
    incentives = models.TextField(_("Incentives"), null=True, blank=True)
    car_available = models.BooleanField(_("Car Available"))
    protected_category = models.ManyToManyField(ProtectedCategory, verbose_name=_("Protected Category"))
    license = models.BooleanField(_("Driver's License"), blank=True, null=True)
    car_owned = models.BooleanField(_("Car Owned"), default=False)
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    history = HistoricalRecords()  # new line
    def __str__(self):
        return f"{self.company} - {self.insertion_title}"

    class Meta:
        verbose_name = _("Vacancy")
        verbose_name_plural = _("Vacancies")


class VacancyFileType(models.Model):
    tipo = models.CharField(_("Type"), max_length=50, unique=True)
    description = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = _("Vacancy File Type")
        verbose_name_plural = _("Vacancy File Types")


class VacancyFile(models.Model):
    def vacancy_file_upload_to(instance, filename):
        return f'files_vacancy/{instance.vacancy.id}/{filename}'

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
    file = models.FileField(_("File"), upload_to=vacancy_file_upload_to)
    description = models.CharField(_("Description"), max_length=255, blank=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    def __str__(self):
        return self.description or self.file.name
