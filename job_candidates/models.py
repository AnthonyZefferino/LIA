from django.db import models
from django.utils.translation import gettext_lazy as _
from vacancies.models import Qualification, JobType, ProtectedCategory, Vacancy, StatusVacancy
from aziende.models import Country, MunicipalityProvince, Company, Office
from lai_projects.models import Project
from utils.models import CustomField
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from simple_history.models import HistoricalRecords


class EducationLevel(models.Model):
    description = models.CharField(_("Description"), max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Education Level")
        verbose_name_plural = _("Education Levels")


class Candidate(models.Model):
    full_name = models.CharField(_("Full Name"), max_length=255)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE, verbose_name=_("Job Type Preference Candidate"),
                                 null=True)
    STATUS_CHOICES = [
        ('unemployed', _('Unemployed')),
        ('employed', _('Employed')),
        ('awaiting_interview', _('Awaiting Interview')),
        ('interviewed', _('Interviewed')),
    ]
    status = models.CharField(
        _("Status Candidate"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='disoccupato',
    )

    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name=_("Education Level"))
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('male', _('male')),
        ('female', _('female'))
    ]
    gender = models.CharField(_("Gender"), max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(_("Birth Date"))
    birth_place = models.CharField(_("Birth Place"), max_length=255)
    address = models.CharField(_("Address"), max_length=255)
    civic_number = models.CharField(_("Civic Number"), max_length=10)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("Country"), default=1)
    municipality_province = models.ForeignKey(MunicipalityProvince, on_delete=models.CASCADE,
                                              verbose_name=_("Municipality Province"), default=7292)
    postal_code = models.CharField(_("Postal Code"), max_length=5, blank=True, null=True)
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True, null=True)
    phone_mobile = models.CharField(_("Phone Mmobile"), max_length=15, blank=True, null=True)
    email = models.EmailField(_("Email"))
    whatsapp = models.BooleanField(_("WhatsApp"))
    facebook = models.CharField(_("Facebook"), max_length=255)
    instagram = models.CharField(_("Instagram"), max_length=255)
    tiktok = models.CharField(_("TikTok"), max_length=255)
    license = models.BooleanField(_("Driver's License"))
    car_owned = models.BooleanField(_("Car Owned"))
    protected_category = models.ManyToManyField(ProtectedCategory, verbose_name=_("Protected Category"))
    description = models.TextField(_("Description"), blank=True, null=True)
    evaluation_lavoriamoci = models.TextField(_("Evaluation Lavoriamoci"), blank=True, null=True)
    description_lia = models.TextField(_("Description LIA"), blank=True, null=True)
    last_lia_analysis = models.JSONField(_("Last Lia analysis"), blank=True, null=True)
    black_list = models.BooleanField(_("black_list"), null=True)
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _("Candidate")
        verbose_name_plural = _("Candidates")


class InterviewType(models.Model):
    description = models.CharField(_("Description"), max_length=255)

    def __str__(self):
        return self.description


class InterviewCandidateVacancyProjectHistory(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='interviews_candidate', verbose_name=_("Candidate"),
                                  on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, related_name='interview_company', verbose_name=_("Company"),
                                limit_choices_to={'industry__id': 2},
                                on_delete=models.CASCADE, null=True, blank=True)
    office = models.ForeignKey(Office, related_name='interview_office', verbose_name=_("office"),
                               on_delete=models.CASCADE, null=True, blank=True)
    vacancy = models.ForeignKey(Vacancy, related_name='interviews_vacanciy', verbose_name=_("Vacancy"),
                                on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, related_name='interviews_project', verbose_name=_("Project"),
                                on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"), null=True)
    interview_date = models.DateField(_("Interview Date"))
    interview_type = models.ForeignKey(InterviewType, on_delete=models.CASCADE, verbose_name=_("Interview Type"))
    verbal_evaluation = models.TextField(_("Verbal Evaluation"))
    star_rating = models.IntegerField(_("Star Rating"))
    status_candidate = models.CharField(
        _("Status Inserted"),
        max_length=10,
        choices=(('Terminate', _('Terminate')), ('pending', _('Pending')), ('Refuse', _('Refuse Candidate'))),
        default='open'
    )
    status_interview = models.CharField(
        _("Status Inserted"),
        max_length=10,
        choices=(('complete', _('Complete')), ('pending', _('Pending')), ('refuse', _('Refuse'))),
        default='open'
    )
    notes = models.TextField(_("Notes"))
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return f"{self.candidate} - {self.interview_date}"

    class Meta:
        verbose_name = _("Interniew Vacancy - Project Candidate History")
        verbose_name_plural = _("Interniew Vacancy - Project Candidate Histories")


class CandidateCustomFieldValue(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='candidate_custom_field_values', on_delete=models.CASCADE)
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    value = models.TextField(_("Value"))
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate.full_name}|{self.custom_field.name}: {self.value}"

    class Meta:
        verbose_name = _("Requirement Candidate value")
        verbose_name_plural = _("Requirement Candidate values")
        ordering = ['candidate__full_name']


class CandidateFileType(models.Model):
    tipo = models.CharField(_("Type"), max_length=50, unique=True)
    description_file = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = _("Candidate File Type")
        verbose_name_plural = _("Candidate File Types")


class CandidateFile(models.Model):
    def candidate_file_upload_to(instance, filename):
        return f'files_candidate/{instance.candidate.id}/{filename}'

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_("Candidate Files")
    )
    tipo_file = models.ForeignKey(
        CandidateFileType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='candidate_files',
        verbose_name=_("File Type")
    )
    file = models.FileField(_("File"), upload_to=candidate_file_upload_to)
    description_file = models.CharField(_("Description"), max_length=255, blank=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    def __str__(self):
        return self.description_file or self.file.name

    class Meta:
        verbose_name = _("Candidate Generic File")
        verbose_name_plural = _("Candidate Generic Files")


def validate_file_extension(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError(_("Only PDF files are allowed."))


def candidate_file_curriculum_upload_to(instance, filename):
    return f'files_candidate/{instance.candidate.id}/curriculum/{filename}'


class CandidatePDF(models.Model):
    candidate = models.OneToOneField(
        Candidate,
        on_delete=models.CASCADE,
        related_name='pdf_file',
        verbose_name=_("Candidate CV")
    )

    file = models.FileField(
        _("PDF File"),
        upload_to=candidate_file_curriculum_upload_to,
        validators=[validate_file_extension]
    )
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.file.name}"

    class Meta:
        verbose_name = _("Candidate Curriculum PDF")
        verbose_name_plural = _("Candidate Curriculum PDFs")


class CandidateProjectVacancyPlacement(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name=_("Company Placement"),
        related_name='company_project_vacancy_placement',
        limit_choices_to={'industry__id': 2}
    )
    office = models.ForeignKey(Office, related_name='placement_office', verbose_name=_("office"),
                               on_delete=models.CASCADE, null=True, blank=True)
    vacancy = models.ForeignKey(Vacancy, related_name='placement_vacanciy', verbose_name=_("Vacancy"),
                                on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, related_name='placement_project', verbose_name=_("Project"),
                                on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        _("Status Inserted"),
        max_length=10,
        choices=(('closed', _('Closed')), ('pending', _('Pending')), ('open', _('Open'))),
        default='open'
    )
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE, verbose_name=_("Job Type Placement"), null=True)
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        verbose_name=_("Candidate Inserted"),
        related_name='candidate_project_placements'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"), null=True)
    note = models.TextField(_("note"), blank=True)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"))
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.company.name}"

    class Meta:
        verbose_name = _("Candidate Placement")
        verbose_name_plural = _("Candidate Placements")
