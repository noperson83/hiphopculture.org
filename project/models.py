from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from datetime import date
from jobsite.models import Jobsite
from todo.models import Task
from material.models import DeviceMaterial, WireMaterial, HardwareMaterial, SoftwareMaterial, LicenseMaterial
from django.contrib.auth.models import Group
from django.conf import settings

class Project(models.Model):
    """
    Model representing a specific job (i.e. that can start after the contract is signed).
    """
    job_num          = models.BigIntegerField(help_text='Job number')
    revision         = models.CharField(max_length=200, null=True, blank=True, help_text='Revision')
    jobsite          = models.ForeignKey(Jobsite, on_delete=models.SET_NULL, null=True, help_text='Job site')
    job_name         = models.CharField(max_length=200, default='Job Name', help_text='Name of job')
    install_overview = models.TextField(max_length=8000, null=True, blank=True, help_text='Enter the overview of the install')
    pricing_disclaim = models.TextField(max_length=8000, null=True, blank=True, help_text='Enter the price disclaimer of the install')
    site_contact     = models.TextField(max_length=200, null=True, blank=True, help_text='Who is the site contact for the install')
    date_requested   = models.DateField(null=True, blank=True, help_text='Start Date')
    due_date         = models.DateField(null=True, blank=True, help_text='Due Date')
    finished_date    = models.DateField(null=True, blank=True, help_text='Date of completion')
    profile_pic      = models.ImageField(upload_to='uploads/project/profile_pics/%Y/%m/%d/', null=True, blank=True, max_length=60, help_text='profilepic.jpg')
    estimator        = models.ForeignKey("munkz.ArtistProfile", on_delete=models.SET_NULL, blank=True, null=True, related_name='Estimator', help_text='Estimator')
    projectmanager   = models.ForeignKey("munkz.ArtistProfile", on_delete=models.SET_NULL, blank=True, null=True, related_name='ProjectManager', help_text='Project Manager')
    foremen          = models.ForeignKey("munkz.ArtistProfile", on_delete=models.SET_NULL, blank=True, null=True, related_name='Foremen', help_text='Foremen')
    lead             = models.ManyToManyField("munkz.ArtistProfile", blank=True, related_name='Lead', help_text='Select leads for this install')
    artist          = models.ManyToManyField("munkz.ArtistProfile", related_name='Artist', blank=True, help_text='Select artist for this install')
    burden           = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default='1.65', help_text='Burden Percentage')
    markup           = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default='1.15', help_text='Material Markup')
    licmarkup        = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default='1.15', help_text='Sofware and License Markup')
    estimated_cost   = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default='4000.', help_text='Estimated Cost')
    contract_value   = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default='4500.', help_text='Contract Value')
    paid_date        = models.DateField(null=True, blank=True, help_text='Date paid')
    lastmodification = models.DateTimeField(auto_now=True, null=True, blank=True, help_text='Last modified')
    PROJECT_STATUS = (
        ('p', 'Prospect'),
        ('q', 'Quoted'),
        ('o', 'Installing'),
        ('c', 'Complete'),
        ('s', 'Service'),
        ('t', 'T & M'),
        ('i', 'Invoiced'),
        ('m', 'Paid'),
        ('l', 'Lost/Cancelled')
    )
    job_status = models.CharField(max_length=1, choices=PROJECT_STATUS, blank=True, default='p', help_text='Install Status')
    TAX_STATUS = (
        ('p', 'P.Y. Tribal Tax'),
        ('o', 'T.O. Tribal Tax'),
        ('x', 'Tax exempt'),
        ('t', 'Taxable'),
        ('s', 'Sub contractor')
    )
    tax_status = models.CharField(max_length=1, choices=TAX_STATUS, blank=True, default='s', help_text='Tax Status')
    DIVISION_STATUS = (
        ('c', 'Communications'),
        ('s', 'Special Systems')
    )
    division_status = models.CharField(max_length=1, choices=DIVISION_STATUS, blank=True, help_text='Division Status')
    TYPE_STATUS = (
        ('c', 'Commercial'),
        ('r', 'Residential')
    )
    type_status = models.CharField(max_length=1, choices=TYPE_STATUS, blank=True, default='c', help_text='Type Status')

    class Meta:
        ordering = ["-job_num"]

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{0} - {1} ({2})'.format(self.job_num,self.job_name,self.jobsite.job_title)
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('project-detail', args=[str(self.job_num)])

class ScopeOfWork(models.Model):
    project          = models.ForeignKey('Project', on_delete=models.SET_NULL, blank=True, null=True, related_name='ScopesProj', help_text='Project')
    area             = models.CharField(max_length=200, help_text='Area in building')
    system_type      = models.CharField(max_length=200, default='Cabling / AV / CCTV / Access Control', help_text='System Type')
    priority         = models.PositiveIntegerField(default='9999', help_text='Priorty')
    dateofcreation   = models.DateTimeField(auto_now_add=True, null=True, help_text='Created at')
    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.area
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this install.
    brand          = models.CharField(max_length=30, default='Job Name', help_text='Brand')
    description    = models.CharField(max_length=200, default='Job Name', help_text='Description')
        """
        return reverse('scope-detail', args=[str(self.pk)])

class Device(models.Model):
    project        = models.ForeignKey('Project', on_delete=models.SET_NULL, blank=True, null=True, related_name='DevProj', help_text='Project')
    task           = models.ForeignKey(Task, on_delete=models.SET_NULL, blank=True, null=True, related_name="taskattached", related_query_name="taskattached", help_text='task')
    device         = models.ForeignKey(DeviceMaterial, on_delete=models.SET_NULL, blank=True, null=True, help_text='wDevice')
    onsite_date    = models.DateField(null=True, blank=True, help_text=u'onsite date')
    installed_date = models.DateField(null=True, blank=True, help_text=u'installed date')
    qty            = models.PositiveIntegerField(null=True, default='1', help_text='Quantity')
    cost           = models.DecimalField(max_digits=18, decimal_places=2,  default='1.00', help_text='Cost') 

    def ext_price(self):
        return self.qty * self.cost
    total = property(ext_price)

    D_STATUS = (
    ('q', 'Quoted'),
    ('p', 'Purchased'),
    ('o', 'Onsite'),
    ('i', 'Installed')
    )

    device_status    = models.CharField(max_length=1, choices=D_STATUS, blank=True, default='q', help_text='Device Status')
    purchased_date = models.DateField(null=True, blank=True, help_text=u'purchased date')
    dateofcreation   = models.DateTimeField(auto_now_add=True, null=True, help_text='Created at')
    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0} - for {1}'.format(self.device,self.task)
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this install.
        """
        return reverse('project-device-detail', args=[str(self.pk)])

class Wire(models.Model):
    project        = models.ForeignKey('Project', on_delete=models.SET_NULL, blank=True, null=True, related_name='WirProj', help_text='Project')
    task           = models.ForeignKey(Task, on_delete=models.SET_NULL, blank=True, null=True, related_name="wtaskattached", related_query_name="wtaskattached", help_text='task')
    wire           = models.ForeignKey(WireMaterial, on_delete=models.SET_NULL, blank=True, null=True, help_text='wMaterial')
    onsite_date    = models.DateField(null=True, blank=True, help_text=u'onsite date')
    installed_date = models.DateField(null=True, blank=True, help_text=u'installed date')
    length         = models.PositiveIntegerField(null=True, default='1000', help_text='Length')
    cost_per_foot  = models.DecimalField(max_digits=18, decimal_places=2, default='1.20', help_text='Per foot') 

    def wire_price(self):
        return self.length * self.cost_per_foot
    total = property(wire_price)

    W_STATUS = (
    ('q', 'Quoted'),
    ('p', 'Purchased'),
    ('o', 'Onsite'),
    ('i', 'Installed')
    )

    wire_status      = models.CharField(max_length=1, choices=W_STATUS, blank=True, default='q', help_text='Wire Status')
    purchased_date = models.DateField(null=True, blank=True, help_text=u'purchased date')
    dateofcreation   = models.DateTimeField(auto_now_add=True, null=True, help_text='Created at')
    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0} - for {1}'.format(self.wire,self.task)
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this install.
        """
        return reverse('project-wire-detail', args=[str(self.pk)])

class Hardware(models.Model):
    project        = models.ForeignKey('Project', on_delete=models.SET_NULL, blank=True, null=True, related_name='HarProj', help_text='Project')
    task           = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, related_name="htaskattached", related_query_name="htaskattached", help_text='task')
    hardware       = models.ForeignKey(HardwareMaterial, on_delete=models.SET_NULL, null=True, help_text='hardware')
    onsite_date    = models.DateField(null=True, blank=True, help_text=u'onsite date')
    installed_date = models.DateField(null=True, blank=True, help_text=u'installed date')

    qty = models.PositiveIntegerField(null=True, blank=True, help_text='Quantity')
    cost = models.DecimalField(max_digits=18, decimal_places=2,null=True, blank=True, help_text='Cost') 

    def ext_price(self):
        return self.qty * self.cost
    total = property(ext_price)

    H_STATUS = (
    ('q', 'Quoted'),
    ('p', 'Purchased'),
    ('o', 'Onsite'),
    ('i', 'Installed')
    )

    hardware_status  = models.CharField(max_length=1, choices=H_STATUS, blank=True, default='q', help_text='Wire Status')
    purchased_date = models.DateField(null=True, blank=True, help_text=u'purchased date')
    dateofcreation   = models.DateTimeField(auto_now_add=True, null=True, help_text='Created at')
    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0} - for {1}'.format(self.hardware,self.task)
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this install.
        """
        return reverse('project-hardware-detail', args=[str(self.pk)])

class Software(models.Model):
    project        = models.ForeignKey('Project', on_delete=models.SET_NULL, blank=True, null=True, related_name='SofProj', help_text='Project')
    task           = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, related_name="staskattached", related_query_name="staskattached", help_text='task')
    software       = models.ForeignKey(SoftwareMaterial, on_delete=models.SET_NULL, null=True, help_text='Software')
    onsite_date    = models.DateField(null=True, blank=True, help_text=u'onsite date')
    installed_date = models.DateField(null=True, blank=True, help_text=u'installed date')
    qty            = models.PositiveIntegerField(null=True, blank=True, help_text='Quantity')
    cost           = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, help_text='Cost') 

    def ext_price(self):
        return (self.qty * self.cost)
    total = property(ext_price)

    S_STATUS = (
    ('q', 'Quoted'),
    ('p', 'Purchased'),
    ('o', 'Onsite'),
    ('i', 'Installed')
    )

    software_status  = models.CharField(max_length=1, choices=S_STATUS, blank=True, default='q', help_text='Software Status')
    purchased_date = models.DateField(null=True, blank=True, help_text=u'purchased date')
    dateofcreation   = models.DateTimeField(auto_now_add=True, null=True, help_text='Created at')
    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0} - for {1}'.format(self.software,self.task)
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this install.
        """
        return reverse('project-software-detail', args=[str(self.pk)])

class License(models.Model):
    project        = models.ForeignKey('Project', on_delete=models.SET_NULL, blank=True, null=True, related_name='LicProj', help_text='Project')
    task           = models.ForeignKey(Task, on_delete=models.SET_NULL, blank=True, null=True, related_name="lictaskattached", related_query_name="lictaskattached", help_text='task')
    license        = models.ForeignKey(LicenseMaterial, on_delete=models.SET_NULL, blank=True, null=True, help_text='wlicense')
    onsite_date    = models.DateField(null=True, blank=True, help_text=u'onsite date')
    installed_date = models.DateField(null=True, blank=True, help_text=u'installed date')
    qty            = models.PositiveIntegerField(null=True, default='1', help_text='Quantity')
    cost           = models.DecimalField(max_digits=18, decimal_places=2,  default='1.00', help_text='Cost') 

    def ext_price(self):
        return self.qty * self.cost
    total = property(ext_price)

    D_STATUS = (
    ('q', 'Quoted'),
    ('p', 'Purchased'),
    ('o', 'Onsite'),
    ('i', 'Installed')
    )

    license_status   = models.CharField(max_length=1, choices=D_STATUS, blank=True, default='q', help_text='license Status')
    purchased_date = models.DateField(null=True, blank=True, help_text=u'purchased date')
    dateofcreation   = models.DateTimeField(auto_now_add=True, null=True, help_text='Created at')
    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0} - for {1}'.format(self.license,self.task)
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this install.
        """
        return reverse('project-license-detail', args=[str(self.pk)])

class Travel(models.Model):
    project        = models.ForeignKey('Project', on_delete=models.SET_NULL, blank=True, null=True, related_name='TravelProj', help_text='Project')
    task           = models.ForeignKey(Task, on_delete=models.SET_NULL, blank=True, null=True, related_name="Traveltaskattached", related_query_name="traveltaskattached", help_text='task')
    travel_name    = models.CharField(max_length=200, null=True, blank=True, help_text='Travel Name')
    hotel_name     = models.CharField(max_length=200, null=True, blank=True, help_text='Hotel/Motel Name')
    cost           = models.DecimalField(max_digits=18, decimal_places=2, default='0.00', help_text='Cost') 
    gas_estimate   = models.DecimalField(max_digits=18, decimal_places=2, default='60.00', help_text='Cost')
    
    def ext_price(self):
        return self.gas_estimate + self.cost
    total = property(ext_price)

    T_STATUS = (
    ('q', 'Quoted'),
    ('p', 'Purchased')
    )

    hotel_status     = models.CharField(max_length=1, choices=T_STATUS, blank=True, default='q', help_text='travel Status')
    purchased_date   = models.DateField(null=True, blank=True, help_text=u'purchased date')
    dateofcreation   = models.DateTimeField(auto_now_add=True, null=True, help_text='Created at')
    lastmodification = models.DateTimeField(auto_now=True, null=True, help_text='Last modified')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0} - for {1}'.format(self.hotel_name,self.task)
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this install.
        """
        return reverse('project-travel-detail', args=[str(self.pk)])
