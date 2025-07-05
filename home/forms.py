from django import forms
from .models import Subscriber

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']