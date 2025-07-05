# music/forms.py

from django import forms
from .models import AudioFile

class MP3UploadForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['title', 'artist', 'album', 'group_album', 'track_number', 'munk', 'up_date', 'genre', 'year', 'audio_file', ]

    audio_file = forms.FileField(label="Upload MP3", required=True)

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['title', 'artist', 'album', 'year', 'track_number', 
                  'comment', 'composer', 'lyrics', 'album_artist', 'disc_number', 'publisher', 
                  'original_artist', 'encoded_by', 'album_art', 'discript', 'rms_list', 
                  'rms_bass', 'rms_mid', 'rms_treble', 'heard', 'likes', 'nots', 'dls']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)



