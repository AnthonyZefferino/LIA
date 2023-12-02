from django.db import models
from django.utils.translation import gettext_lazy as _
from vacancies.models import Qualification, JobType, ProtectedCategory, Vacancy
from aziende.models import Country, MunicipalityProvince
from utils.models import CustomField
from django.core.exceptions import ValidationError


class Candidate(models.Model):
    full_name = models.CharField(_("Full Name"), max_length=255)
    acquisition_date = models.DateField(_("Acquisition Date"))
    vacancy_start_date = models.DateField(_("Vacancy Start Date"))
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE, verbose_name=_("Job Type"))
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    study_title = models.CharField(_("Study Title"), max_length=255)
    birth_date = models.DateField(_("Birth Date"))
    birth_place = models.CharField(_("Birth Place"), max_length=255)
    address = models.CharField(_("Address"), max_length=255)
    civic_number = models.CharField(_("Civic Number"), max_length=10)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("Country"))
    municipality_province = models.ForeignKey(MunicipalityProvince, on_delete=models.CASCADE,
                                              verbose_name=_("Municipality Province"))
    phone = models.CharField(_("Phone"), max_length=15)
    mobile = models.CharField(_("Mobile"), max_length=15)
    email = models.EmailField(_("Email"))
    whatsapp = models.BooleanField(_("WhatsApp"))
    facebook = models.CharField(_("Facebook"), max_length=255)
    instagram = models.CharField(_("Instagram"), max_length=255)
    tiktok = models.CharField(_("TikTok"), max_length=255)
    license = models.BooleanField(_("Driver's License"))
    car_owned = models.BooleanField(_("Car Owned"))
    protected_category = models.ManyToManyField(ProtectedCategory, verbose_name=_("Protected Category"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return self.full_name


class InterviewType(models.Model):
    description = models.CharField(_("Description"), max_length=255)

    def __str__(self):
        return self.description


class InterviewHistory(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='interviews', verbose_name=_("Candidate"),
                                  on_delete=models.CASCADE, null=True)
    interview_date = models.DateField(_("Interview Date"))
    interview_type = models.ForeignKey(InterviewType, on_delete=models.CASCADE, verbose_name=_("Interview Type"))
    interviewer = models.CharField(_("Interviewer"), max_length=255)
    verbal_evaluation = models.TextField(_("Verbal Evaluation"))
    star_rating = models.IntegerField(_("Star Rating"))
    status = models.CharField(_("Status"), max_length=255)
    notes = models.TextField(_("Notes"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return f"{self.candidate} - {self.interview_date}"



class InterviewCandidateVcancyHistory(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='interviews_candidate', verbose_name=_("Candidate"),
                                  on_delete=models.CASCADE, null=True)
    vacancy = models.ForeignKey(Vacancy, related_name='interviews_vacanciy', verbose_name=_("Vacancy"),
                                on_delete=models.CASCADE, null=True)
    interview_date = models.DateField(_("Interview Date"))
    interview_type = models.ForeignKey(InterviewType, on_delete=models.CASCADE, verbose_name=_("Interview Type"))
    verbal_evaluation = models.TextField(_("Verbal Evaluation"))
    star_rating = models.IntegerField(_("Star Rating"))
    status = models.CharField(_("Status"), max_length=255)
    notes = models.TextField(_("Notes"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return f"{self.candidate} - {self.interview_date}"

    class Meta:
        verbose_name = _("Vacancy Candidate History")
        verbose_name_plural = _("Vacancy Candidates History")


class CandidateCustomFieldValue(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='candidate_custom_field_values', on_delete=models.CASCADE)
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    value = models.TextField(_("Value"))

    def __str__(self):
        return f"{self.custom_field.name}: {self.value}"


class CandidateFileType(models.Model):
    tipo = models.CharField(_("Type"), max_length=50, unique=True)
    descrizione = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = _("Candidate File Type")
        verbose_name_plural = _("Candidate File Types")


class CandidateFile(models.Model):
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
    file = models.FileField(_("File"), upload_to='candidate/files')
    descrizione = models.CharField(_("Description"), max_length=255, blank=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    def __str__(self):
        return self.descrizione or self.file.name

    class Meta:
        verbose_name = _("Candidate Generic File")
        verbose_name_plural = _("Candidate Generic Files")


def validate_file_extension(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError(_("Only PDF files are allowed."))


class CandidatePDF(models.Model):
    candidate = models.OneToOneField(
        Candidate,
        on_delete=models.CASCADE,
        related_name='pdf_file',
        verbose_name=_("Candidate CV")
    )

    file = models.FileField(
        _("PDF File"),
        upload_to='candidate_pdfs/',
        validators=[validate_file_extension]
    )
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.file.name}"

    class Meta:
        verbose_name = _("Candidate Curriculum PDF")
        verbose_name_plural = _("Candidate Curriculum PDFs")
