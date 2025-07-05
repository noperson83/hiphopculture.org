from django.db import models
from datetime import date
from django.conf import settings    

class Distributor(models.Model):
    name                    = models.CharField(max_length=40, help_text="Enter a Distributor name.")
    google_maps_link        = models.CharField(max_length=200, null=True, blank=True, help_text='Google map link')
    company_url             = models.CharField(max_length=100, blank=True, help_text='Web page')
    logo                    = models.ImageField(upload_to='uploads/distributor/logo_pics/%Y/%m/%d/', null=True, blank=True, max_length=60, help_text='distlogopic.jpg')
    first_name              = models.CharField(max_length=100, blank=True, help_text='Contact first name')
    last_name               = models.CharField(max_length=100, blank=True, help_text='Contact last name')
    contact_email           = models.EmailField(max_length=254, blank=True, help_text='Contact@email.com')
    contact_phone           = models.CharField(max_length=17, blank=True, help_text='Contact phone number')
    summary                 = models.TextField(max_length=1000, blank=True, help_text='Enter a brief description of the Building or Orginization')
    billing_top_address     = models.CharField(max_length=100, blank=True, help_text='Attn: John Doe')
    billing_address         = models.CharField(max_length=100, default='1234 N Strong. Dr', blank=True, help_text='Distributor address')
    billing_address_city    = models.CharField(max_length=100, blank=True, help_text='Distributor city')
    billing_address_state   = models.CharField(max_length=100, blank=True, help_text='Distributor state')
    billing_address_zipcode = models.CharField(max_length=100, blank=True, help_text='Distributor zip')
    contract_info           = models.TextField(max_length=4000, null=True, blank=True, help_text='Contract Information')
    dateofcontract          = models.DateTimeField(blank=True, null=True, help_text='Contract start date')
    lastmodification        = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class DeviceManufacturer(models.Model):
    name                    = models.CharField(max_length=40, help_text="Enter a device manufacturer")
    distributor             = models.ManyToManyField('Distributor', blank=True, related_name='Distributor', help_text='Select possable distributors')
    google_maps_link        = models.CharField(max_length=200, null=True, blank=True, help_text='Google map link')
    company_url             = models.CharField(max_length=100, blank=True, help_text='Web page')
    logo                    = models.ImageField(upload_to='uploads/distributor/logo_pics/%Y/%m/%d/', null=True, blank=True, max_length=60, help_text='devicelogopic.jpg')
    first_name              = models.CharField(max_length=100, blank=True, help_text='Contact first name')
    last_name               = models.CharField(max_length=100, blank=True, help_text='Contact last name')
    contact_email           = models.EmailField(max_length=254, blank=True, help_text='Contact@email.com')
    contact_phone           = models.CharField(max_length=17, blank=True, help_text='Contact phone number')
    summary                 = models.TextField(max_length=1000, blank=True, help_text='Enter a brief description of the Building or Orginization')
    manu_top_address        = models.CharField(max_length=100, blank=True, help_text='Attn: John Doe')
    manu_address            = models.CharField(max_length=100, default='1234 N Strong. Dr', blank=True, help_text='Manufacturer address')
    manu_address_city       = models.CharField(max_length=100, blank=True, help_text='Manufacturer city')
    manu_address_state      = models.CharField(max_length=100, blank=True, help_text='Manufacturer state')
    manu_address_zipcode    = models.CharField(max_length=100, blank=True, help_text='Manufacturer zip')
    contract_info           = models.TextField(max_length=4000, null=True, blank=True, help_text='Contract Information')
    dateofcontract          = models.DateTimeField(blank=True, null=True, help_text='Contract start date')

    lastmodification        = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class DeviceMaterial(models.Model):
    dist            = models.ManyToManyField('Distributor', blank=True, related_name="ddistributor", related_query_name="ddistributor", help_text='distributor')
    dmfg            = models.ForeignKey('DeviceManufacturer', on_delete=models.SET_NULL, null=True, related_name="dmanufacturer", related_query_name="dmanufacturer", help_text='dManufacturer')
    pic_link       = models.CharField(max_length=200, null=True, blank=True, help_text='web link https://embed.widencdn.net/img/crestron/46o04kr8yb/exact/photo_cp3_comp.jpeg')
    install_link   = models.CharField(max_length=200, null=True, blank=True, help_text='web link https://embed.crestron.net/mg_rg_3-series_control_systems.pdf')
    overview        = models.TextField(max_length=1000, blank=True, help_text='Enter an overview')
    specifications  = models.TextField(max_length=1000, blank=True, help_text='Enter specifications')
    dist_part_num   = models.CharField(max_length=60, blank=True, help_text="Enter the distributors part number.")
    manu_part_num   = models.CharField(max_length=60, blank=True, help_text="Enter the manufacturers part number.")
    general_disc    = models.CharField(max_length=200, help_text="Enter a general description.")
    part_disc       = models.CharField(max_length=200, blank=True, help_text="Enter manufacture name.")
    cost            = models.DecimalField(max_digits=18, decimal_places=2, default='0.65', help_text='Cost')
    msrp            = models.DecimalField(max_digits=18, decimal_places=2, default='1.00', help_text='MSRP')
    
    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.part_disc

class WireMaterial(models.Model):
    dist            = models.ManyToManyField('Distributor', blank=True, related_name="wdistributor", related_query_name="wdistributor", help_text='wdistributor')
    wmfg            = models.ForeignKey('DeviceManufacturer', on_delete=models.SET_NULL, null=True, related_name="wmanufacturer", related_query_name="wmanufacturer", help_text='wManufacturer')
    pic_link       = models.CharField(max_length=200, null=True, blank=True, help_text='web link https://embed.widencdn.net/img/crestron/46o04kr8yb/exact/photo_cp3_comp.jpeg')
    install_link   = models.CharField(max_length=200, null=True, blank=True, help_text='web link https://embed.crestron.net/mg_rg_3-series_control_systems.pdf')
    overview        = models.TextField(max_length=1000, blank=True, help_text='Enter an overview')
    specifications  = models.TextField(max_length=1000, blank=True, help_text='Enter specifications')
    dist_part_num   = models.CharField(max_length=60, blank=True, help_text="Enter the distributors part number.")
    manu_part_num   = models.CharField(max_length=60, blank=True, help_text="Enter the manufacturers part number.")
    general_disc    = models.CharField(max_length=200, help_text="Enter a general description.")
    part_disc       = models.CharField(max_length=200, blank=True, help_text="Enter manufacture name.")
    cost            = models.DecimalField(max_digits=18, decimal_places=2, default='0.60', help_text='Cost')
    msrp            = models.DecimalField(max_digits=18, decimal_places=2, default='1.00', help_text='MSRP')

    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.part_disc

class HardwareMaterial(models.Model):
    dist            = models.ManyToManyField('Distributor', blank=True, related_name="hdistributor", related_query_name="hdistributor", help_text='hdistributor')
    hmfg            = models.CharField(max_length=60, unique=True, help_text="Enter a manufacturer.")
    pic_link       = models.CharField(max_length=200, null=True, blank=True, help_text='web link https://embed.widencdn.net/img/crestron/46o04kr8yb/exact/photo_cp3_comp.jpeg')
    install_link   = models.CharField(max_length=200, null=True, blank=True, help_text='web link https://embed.crestron.net/mg_rg_3-series_control_systems.pdf')
    overview        = models.TextField(max_length=1000, blank=True, help_text='Enter an overview')
    specifications  = models.TextField(max_length=1000, blank=True, help_text='Enter specifications')
    dist_part_num   = models.CharField(max_length=60, blank=True, help_text="Enter the distributors part number.")
    manu_part_num   = models.CharField(max_length=60, blank=True, help_text="Enter the manufacturers part number.")
    general_disc    = models.CharField(max_length=200, help_text="Enter a general description.")
    part_disc       = models.CharField(max_length=200, blank=True, help_text="Enter manufacture name.")
    cost            = models.DecimalField(max_digits=18, decimal_places=2, default='0.60', help_text='Cost')
    msrp            = models.DecimalField(max_digits=18, decimal_places=2, default='1.00', help_text='MSRP')
    
    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.part_disc

class SoftwareMaterial(models.Model):
    dist            = models.ManyToManyField('Distributor', blank=True, related_name="sdistributor", related_query_name="sdistributor", help_text='sdistributor')
    smfg            = models.ForeignKey('DeviceManufacturer', on_delete=models.SET_NULL, null=True, related_name="smanufacturer", related_query_name="smanufacturer", help_text='sManufacturer')
    pic_link        = models.CharField(max_length=200, null=True, blank=True, help_text='web link https://embed.widencdn.net/img/crestron/46o04kr8yb/exact/photo_cp3_comp.jpeg')
    install_link    = models.CharField(max_length=200, null=True, blank=True, help_text='web link https://embed.crestron.net/mg_rg_3-series_control_systems.pdf')
    overview        = models.TextField(max_length=1000, blank=True, help_text='Enter an overview')
    specifications  = models.TextField(max_length=1000, blank=True, help_text='Enter specifications')
    dist_part_num   = models.CharField(max_length=60, blank=True, help_text="Enter the distributors part number.")
    manu_part_num   = models.CharField(max_length=60, blank=True, help_text="Enter the manufacturers part number.")
    general_disc    = models.CharField(max_length=200, help_text="Enter a general description.")
    part_disc       = models.CharField(max_length=200, blank=True, help_text="Enter manufacture name.")
    cost            = models.DecimalField(max_digits=18, decimal_places=2, default='0.65', help_text='Cost')
    msrp            = models.DecimalField(max_digits=18, decimal_places=2, default='1.00', help_text='MSRP')
    
    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.part_disc

class LicenseMaterial(models.Model):
    dist            = models.ManyToManyField('Distributor', blank=True, related_name="ldistributor", related_query_name="ldistributor", help_text='distributor')
    dmfg            = models.ForeignKey('DeviceManufacturer', on_delete=models.SET_NULL, null=True, related_name="lmanufacturer", related_query_name="lmanufacturer", help_text='dManufacturer')
    pic_link        = models.CharField(max_length=200, null=True, blank=True, help_text='web link https://embed.widencdn.net/img/crestron/46o04kr8yb/exact/photo_cp3_comp.jpeg')
    install_link    = models.CharField(max_length=200, null=True, blank=True, help_text='web link https://embed.crestron.net/mg_rg_3-series_control_systems.pdf')
    overview        = models.TextField(max_length=1000, blank=True, help_text='Enter an overview')
    specifications  = models.TextField(max_length=1000, blank=True, help_text='Enter specifications')
    dist_part_num   = models.CharField(max_length=60, blank=True, help_text="Enter the distributors part number.")
    manu_part_num   = models.CharField(max_length=60, blank=True, help_text="Enter the manufacturers part number.")
    general_disc    = models.CharField(max_length=200, help_text="Enter a general description.")
    part_disc       = models.CharField(max_length=200, blank=True, help_text="Enter manufacture name.")
    cost            = models.DecimalField(max_digits=18, decimal_places=2, default='0.65', help_text='Cost')
    msrp            = models.DecimalField(max_digits=18, decimal_places=2, default='1.00', help_text='MSRP')
    
    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.part_disc