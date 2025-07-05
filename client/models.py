from django.db import models
from django.urls import reverse #for the get_absolute_url return
#from filer.fields.image import FilerImageField

class Client(models.Model):
    """
    Model representing a client.
    """
    company_name            = models.CharField(max_length=100, help_text='Company name')
    company_url             = models.CharField(max_length=100, blank=True, help_text='Web page')
    logo                    = models.ImageField(upload_to='uploads/clientlogo/%Y/%m/%d/', null=True, blank=True, max_length=60, help_text='clientlogo.jpg')
    first_name              = models.CharField(max_length=100, help_text='Payment contact first name')
    last_name               = models.CharField(max_length=100, blank=True, help_text='Payment contact last name')
    contact_email           = models.EmailField(max_length=254, blank=True, help_text='Contact@email.com')
    contact_phone           = models.CharField(max_length=17, blank=True, help_text='Contact phone number')
    billing_top_address     = models.CharField(max_length=100, blank=True, help_text='Attn: John Doe')
    billing_address         = models.CharField(max_length=100, blank=True, help_text='Street addess')
    billing_address_city    = models.CharField(max_length=100, blank=True, help_text='City')
    billing_address_state   = models.CharField(max_length=100, blank=True, help_text='State')
    billing_address_zipcode = models.CharField(max_length=100, blank=True, help_text='Zip code')
    summary                 = models.TextField(max_length=1000, blank=True, help_text='Enter a brief description of the Building or Orginization')
    date_of_contact         = models.DateField(null=True, help_text='Date of contact 5/22/2018 or 2018-05-22')
    date_of_contract        = models.DateField(null=True, blank=True, help_text='Date of contract 5/22/2018 or 2018-05-22')
    ytd_revenue             = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, help_text='year to date revenue')
    total_revenue           = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, help_text='total revenue')
    
    class Meta:
        ordering = ["company_name"]
        verbose_name_plural = "Client Info"
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.company_name

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this install.
        """
        return reverse('client-detail', args=[str(self.id)])