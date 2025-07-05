from django.db import models
from django.forms import ModelForm
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from datetime import date
from client.models import Client

class Jobsite(models.Model):
    """
    Model representing a Job site (but not a specific system install).
    """
    job_client       = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name="jobsites", related_query_name="jobsite", help_text='Client')
    job_title        = models.CharField(max_length=200, help_text='Name of Job Site')
    job_summary      = models.TextField(max_length=800, help_text='Enter a brief description of the Building or Orginization')
    profile_pic      = models.ImageField(upload_to='uploads/jobsite/profile_pics/%Y/%m/%d/', null=True, blank=True, max_length=60, help_text='profilepic.jpg')
    google_maps_link = models.CharField(max_length=200, null=True, blank=True, help_text='Google maps > click share > copy link > paste it here. https://goo.gl/maps/mqgVC9Ed4ik')
    latlng           = models.CharField(max_length=200, null=True, blank=True, help_text='Google maps > right click > where is > copy from right to left')
    signed_contract  = models.DateField(null=True, blank=True, help_text='Signed contract 5/22/2018 or 2018-05-22')
    top_address      = models.CharField(max_length=100, default='Attn: Mr Rogers', blank=True, help_text='Line 1 address')
    street_address   = models.CharField(max_length=100, default='1234 N Strong. Dr', blank=True, help_text='Line 2 Street address')
    city             = models.CharField(max_length=100, blank=True, help_text='City')
    state            = models.CharField(max_length=100, blank=True, help_text='State')
    zipcode          = models.CharField(max_length=100, blank=True, help_text='Zip code')

    class Meta:
        ordering = ["job_title"]
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.job_title

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('jobsite-detail', args=[str(self.id)])
