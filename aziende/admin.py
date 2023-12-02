from pprint import pprint
from django.http import QueryDict
from django.contrib import admin
from .models import Company, Sector, Industry, CompanyFile, FileType, Role, ActivityType, MunicipalityProvince, Country, \
    CompanyRepresentative, RoleHistory, Activity, Office
from django.urls import reverse, path
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html


class CompanyFileInline(admin.TabularInline):
    model = CompanyFile
    extra = 0


class OfficeInline(admin.StackedInline):
    model = Office
    extra = 0


class CompanyRepresentativeInline(admin.StackedInline):
    model = CompanyRepresentative
    extra = 0


class CompanyFileInline(admin.TabularInline):
    model = CompanyFile
    extra = 0


class RoleHistoryInline(admin.StackedInline):
    model = RoleHistory
    extra = 0


class ActivityInline(admin.StackedInline):
    model = Activity
    extra = 0


class CompanyRepresentativeInline(admin.TabularInline):
    model = CompanyRepresentative
    extra = 0  # Numero di forme vuote da visualizzare

    readonly_fields = ('role_history_link', 'activity_link',)

    def role_history_link(self, obj):
        if obj.pk:
            url = reverse('admin:aziende_rolehistory_add') + f'?_popup=1&company_representative={obj.pk}'
            return format_html(
                '<a href="{}" class="related-widget-wrapper-link add-related" id="add_id_role_history" onclick="return showAddAnotherPopup(this);"><img src="/static/admin/img/icon-addlink.svg" alt="Aggiungi"> Aggiungi Ruoli</a>',
                url)
        return ""
        role_history_link.short_description = 'Role History'

    def activity_link(self, obj):
        # L'indirizzo URL di modifica per una nuova istanza di Activity collegata a obj
        url = reverse('aziende:aziende_activity_add') + f'?company_representative={obj.pk}'
        return format_html(f'<a href="{url}">Aggiungi/Modifica Attività</a>') if obj.pk else ""

    activity_link.short_description = 'Activity'


@admin.register(CompanyRepresentative)
class CompanyRepresentativeAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'address',
        'phone_mobile',
        'phone_number',
        'email',
        'fax',
        'whatsapp',
        'instagram',
        'facebook',
        'tiktok',
    )
    list_filter = (
        'address',
        'whatsapp',
    )
    search_fields = (
        'full_name', 'email'
    )

    inlines = [RoleHistoryInline, ActivityInline]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'macro_switch',
        'industry',
        'sector',
        'email',
        'phone_mobile',
        'phone_number',
        'address',
        'website',
        'status',
        'number_employees',
    )
    list_filter = (
        'industry',
        'sector',
    )
    search_fields = (
        'name', 'email'
    )
    inlines = [
        CompanyFileInline,
        OfficeInline,
        CompanyRepresentativeInline,
    ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'industry/<str:industry_name>/',
                self.admin_site.admin_view(self.industry_view),
                name='aziende_industry_view',  # Assicurati che il namespace sia corretto
            ),
        ]
        return custom_urls + urls

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        changelist_filters = request.GET.get('_changelist_filters')
        pprint(changelist_filters)
        if changelist_filters:
            query_dict = QueryDict(changelist_filters)
            industry_filter = query_dict.get('industry__id__exact')
            if industry_filter:
                # Procedi come prima da qui
                extra_context['default_industry'] = industry_filter
                print('extra_context')
                print(extra_context)
        return super().add_view(request, form_url, extra_context=extra_context)

    add_form_template = 'admin/aziende/company/add_form.html'

    def industry_view(self, request, industry_name):
        """
        Questa vista filtra le aziende basandosi sull'industria selezionata
        e reindirizza alla pagina changelist con il filtro applicato.
        """
        # Trova l'ID dell'industria basandosi sul nome.
        industry_id = Industry.objects.get(name=industry_name).id

        # Costruisci l'URL della changelist delle aziende con il filtro applicato.
        changelist_url = reverse(
            'admin:aziende_company_changelist',  # Aggiorna con il tuo 'appname'
            current_app=self.admin_site.name,
        )

        # Aggiungi i parametri del filtro all'URL.
        filtered_url = f"{changelist_url}?industry__id__exact={industry_id}"

        # Reindirizza all'URL filtrato.
        return HttpResponseRedirect(filtered_url)


@admin.register(RoleHistory)
class RoleHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'company_representative', 'role', 'date_from', 'date_to'
    )


admin.site.register(Office)
admin.site.register(Activity)
admin.site.register(Sector)
admin.site.register(Industry)
admin.site.register(FileType)
admin.site.register(Role)
admin.site.register(ActivityType)
admin.site.register(MunicipalityProvince)
admin.site.register(Country)
