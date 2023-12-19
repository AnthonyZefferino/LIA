from django.contrib import admin
from .models import (
    JobType,
    Qualification,
    InsertionType,
    Vacancy,
    VacancyFile,
    ProtectedCategory
)
from utils.models import VacancyCustomFieldValue, CustomField


class VacancyFileInline(admin.TabularInline):
    model = VacancyFile
    extra = 0



class VacancyCustomFieldValueInline(admin.TabularInline):
    model = VacancyCustomFieldValue
    extra = 0
    fields = ['custom_field', 'value', 'required_custom_value']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "custom_field":
            kwargs["queryset"] = CustomField.objects.order_by('group__description', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('description',)


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('description',)


@admin.register(InsertionType)
class InsertionTypeAdmin(admin.ModelAdmin):
    list_display = ('description',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'insertion_title',
        'company',
        'office',
        'company_representative',
        'job_type',
        'qualification',
        'positions_required',
        'insertion_type',
        'insertion_start_date',
        'insertion_end_date',
        'insertion_duration',
        'insertion_finalization',
        'car_available',
        'license',
        'car_owned'
    )
    list_filter = (
        'company',
        'office',
        'insertion_type',
        'job_type',
        'qualification',
        'insertion_start_date',
        'insertion_end_date',
    )
    search_fields = (
        'description',
        'job_specifications',
        'incentives',
        'company__name',
        'office__identifier',
        'company_representative__full_name',
    )
    date_hierarchy = 'insertion_start_date'
    ordering = ('insertion_start_date', 'insertion_end_date')
    inlines = [
        VacancyFileInline
    ]


admin.site.register(ProtectedCategory)
