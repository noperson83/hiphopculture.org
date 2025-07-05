from django.db import models
from django.urls import reverse #for the get_absolute_url return

class SiteSettings(models.Model):
    promotion_message = models.CharField(max_length=255, default="Subscribe to Premium for ad-free music!")
    active_trend = models.CharField(max_length=255, default="Top track: 'Blinding Lights' by The Weeknd")
    
    def save(self, *args, **kwargs):
        if SiteSettings.objects.exists() and not self.pk:
            raise ValueError("You can only have one SiteSettings instance.")
        super().save(*args, **kwargs)

    def __str__(self):
        return "Site Settings"
    
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
