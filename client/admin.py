from django.contrib import admin
from datetime import datetime

from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name',
                    'company_url',
                    'logo',
                    'first_name', 
                    'last_name',
                    'contact_email',
                    'contact_phone', 
                    'billing_address_city', 
                    'billing_address_state',
                    'date_of_contract')

    list_filter = ('company_name', 
                   'billing_address_city', 
                   'billing_address_state',
                   'date_of_contact', 
                   'date_of_contract')
    readonly_fields = ['ytd_revenue',
                    'total_revenue']

    date_hierarchy = 'date_of_contact'