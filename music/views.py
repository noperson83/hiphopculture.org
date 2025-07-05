
from .forms import ContactForm
from .models import AudioFile, Video
from group.models import Album
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from django.core.mail import send_mail
from django.contrib import messages
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TDRC, TRCK, COMM, TCOM, USLT, TPE2, TPUB, APIC

from .forms import MP3UploadForm, AudioFileForm
import librosa, os
import soundfile as sf
import numpy as np

def upload_mp3(request):
    """Handles MP3 file upload and analysis"""
    if request.method == 'POST':
        form = MP3UploadForm(request.POST, request.FILES)
        if form.is_valid():
            mp3_instance = form.save(commit=False)
            mp3_file = request.FILES['audio_file']

            # Check if file is an MP3
            if not mp3_file.name.lower().endswith('.mp3'):
                return render(request, 'music/upload.html', {
                    'form': form,
                    'error': "Invalid file type. Please upload an MP3 file."
                })

            try:
                # Load metadata
                audio = MP3(mp3_file, ID3=ID3)
                
                # Extract metadata, ensuring default values
                mp3_instance.title = audio.tags.get("TIT2", ["Unknown Title"])[0]
                mp3_instance.artist = audio.tags.get("TPE1", ["Unknown Artist"])[0]
                mp3_instance.album = audio.tags.get("TALB", ["Unknown Album"])[0]
                mp3_instance.munk = request.user
                mp3_instance.year = audio.tags.get("TYER", ["2000"])[0]

                # Extract cover art (if exists)
                if APIC in audio.tags:
                    cover_art = audio.tags[APIC].data
                    cover_filename = f"cover_{os.path.splitext(mp3_file.name)[0]}.jpg"
                    cover_path = os.path.join('media/covers', cover_filename)
                    with open(cover_path, 'wb') as f:
                        f.write(cover_art)
                    mp3_instance.cover_art = cover_path

                # Save MP3 instance
                mp3_instance.save()

                return redirect('music:analyze-mp3', mp3_id=mp3_instance.id)

            except Exception as e:
                return render(request, 'music/upload.html', {
                    'form': form,
                    'error': f"Error processing MP3 file: {e}"
                })

    else: 
        metadata = {
            "munk":  request.user,
        }
        form = MP3UploadForm(initial=metadata)

    return render(request, 'music/upload.html', {'form': form})

def analyze_mp3(request, mp3_id):
    audio_file = get_object_or_404(AudioFile, pk=mp3_id)

    if not audio_file.audio_file:
        return HttpResponse("No audio file associated with this entry.")

    file_path = audio_file.audio_file.path

    try:
        audio = MP3(file_path, ID3=ID3)

        metadata = {
            "title": str(audio.tags.get("TIT2", audio_file.title)),
            "artist": str(audio.tags.get("TPE1", audio_file.artist)),
            "album": str(audio.tags.get("TALB", audio_file.album)),
            "genre": str(audio.tags.get("TCON", audio_file.genre)),
            "year": str(audio.tags.get("TDRC", audio_file.year)),
            "track_number": str(audio.tags.get("TRCK", audio_file.track_number)),  # Ensure string format
            "comment": str(audio.tags.get("COMM::'eng'", audio_file.comment)),
            "composer": str(audio.tags.get("TCOM", audio_file.composer)),
            "lyrics": str(audio.tags.get("USLT::'eng'", audio_file.lyrics)),
            "album_artist": str(audio.tags.get("TPE2", audio_file.album_artist)),
            "publisher": str(audio.tags.get("TPUB", audio_file.publisher)),
        }

    except Exception as e:
        print("Error extracting metadata:", str(e))
        return HttpResponse(f"Error extracting metadata: {str(e)}")

    if request.method == "POST":
        form = AudioFileForm(request.POST, instance=audio_file)
        if form.is_valid():
            form.save()
            return redirect('music:music-detail', id=audio_file.pk)  # Ensure correct redirect

    else:
        form = AudioFileForm(initial=metadata)

    return render(request, "music/analyze.html", {"form": form, "audio_file": audio_file})
    
def estimate_key(y, sr):
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_sum = chroma.sum(axis=1)
    key_idx = chroma_sum.argmax()
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return keys[key_idx]

def analyze_audio(request, pk):
    # Get the audio file
    audio_file = AudioFile.objects.get(pk=pk)

    # Check if the file has already been analyzed
    if audio_file.analyzed:
        return render(request, 'analyze_result.html', {
            'audio_file': audio_file,
            'message': "This file has already been analyzed.",
        })

    # Load audio file
    file_path = audio_file.audio_file.path
    y, sr = librosa.load(file_path, sr=None)

    # Calculate BPM and Key
    bpm, _ = librosa.beat.beat_track(y=y, sr=sr)
    key = estimate_key(y, sr)

    # Calculate RMS
    with sf.SoundFile(file_path) as f:
        rms_list = []
        block_size = 512
        while True:
            block = f.read(block_size)
            if len(block) == 0:
                break
            rms_value = np.sqrt(np.mean(block**2))
            rms_list.append(rms_value)

    rms_normalized = (np.array(rms_list) / np.max(rms_list)).tolist()

    # Save analysis results to the database
    audio_file.bpm = bpm
    audio_file.key = key
    audio_file.rms_data = rms_normalized
    audio_file.duration = len(y) / sr  # Duration in seconds
    audio_file.analyzed = True
    audio_file.save()

    return render(request, 'analyze_result.html', {
        'audio_file': audio_file,
        'message': "Audio analysis completed successfully.",
    })

def MusicHomeView(request):
    template = 'music_home.html'
    music_list = AudioFile.objects.all().order_by("-artist", "group_album", "track_number").prefetch_related('munk') # Assuming you have a ForeignKey to an Artist model
    album_list = Album.objects.all().order_by('-release_date')

    return render(request, template, {'music_list':music_list, 'album_list': album_list})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = f"New message from {name}"
            full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            send_mail(subject, full_message, email, ['marcus@noperson.com'])

            messages.success(request, 'Email sent successfully!')
            return redirect('music:contact')
    else:
        form = ContactForm()
    return render(request, 'music/contact.html', {'form': form})

def MusicDeView(request, id):
    template_name = 'music_detail.html'
    music_detail = AudioFile.objects.get(id=id) 
    #client_job_list = Jobsite.objects.all().filter(job_client__company_name__contains=client_detail.company_name)
    
    return render(
        request,
        template_name,
        context={
            'music_detail':music_detail,
            #'client_list':client_list
             }, 
    )

def video_list(request):
    video_folder = os.path.join(settings.MEDIA_ROOT, 'videos')
    if os.path.exists(video_folder):
        videos = [
            'videos/' + f for f in os.listdir(video_folder)
            if f.lower().endswith(('.mp4', '.mov', '.webm', '.ogg'))
        ]
    else:
        videos = []
    ytvideos = Video.objects.all().order_by('-published_date')
    context = {'ytvideos': ytvideos, 'videos': videos}
    return render(request, 'videos.html', context)