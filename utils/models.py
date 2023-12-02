from django.db import models
from django.utils.translation import gettext_lazy as _
from vacancies.models import Vacancy


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
    field_type = models.CharField(_("Field Type"), max_length=50, choices=FIELD_TYPES)
    default_value = models.TextField(_("Default Value"), blank=True, null=True)
    question_lia=models.TextField(_("Question for LIA"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Requisito")
        verbose_name_plural = _("Requisiti")


class CustomFieldChoice(models.Model):
    custom_field = models.ForeignKey(CustomField, related_name='choices', on_delete=models.CASCADE)
    value = models.CharField(_("Value"), max_length=255)

    def __str__(self):
        return self.value


class VacancyCustomFieldValue(models.Model):
    vacancy = models.ForeignKey(Vacancy, related_name='custom_field_values', on_delete=models.CASCADE)
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    value = models.TextField(_("Value"))

    def __str__(self):
        return f"{self.custom_field.name}: {self.value}"

class VacancyCustomFieldRequirement(models.Model):
    vacancy = models.ForeignKey(Vacancy, related_name='custom_field_requirements', on_delete=models.CASCADE)
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    is_required = models.BooleanField(_("Is Required"))

    def __str__(self):
        return f"{self.vacancy.insertion_title}: {self.custom_field.name} {'(Required)' if self.is_required else '(Optional)'}"