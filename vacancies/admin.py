from django.contrib import admin
from .models import (
    JobType,
    Qualification,
    InsertionType,
    ProtectedCategory,
    Vacancy,
    CompanyRepresentative,
    VacancyFile
)
from utils.models import VacancyCustomFieldValue, CustomField, CustomFieldGroup, VacancyCustomFieldRequirement
from job_candidates.models import InterviewCandidateVcancyHistory


class VacancyFileInline(admin.TabularInline):
    model = VacancyFile
    extra = 1


class InterviewCandidateVcancyHistoryInline(admin.TabularInline):
    model = InterviewCandidateVcancyHistory
    extra = 1
    fields = ['candidate', 'vacancy', 'interview_date', 'interview_type', 'verbal_evaluation', 'star_rating']


class VacancyCustomFieldValueInline(admin.TabularInline):
    model = VacancyCustomFieldValue
    extra = 1
    fields = ['custom_field', 'value']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "custom_field":
            kwargs["queryset"] = CustomField.objects.order_by('group__description', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CompanyRepresentativeInline(admin.StackedInline):
    model = CompanyRepresentative
    extra = 1  # Numero di form vuoti da mostrare.


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('description',)


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('description',)


@admin.register(InsertionType)
class InsertionTypeAdmin(admin.ModelAdmin):
    list_display = ('description',)


@admin.register(ProtectedCategory)
class ProtectedCategoryAdmin(admin.ModelAdmin):
    list_display = ('description',)


class VacancyCustomFieldRequirementInline(admin.TabularInline):
    model = VacancyCustomFieldRequirement
    extra = 1


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'office',
        'company_representative',
        'description',
        'start_date',
        'end_date',
        'insertion_start_date',
        'job_type',
        'qualification',
        'positions_required',
        'insertion_type',
        'insertion_duration',
        'insertion_finalization',
        'transfer_available',
        'car_available',
        'previous_experience',
        'experience_years',
    )
    list_filter = (
        'company',
        'office',
        'insertion_type',
        'job_type',
        'qualification',
        'start_date',
        'end_date',
    )
    search_fields = (
        'description',
        'job_specifications',
        'incentives',
        'company__name',
        'office__identifier',
        'company_representative__full_name',
    )
    date_hierarchy = 'start_date'
    ordering = ('start_date', 'end_date')
    inlines = [
        VacancyFileInline,InterviewCandidateVcancyHistoryInline
    ]

    admin.site.register(VacancyCustomFieldRequirement)

    def render_change_form(self, request, context, *args, **kwargs):
        context['custom_field_groups'] = CustomFieldGroup.objects.prefetch_related('custom_fields__choices').all()
        return super().render_change_form(request, context, *args, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Override della funzione save_model per gestire il salvataggio
        dei campi personalizzati insieme all'istanza di Vacancy.
        """
        # Salvataggio dell'oggetto Vacancy
        super().save_model(request, obj, form, change)

        # Salvataggio dei valori dei campi personalizzati
        for custom_field in CustomField.objects.all():
            field_name = f'custom_{custom_field.id}'

            # Ottieni il valore dal form; per i campi 'set', ottieni l'elenco dei valori selezionati
            field_value = form.cleaned_data.get(field_name, '')
            if custom_field.field_type == 'set':
                field_value = ';'.join(form.cleaned_data.get(field_name,
                                                             []))  # Per esempio, unisci i valori in una stringa separata da ";"

            # Trova e aggiorna il valore esistente, oppure crea un nuovo oggetto VacancyCustomFieldValue
            custom_field_value, created = VacancyCustomFieldValue.objects.get_or_create(
                vacancy=obj, custom_field=custom_field, defaults={'value': field_value}
            )
            if not created:
                custom_field_value.value = field_value
                custom_field_value.save()

            # Ottieni o crea l'oggetto VacancyCustomFieldRequirement

            requirement_field_name = f'custom_requirement_{custom_field.id}'
            is_required = request.POST.get(requirement_field_name) == 'on'
            requirement, created = VacancyCustomFieldRequirement.objects.get_or_create(
                vacancy=obj,
                custom_field=custom_field,
                defaults={'is_required': is_required}
            )
            # Se l'oggetto esiste già e il valore di `is_required` è diverso, aggiornalo.
            if not created and requirement.is_required != is_required:
                requirement.is_required = is_required
                requirement.save()
