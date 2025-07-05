from django.contrib import admin

from .models import AudioFile, Video

class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'genre', 'group_album', 'track_number', 'munk', 'up_date')
    
    fieldsets = [
        (None,               {'fields': ['title', 'artist', 'album', 'genre', 'group_album', 'track_number', 'munk', 'contact_email', 'up_date']}),
        ('file',             {'fields': ['audio_file', 'album_art']}),
        ('information',      {'fields': ['year', 'comment', 'composer', 'lyrics', 'album_artist', 
                                         'disc_number', 'publisher', 'original_artist', 'encoded_by', 
                                         'discript', 'rms_list', 'rms_bass', 'rms_mid', 'rms_treble', 'heard','likes', 'nots', 'dls'], 'classes': ['collapse']}),
    ]

    search_fields = ['title', 'group_album', 'track_number']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_type', 'published_date')

admin.site.register(AudioFile, AudioFileAdmin)