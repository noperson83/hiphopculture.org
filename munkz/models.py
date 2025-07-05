from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from group.models import Group
from schedule.models import Calendar, Event
import os

def upload_to_profile_folder(instance, filename):
    # Normalize the group name to be used as a folder name
    display_name = instance.display_name().replace(" ", "_").lower() if instance.display_name() else "unknown"
    group_name = instance.group.group_name.replace(' ', '_').lower() if instance.group else "solo"
    # Generate the folder path
    folder_name = f'{group_name}/{display_name}/profile_pics/'
    # Return the full path to the file
    return os.path.join(folder_name, filename)

def upload_to_cover_photos(instance, filename):
    # Normalize the group name to be used as a folder name
    display_name = instance.display_name().replace(" ", "_").lower() if instance.display_name() else "unknown"
    group_name = instance.group.group_name.replace(' ', '_').lower() if instance.group else "solo"
    # Generate the folder path
    folder_name = f'{group_name}/{display_name}/cover_photos/'
    # Return the full path to the file
    return os.path.join(folder_name, filename)

class ArtistManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Artists must have an email address')
        artist = self.model(email=self.normalize_email(email))
        artist.set_password(password)
        artist.save(using=self._db)
        return artist

    def create_superuser(self, email, password):
        artist = self.create_user(email, password=password)
        artist.is_staff = True
        artist.is_admin = True
        artist.save(using=self._db)
        return artist

class ArtistProfile(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    stage_name = models.CharField(max_length=100, blank=True, null=True, help_text='Artist or stage name')
    first_name = models.CharField(max_length=100, blank=True, null=True, help_text='Artist first name')
    last_name = models.CharField(max_length=100, blank=True, null=True, help_text='Artist last name')
    bio = models.TextField(blank=True, help_text='Artist biography')
    profile_pic = models.ImageField(upload_to=upload_to_profile_folder, null=True, blank=True, help_text='Profile picture')
    cover_photo = models.ImageField(upload_to=upload_to_cover_photos, null=True, blank=True, help_text='Cover photo')
    website = models.URLField(blank=True, null=True, help_text='Artist website')
    phone_number = models.CharField(max_length=17, null=True, blank=True, help_text='Contact phone number')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, help_text='Associated group')
    facebook_url = models.URLField(max_length=200, blank=True, help_text='Facebook page URL')
    instagram_url = models.URLField(max_length=200, blank=True, help_text='Instagram page URL')
    twitter_url = models.URLField(max_length=200, blank=True, help_text='Twitter handle URL')
    youtube_url = models.URLField(max_length=200, blank=True, help_text='YouTube channel URL')
    spotify_url = models.URLField(max_length=200, blank=True, help_text='Spotify artist profile')

    # Time Tracking
    total_hours_logged = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Total hours logged on projects')
    last_clock_in = models.DateTimeField(null=True, blank=True, help_text='Last clock-in time')
    last_clock_out = models.DateTimeField(null=True, blank=True, help_text='Last clock-out time')

    # Calendar & Organization
    has_calendar_access = models.BooleanField(default=False, help_text='Can the artist access the calendar?')
    has_task_management = models.BooleanField(default=False, help_text='Can the artist manage tasks?')

    # Permissions
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Connect to the schedule app
    calendar = models.OneToOneField(Calendar, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Events
    events = models.ManyToManyField(Event, blank=True, related_name="artist_events")
    show_public_events = models.BooleanField(default=True, help_text="Show events on public profile")

    objects = ArtistManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['first_name']

    def get_calendar_name(self):
        """Returns the calendar name for the artist."""
        return self.calendar.slug if self.calendar else "default"

    def public_events(self):
        """Returns only public events for display."""
        return self.events.filter(visibility="public")

    def private_events(self):
        """Returns private events for the artist only."""
        return self.events.filter(visibility="private")

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.email

    def get_absolute_url(self):
        return reverse('munkz:artist-detail', args=[str(self.id)])

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.email

    def get_short_name(self):
        return self.first_name if self.first_name else self.email

    def clock_in(self, timestamp):
        self.last_clock_in = timestamp
        self.save()

    def clock_out(self, timestamp):
        if self.last_clock_in:
            time_logged = timestamp - self.last_clock_in
            self.total_hours_logged += time_logged.total_seconds() / 3600  # Convert seconds to hours
            self.last_clock_out = timestamp
            self.save()
        else:
            raise ValueError("Artist must clock in first.") 

    def has_perm(self, perm, obj=None):
        """Return True if the user has the specified permission."""
        return self.is_admin

    def has_module_perms(self, app_label):
        """Return True if the user has permissions to view the app `app_label`."""
        return self.is_admin
    
    def display_name(self):
        """Return the artist's preferred name (Stage Name > First/Last Name)."""
        return self.stage_name if self.stage_name else f"{self.first_name}{self.last_name}"
