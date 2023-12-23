from django.contrib import admin
from .models import Candidate, CandidateCustomFieldValue, CandidateFile, CandidatePDF, InterviewType, \
    CandidateProjectVacancyPlacement, InterviewCandidateVacancyProjectHistory, EducationLevel
from utils.models import CustomField, CustomFieldGroup
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class CandidatePDFInline(admin.StackedInline):
    model = CandidatePDF
    extra = 0
    can_delete = False
    max_num = 1


class CandidateFileInline(admin.TabularInline):
    model = CandidateFile
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "custom_field":
            kwargs["queryset"] = CustomField.objects.order_by('group__description', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CandidateProjectVacancyPlacementInline(admin.TabularInline):
    model = CandidateProjectVacancyPlacement
    extra = 0


class CandidateProjectVacancyInterviewInline(admin.TabularInline):
    model = InterviewCandidateVacancyProjectHistory
    extra = 0


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    save_as = True

    def protected_category_display(self, obj):
        return ", ".join(pc.description for pc in obj.protected_category.all())

    protected_category_display.short_description = _("Protected Category")

    list_display = (
        'full_name',
        'job_type',
        'qualification',
        'birth_date',
        'birth_place',
        'address',
        'civic_number',
        'country',
        'phone_number',
        'phone_mobile',
        'email',
        'whatsapp',
        'facebook',
        'instagram',
        'tiktok',
        'license',
    )
    list_filter = (
        'full_name',
        'job_type',
        'qualification',

    )
    search_fields = (
        'full_name', 'email', 'phone', 'mobile'
    )
    # date_hierarchy = 'created_at'
    ordering = ('full_name', 'created_at')
    inlines = [
        CandidatePDFInline, CandidateFileInline,
        CandidateProjectVacancyInterviewInline,
        CandidateProjectVacancyPlacementInline
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.save()


admin.site.register(CandidateCustomFieldValue)
list_display = (
    'candidate.full_name',
    'value',
)

admin.site.register(EducationLevel)
admin.site.register(CandidateProjectVacancyPlacement)
