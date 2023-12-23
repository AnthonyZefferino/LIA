from pprint import pprint
from django.http import QueryDict
from django.contrib import admin
from .models import  Ticketing,TicketingResponse
from django.urls import reverse, path
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html


class TicketingResponseInline(admin.TabularInline):
    model = TicketingResponse
    extra = 0






@admin.register(Ticketing)
class CompanyRepresentativeAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'candidate',
        'company',
        'office',
        'vacancy',
        'project',
        'placement',
        'ticket_status',
        'ticket_type',
        'user_created',
        'user_assigned',
        'data_viewed',
    )
    # list_filter = (
    #     'address',
    #     'whatsapp',
    # )
    # search_fields = (
    #     'full_name', 'email'
    # )

    inlines = [TicketingResponseInline]

