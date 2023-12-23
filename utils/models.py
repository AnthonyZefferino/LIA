from django.db import models
from django.utils.translation import gettext_lazy as _
from vacancies.models import Vacancy
from lai_projects.models import Project


class CustomFieldGroup(models.Model):
    description = models.CharField(_("Description"), max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Gruppo Requisiti")
        verbose_name_plural = _("Gruppi Requisiti")


class CustomField(models.Model):
    FIELD_TYPES = (
        ('number', _('Number')),
        ('date', _('Date')),
        ('string', _('String')),
        ('text', _('Text')),
        ('enum', _('Enum')),
        ('set', _('Set')),
    )

    group = models.ForeignKey(CustomFieldGroup, related_name='custom_fields', on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=255)
    label = models.CharField(_("Label"), max_length=255, blank=True, null=True)
    field_type = models.CharField(_("Field Type"), max_length=50, choices=FIELD_TYPES)
    list_values = models.TextField(_("Listt Values"), blank=True, null=True)
    default_value = models.CharField(_("Default Value"), max_length=255, blank=True, null=True)
    question_lia = models.TextField(_("Question for LIA"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Requisito Campo Custom")
        verbose_name_plural = _("Requisiti Campi Custom")


class CustomFieldChoice(models.Model):
    vacancy = models.ForeignKey(Vacancy, related_name='custom_field_choice', on_delete=models.CASCADE,
                                blank=True, null=True)
    custom_field = models.ForeignKey(CustomField, related_name='choices_field', on_delete=models.CASCADE)
    value = models.CharField(_("Value Custom"), max_length=255)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = _("Requisito custom valore")
        verbose_name_plural = _("Requisiti custom valori")


class CustomFieldChoiceProject(models.Model):
    project = models.ForeignKey(Project, related_name='project_custom_field_values', on_delete=models.CASCADE,
                                blank=True, null=True)
    custom_field = models.ForeignKey(CustomField, related_name='project_custom_field',
                                     on_delete=models.CASCADE)
    value = models.CharField(_("Value"), max_length=255)
    required_custom_value = models.BooleanField(_("required custom value"), default=True)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = ['project', 'custom_field']
        verbose_name = _("Requisito Project valore")
        verbose_name_plural = _("Requisiti Project valori")


class VacancyCustomFieldValue(models.Model):
    vacancy = models.ForeignKey(Vacancy, related_name='vacancy_custom_field_values', on_delete=models.CASCADE)
    custom_field = models.ForeignKey(CustomField, related_name='vacancy_custom_field',
                                     on_delete=models.CASCADE)
    value = models.TextField(_("Value"))
    required_custom_value = models.BooleanField(_("required custom value"), default=True)

    def __str__(self):
        return f"{self.custom_field.name}: {self.value}: {self.required_custom_value}"

    class Meta:
        unique_together = ['vacancy', 'custom_field']
        verbose_name = _("Requisito Vacancy valore")
        verbose_name_plural = _("Requisiti Vacancy valori")

