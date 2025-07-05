from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta, datetime, date, time, tzinfo
from django.utils import timezone
from django.conf import settings
from munkz.models import ArtistProfile
from project.models import Project

class TimeCard(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False, help_text=u'Date')
    #worker = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="timecard", related_query_name="timecard", on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, help_text='Project')
    site_time = models.TimeField(null=True, help_text=u'Start time')
    site_end_time = models.TimeField(blank=True, null=True, help_text=u'Stop time')
    site_time_after = models.TimeField(blank=True, null=True, help_text=u'Start time after lunch')
    site_end_time_after = models.TimeField(null=True, help_text=u'Stop time after lunch')

    def reg(self):
        time = datetime.combine(date.today(), self.site_end_time) - datetime.combine(date.today(), self.site_time)
        time_after = datetime.combine(date.today(), self.site_end_time_after) - datetime.combine(date.today(), self.site_time_after)
        return time + time_after
    day_total = property(reg)
    
    @property
    def seconds(self):
        return (self.end - self.start).total_seconds()

    @property
    def minutes(self):
        return float(self.seconds) / 60

    @property
    def hours(self):
        return float(self.seconds) / 3600
    
    class Meta:
        ordering = ["date"]

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('timecard', args=[str(self.id)])
