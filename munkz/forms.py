from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ArtistProfile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

class ArtistProfileForm(forms.ModelForm):
    class Meta:
        model = ArtistProfile
        fields = [
            "email", "first_name", "last_name", "bio", "profile_pic", "cover_photo", "website",
            "phone_number", "facebook_url", "instagram_url", "twitter_url", "youtube_url", "spotify_url",
            "group", "has_calendar_access", "has_task_management",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "cols": 40}),
            "website": forms.URLInput(attrs={"placeholder": "https://yourwebsite.com"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "+1 123-456-7890"}),
        }

class ArtistClockInForm(forms.Form):
    clock_in_time = forms.DateTimeField(widget=forms.HiddenInput())

class ArtistClockOutForm(forms.Form):
    clock_out_time = forms.DateTimeField(widget=forms.HiddenInput())

class ArtistChangeForm(UserChangeForm):
    class Meta:
        model = ArtistProfile
        fields = ["email", "first_name", "last_name", "bio", "profile_pic", "cover_photo", "website",
                  "phone_number", "facebook_url", "instagram_url", "twitter_url", "youtube_url", "spotify_url",
                  "group",]
      
class ArtistCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone_number = forms.CharField(max_length=17, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}), required=False)

    class Meta: 
        model = ArtistProfile
        fields = ["email", "first_name", "phone_number", "bio", "password1", "password2"]
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)  # Basic email format check
        except ValidationError:
            raise forms.ValidationError("Invalid email address format.")

        # Optional: Use regex for basic validation without MX lookup
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Please enter a valid email address.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = False  # ✅ Explicitly set to False
        user.is_staff = False
        if commit:
            user.save()
        return user
