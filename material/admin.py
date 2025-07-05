from django.contrib import admin
from .models import Distributor, DeviceManufacturer, DeviceMaterial, WireMaterial, HardwareMaterial, SoftwareMaterial, LicenseMaterial

class DistributorAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'google_maps_link',
                    'company_url',
                    'logo',
                    'first_name',
                    'last_name',
                    'contact_email',
                    'contact_phone',
                    'summary',
                    'billing_top_address',
                    'billing_address',
                    'billing_address_city',
                    'billing_address_state',
                    'billing_address_zipcode',
                    'contract_info',
                    'dateofcontract',
                    'lastmodification') 

admin.site.register(Distributor, DistributorAdmin)

class DeviceManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'google_maps_link',
                    'company_url',
                    'logo',
                    'first_name',
                    'last_name',
                    'contact_email',
                    'contact_phone',
                    'summary',
                    'manu_top_address',
                    'manu_address',
                    'manu_address_city',
                    'manu_address_state',
                    'manu_address_zipcode',
                    'contract_info',
                    'dateofcontract') 

admin.site.register(DeviceManufacturer, DeviceManufacturerAdmin)

class DeviceMaterialAdmin(admin.ModelAdmin):
    list_display = ('part_disc',
                    'dmfg',
                    'overview',
                    'specifications',
                    'dist_part_num',
                    'manu_part_num',
                    'general_disc',
                    'cost',
                    'msrp',
                    'lastmodification')

admin.site.register(DeviceMaterial, DeviceMaterialAdmin)

class WireMaterialAdmin(admin.ModelAdmin):
    list_display = ('part_disc',
                    'wmfg',
                    'overview',
                    'specifications',
                    'dist_part_num',
                    'manu_part_num',
                    'general_disc',
                    'cost',
                    'msrp',
                    'lastmodification')
    
admin.site.register(WireMaterial, WireMaterialAdmin)

class HardwareMaterialAdmin(admin.ModelAdmin):
    list_display = ('part_disc',
                    'hmfg',
                    'overview',
                    'specifications',
                    'dist_part_num',
                    'manu_part_num',
                    'general_disc',
                    'cost',
                    'msrp',
                    'lastmodification') 
    
admin.site.register(HardwareMaterial, HardwareMaterialAdmin)

class SoftwareMaterialAdmin(admin.ModelAdmin):
    list_display = ('part_disc',
                    'smfg',
                    'overview',
                    'specifications',
                    'dist_part_num',
                    'manu_part_num',
                    'general_disc',
                    'cost',
                    'msrp',
                    'lastmodification')
    
admin.site.register(SoftwareMaterial, SoftwareMaterialAdmin)

class LicenseMaterialAdmin(admin.ModelAdmin):
    list_display = ('part_disc',
                    'dmfg',
                    'overview',
                    'specifications',
                    'dist_part_num',
                    'manu_part_num',
                    'general_disc',
                    'cost',
                    'msrp',
                    'lastmodification')

admin.site.register(LicenseMaterial, LicenseMaterialAdmin)
