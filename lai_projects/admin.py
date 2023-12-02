from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Project, BudgetYear, BudgetType, Budget, BudgetObjective
from django.utils.translation import gettext_lazy as _


class BudgetObjectiveInline(admin.TabularInline):
    model = BudgetObjective
    extra = 1
    fk_name = 'budget'


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('display_budget_year_link', 'budget_type', 'value')
    list_select_related = ('budget_year__project', 'budget_type')
    inlines = [BudgetObjectiveInline]

    def display_budget_year_link(self, obj):
        link = reverse("admin:projects_budgetyear_change", args=[obj.budget_year.id])
        return format_html('<a href="{}">{}</a>', link, obj.budget_year)

    display_budget_year_link.short_description = _("Budget Year")

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(BudgetAdmin, self).get_inline_instances(request, obj)


class BudgetInline(admin.TabularInline):
    model = Budget
    extra = 1
    show_change_link = True  # Allows you to click to the Budget detail page
    inlines = [BudgetObjectiveInline]


@admin.register(BudgetYear)
class BudgetYearAdmin(admin.ModelAdmin):
    list_display = ('project', 'year', 'budget_title')
    inlines = [BudgetInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(BudgetYearAdmin, self).get_inline_instances(request, obj)


class BudgetYearInline(admin.StackedInline):
    model = BudgetYear
    extra = 1
    show_change_link = True  # This allows you to click to the BudgetYear detail page


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'company', 'project_type', 'start_date', 'end_date')
    fieldsets = (
        (None, {
            'fields': ('project_title', 'company', 'project_type', 'description',
                       'start_date', 'end_date', 'target', 'lead_partne',
                       'partner', 'supporters')
        }),
    )
    inlines = [BudgetYearInline]


@admin.register(BudgetType)
class BudgetTypeAdmin(admin.ModelAdmin):
    list_display = ('description',)
