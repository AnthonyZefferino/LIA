from django.contrib import admin
from .models import Candidate, InterviewHistory, CandidateCustomFieldValue, CandidateFile,CandidatePDF
from utils.models import VacancyCustomFieldValue, CustomField, CustomFieldGroup
from django.utils.translation import gettext_lazy as _

class CandidatePDFInline(admin.StackedInline):
    model = CandidatePDF
    extra = 0
    can_delete = False
    max_num = 1

class CandidateFileInline(admin.TabularInline):
    model = CandidateFile
    extra = 1


class InterviewHistoryInline(admin.TabularInline):  # O usa admin.StackedInline se preferisci quello stile.
    model = InterviewHistory
    extra = 1


class CandidateCustomFieldValueInline(admin.TabularInline):
    model = CandidateCustomFieldValue
    extra = 1
    fields = ['custom_field', 'value']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "custom_field":
            kwargs["queryset"] = CustomField.objects.order_by('group__description', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):

    def protected_category_display(self, obj):
        return ", ".join(pc.description for pc in obj.protected_category.all())

    protected_category_display.short_description = _("Protected Category")

    list_display = (
        'full_name',
        'acquisition_date',
        'vacancy_start_date',
        'job_type',
        'qualification',
        'study_title',
        'birth_date',
        'birth_place',
        'address',
        'civic_number',
        'country',
        'phone',
        'mobile',
        'email',
        'whatsapp',
        'facebook',
        'instagram',
        'tiktok',
        'license',
        'protected_category_display',
    )
    list_filter = (
        'full_name',
        'acquisition_date',
        'vacancy_start_date',
        'job_type',
        'qualification',
        'study_title',

    )
    search_fields = (
        'full_name', 'email', 'phone', 'mobile'
    )
    date_hierarchy = 'acquisition_date'
    ordering = ('full_name', 'acquisition_date')
    inlines = [
        CandidatePDFInline,  CandidateFileInline, InterviewHistoryInline,
    ]

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
                                                             []))
            # Trova e aggiorna il valore esistente, oppure crea un nuovo oggetto VacancyCustomFieldValue
            custom_field_value, created = VacancyCustomFieldValue.objects.get_or_create(
                vacancy=obj, custom_field=custom_field, defaults={'value': field_value}
            )
            if not created:
                custom_field_value.value = field_value
                custom_field_value.save()
