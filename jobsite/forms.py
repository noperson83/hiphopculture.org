from django import forms
from django.contrib.auth.models import User, Group 
from django.forms import ModelForm
from client.models import Client
from .models import Jobsite

class JobsiteForm(ModelForm):
    google_maps_link = forms.CharField(widget=forms.widgets.TextInput(), required=False)
    latlng           = forms.CharField(widget=forms.widgets.TextInput(), required=False)
    signed_contract  = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)
    top_address      = forms.CharField(widget=forms.widgets.TextInput(), required=False)
    street_address   = forms.CharField(widget=forms.widgets.TextInput(), required=False)
    city             = forms.CharField(widget=forms.widgets.TextInput(), required=False)
    state            = forms.CharField(widget=forms.widgets.TextInput(), required=False)
    zipcode          = forms.CharField(widget=forms.widgets.TextInput(), required=False)
    
    def __init__(self, *args, **kwargs):
        super(JobsiteForm, self).__init__(*args, **kwargs)
        self.fields["job_client"].widget. attrs = {
            "id": "id_job_client",
            "class": "custom-select mb-3",
            "name": "job_client",
        }
        self.fields["job_title"].widget.attrs = {
            "id": "id_job_title",
            "class": "form-control mb-3",
            "name": "job_title",
            "placeholder": "Enter a job title",
        }
        self.fields["job_summary"].widget.attrs = {
            "id": "id_job_summary",
            "class": "form-control mb-3",
            "name": "job_summary",
            "placeholder": "Enter a brief description of the Building or Orginization",
        }
    class Meta:
        model = Jobsite
        fields = ['job_title', 'job_client', 'job_summary', 'google_maps_link', 'latlng', 'signed_contract', 'top_address', 'street_address', 'city', 'state', 'zipcode']
        exclude = []
    
        