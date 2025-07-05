import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from group.models import Album, Group
import os

def upload_to_artist_folder(instance, filename):
    # Normalize the artist name to be used as a folder name
    artist_name = instance.group_album.group.group_name.replace(' ', '_').lower()
    # Generate the folder path
    folder_name = f'media/{artist_name}/'
    # Return the full path to the file
    return os.path.join(folder_name, filename)

def upload_to_artist_folder2(instance, filename):
    # Normalize the artist name to be used as a folder name
    artist_name = instance.group_album.group.group_name.replace(' ', '_').lower()
    # Generate the folder path
    folder_name = f'music/{artist_name}/'
    # Return the full path to the file
    return os.path.join(folder_name, filename)

def upload_to_artist_folder3(instance, filename):
    # Normalize the artist name to be used as a folder name
    artist_name = instance.group.group_name.replace(' ', '_').lower()
    # Generate the folder path
    folder_name = f'video/{artist_name}/'
    # Return the full path to the file
    return os.path.join(folder_name, filename)

class AudioFile(models.Model):
    #  user adds_ 
    title = models.CharField(max_length=255, default='Unknown Title', help_text='Song Title')
    artist = models.CharField(max_length=255, default='Unknown Artist', help_text='Song Artist')
    album = models.CharField(max_length=255, default='Unknown Album', help_text='Song Album')
    G_STATUS = (
        ('q', 'Unknown Genre'),('a', 'Hip-Hop'),('b', 'Rock'),('c', 'Pop'),('d', 'Jazz'),('e', 'Classical'),('f', 'Electronic'),    
        ('g', 'Country'),('h', 'Reggae'),('i', 'Blues'),('j', 'R&B/Soul'),('k', 'Metal'),('l', 'Folk'),('m', 'Rock'),('n', 'Punk'),('o', 'Funk'),
        ('p', 'Disco'),('r', 'Gospel'),('s', 'Ska'),('t', 'Latin'),('u', 'Alternative'),('v', 'K-Pop'))
    genre = models.CharField(max_length=1, choices=G_STATUS, blank=True, default='a', help_text='Song Genre')
    year = models.CharField(max_length=4, default='2000', help_text='Song Year')    
    track_number = models.CharField(max_length=255, default='Unknown Track Number', help_text='Song Track Number')
    comment = models.CharField(max_length=255, default='No Comment', help_text='Song Comment')
    composer = models.CharField(max_length=255, default='Unknown Composer', help_text='Song Composer')
    lyrics = models.CharField(max_length=4320, default='No Lyrics', help_text='Song Lyrics')
    album_artist = models.CharField(max_length=255, default='Unknown Album Artist', help_text='Song Album Artist')
    disc_number = models.CharField(max_length=255, default='Unknown Disc Number', help_text='Song Disc Number')
    publisher = models.CharField(max_length=255, default='Unknown Publisher', help_text='Song Publisher')
    original_artist = models.CharField(max_length=255, default='Unknown Original Artist', help_text='Song Original Artist')
    encoded_by = models.CharField(max_length=255, default='Unknown Encoder', help_text='Song Encoder')
    contact_email = models.EmailField(max_length=254, blank=True, help_text='Contact@email.com')
    album_art = models.ImageField(upload_to=upload_to_artist_folder, null=True, blank=True, max_length=60, help_text='albumcover.jpg')
    audio_file = models.FileField(upload_to=upload_to_artist_folder2, null=True, blank=True, max_length=180, help_text='TrackName.mp3') 
    rms_list = models.CharField(max_length=1200000, default='Unknown RMS', help_text='Song RMS')
    rms_bass = models.CharField(max_length=1200000, default='Unknown Bass RMS', help_text='Song Bass')
    rms_mid = models.CharField(max_length=1200000, default='Unknown Mids RMS', help_text='Song Mids')
    rms_treble = models.CharField(max_length=1200000, default='Unknown Treb', help_text='Song Treb')  
    discript = models.CharField(max_length=1200, default='Unknown User Discription', help_text='Song User Discription')
    up_date = models.DateTimeField('date published', default='03/11/2002')
    #  fan adds_    
    heard = models.BigIntegerField(default=1)
    likes = models.BigIntegerField(default=1)
    nots = models.BigIntegerField(default=1)
    dls = models.BigIntegerField(default=1)
    group_album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True, help_text='Album')
    munk = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="audiofile", related_query_name="audiofile", on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        return self.up_date >= timezone.now() - datetime.timedelta(days=1)
    
    @admin.display(
        boolean=True,
        ordering='up_date',
        description='Published recently?',)

    def get_absolute_url(self):
        
            """Returns the url to access a detail record for this install."""
            
            return reverse('audiofile', args=[str(self.pk)])

class Video(models.Model):
    VIDEO_TYPE_CHOICES = [
        ('youtube', 'YouTube'),
        ('uploaded', 'Uploaded'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, help_text='Group')
    video_type = models.CharField(max_length=10, choices=VIDEO_TYPE_CHOICES)
    youtube_url = models.URLField(blank=True, null=True)  # For YouTube videos
    video_file = models.FileField(upload_to=upload_to_artist_folder3, blank=True, null=True, max_length=180, help_text='TrackName.mp4')  # For uploaded videosmodels.FileField(upload_to=upload_to_artist_folder2, null=True, blank=True, max_length=180, help_text='TrackName.mp3')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
