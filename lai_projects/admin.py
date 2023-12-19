from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Project, BudgetType, Budget, BudgetObjective, TargetProject, ProjectFile, BudgetYear
from django.utils.translation import gettext_lazy as _
from utils.models import CustomFieldChoiceProject


class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 0





class BudgetObjectiveInline(admin.TabularInline):
    model = BudgetObjective
    extra = 0
    fk_name = 'budget_year'



class BudgetInline(admin.TabularInline):
    model = Budget
    extra = 0
    show_change_link = True
    inlines = [BudgetObjectiveInline]


@admin.register(BudgetYear)
class BudgetYearAdmin(admin.ModelAdmin):
    list_display = ('project', 'year', 'budget_title')
    list_filter = (
        'project',
        'year',
    )
    inlines = [BudgetInline, BudgetObjectiveInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(BudgetYearAdmin, self).get_inline_instances(request, obj)

class BudgetTypeInline(admin.StackedInline):
    model = BudgetType
    extra = 0
    show_change_link = True  # This allows you to click to the BudgetYear detail page
class BudgetYearInline(admin.StackedInline):
    model = BudgetYear
    extra = 0
    show_change_link = True  # This allows you to click to the BudgetYear detail page


class CustomFieldChoiceProjectInline(admin.TabularInline):
    model = CustomFieldChoiceProject
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('project_title', 'company', 'status', 'start_date', 'end_date')
    fieldsets = (
        (None, {
            'fields': ('project_title', 'amount', 'company', 'description',
                       'start_date', 'end_date', 'target', 'lead_partner',
                       'partner', 'supporters', 'protected_category')
        }),
    )
    inlines = [CustomFieldChoiceProjectInline, ProjectFileInline]




