from django.contrib import admin
from .models import CustomFieldChoice, CustomFieldGroup, CustomField


class CustomFieldChoiceInline(admin.TabularInline):
    model = CustomFieldChoice
    extra = 0


@admin.register(CustomFieldGroup)
class CustomFieldGroupAdmin(admin.ModelAdmin):
    list_display = ['description']


@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'field_type', 'group', 'default_value']
    list_filter = ['group']
