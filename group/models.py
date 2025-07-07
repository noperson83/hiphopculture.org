from django.db import models
from django.urls import reverse #for the get_absolute_url return
import os

def upload_to_group_folder(instance, filename):
    """Return file path for uploads scoped to a group's folder.

    When called from the :class:`Group` model itself ``instance`` will be a
    ``Group`` object. In that case the group name is stored directly on the
    instance. For related models (e.g. ``Album``) ``instance`` will have a
    ``group`` attribute pointing to the ``Group`` object.  Support both
    scenarios so the same function can be reused across models.
    """

    group_obj = getattr(instance, "group", None) or instance
    group_name = group_obj.group_name.replace(" ", "_").lower()
    folder_name = f"{group_name}/"
    return os.path.join(folder_name, filename)

def upload_to_group_folder_ac(instance, filename):
    # Normalize the group name to be used as a folder name
    group_name = instance.group.group_name.replace(' ', '_').lower()
    # Generate the folder path
    folder_name = f'{group_name}/album_covers/'
    # Return the full path to the file
    return os.path.join(folder_name, filename)

class Genre(models.Model):
    name = models.CharField(max_length=50, blank=True, help_text='Genre - "Hip-Hop"')
    description = models.TextField(max_length=100, blank=True, null=True, help_text='Description')

    def __str__(self):
        return self.name

class Group(models.Model):
    """
    Model representing a client.
    """
    group_name              = models.CharField(max_length=100, help_text='Group name')
    group_url               = models.CharField(max_length=100, blank=True, help_text='Web page')
    logo                    = models.ImageField(upload_to=upload_to_group_folder, null=True, blank=True, max_length=60, help_text='Logopic.jpg', default="home/images/LMNlogo.jpg")
    button                  = models.FileField(upload_to=upload_to_group_folder, null=True, blank=True, max_length=60, help_text='button.png', default="home/images/LMNlogo.jpg")
    background_image        = models.ImageField(
        upload_to=upload_to_group_folder,
        null=True,
        blank=True,
        max_length=60,
        help_text='Background image',
        default="home/images/LMNlogo.jpg",
    )
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
    facebook_url            = models.URLField(max_length=200, blank=True, help_text='Facebook page URL')
    instagram_url           = models.URLField(max_length=200, blank=True, help_text='Instagram page URL')
    twitter_url             = models.URLField(max_length=200, blank=True, help_text='Twitter handle URL')
    youtube_url             = models.URLField(max_length=200, blank=True, help_text='YouTube channel URL')
    spotify_url             = models.URLField(max_length=200, blank=True, help_text='Spotify profile URL')
    apple_music_url         = models.URLField(max_length=200, blank=True, help_text='Apple Music profile URL')
    soundcloud_url          = models.URLField(max_length=200, blank=True, help_text='SoundCloud profile URL')
    bandcamp_url            = models.URLField(max_length=200, blank=True, help_text='Bandcamp profile URL')
    tidal_url               = models.URLField(max_length=200, blank=True, help_text='Tidal profile URL')
    shazam_url              = models.URLField(max_length=200, blank=True, help_text='Shazam profile URL')
    tiktok_url              = models.URLField(max_length=200, blank=True, help_text='TikTok profile URL')

    class Meta:
        ordering = ["group_name"]
        verbose_name_plural = "Group Info"
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.group_name

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this install.
        """
        return reverse('group-detail', args=[str(self.id)])
    
class Album(models.Model):
    title = models.CharField(max_length=200)
    group  = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, help_text='Group')
    release_date = models.DateField()
    genre = models.ManyToManyField('Genre', related_name='albums')
    cover_art = models.ImageField(upload_to=upload_to_group_folder_ac, blank=True, null=True, default="home/images/LMNlogo.jpg")
    description = models.TextField(blank=True, null=True)
    record_label = models.CharField(max_length=100, blank=True, null=True)
    total_tracks = models.PositiveIntegerField()
    duration = models.DurationField(help_text="Duration in HH:MM:SS")
    spotify_link = models.URLField(blank=True, null=True)
    apple_music_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this install.
        """
        return reverse('album-detail', args=[str(self.pk)])
