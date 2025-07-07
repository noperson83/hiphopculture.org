from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy
from .models import Group, Album
from munkz.models import ArtistProfile
from music.models import AudioFile
# from django.utils import timezone for filtering events
from django.utils import timezone
from schedule.models import Calendar
#from client.models import Client

def group(request):
    """Display a list of all groups."""
    groups = Group.objects.all()

    return render(
        request,
        'group_list.html',
        context={'group_list': groups},
    )
    
def GroupDeView(request, id):
    template_name = 'group_detail.html'
    group_detail = Group.objects.get(id=id)
    group_album_list = Album.objects.all().filter(group__id=group_detail.pk)
    group_member_list = ArtistProfile.objects.all().filter(group__id=group_detail.pk)
    calendar = Calendar.objects.get_or_create_calendar_for_object(
        group_detail, name=f"{group_detail.group_name} Calendar"
    )
    upcoming_events = calendar.events.filter(start__gte=timezone.now()).order_by('start')
    old_events = calendar.events.filter(start__lt=timezone.now()).order_by('-start')

    return render(
        request,
        template_name,
        context={
            'group_detail':group_detail,
            'group_album_list':group_album_list,
            'group_member_list':group_member_list,
            'calendar': calendar,
            'upcoming_events': upcoming_events,
            'old_events': old_events,
             },
    )

class GroupListView(generic.ListView):
    model = Group
    queryset = Group.objects.filter(group_name__icontains='').order_by('-group_name')
    template_name = 'group_list.html'  # Specify your own template name/location
    paginate_by = 20

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(GroupListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class GroupCreate(CreateView):
    model = Group
    fields = ['group_name',
              'group_url',
              'logo',
              'button',
              'first_name',
              'last_name',
              'contact_email',
              'contact_phone',
              'youtube_url',
              'spotify_url',
              'apple_music_url',
              'soundcloud_url',
              'bandcamp_url',
              'tidal_url',
              'shazam_url',
              'tiktok_url',
              'billing_top_address',
              'billing_address',
              'billing_address_city',
              'billing_address_state',
              'billing_address_zipcode',
              'summary',
              'date_of_contact',
              'date_of_contract',
              'ytd_revenue',
              'total_revenue']

class GroupUpdate(UpdateView):
    model = Group
    fields = ['group_name',
              'group_url',
              'logo',
              'button',
              'first_name',
              'last_name',
              'contact_email',
              'contact_phone',
              'facebook_url',
              'instagram_url',
              'twitter_url',
              'youtube_url',
              'spotify_url',
              'apple_music_url',
              'soundcloud_url',
              'bandcamp_url',
              'tidal_url',
              'shazam_url',
              'tiktok_url',
              'billing_top_address',
              'billing_address',
              'billing_address_city',
              'billing_address_state',
              'billing_address_zipcode',
              'summary',
              'date_of_contact',
              'date_of_contract',
              'ytd_revenue',
              'total_revenue']
    
class GroupDelete(DeleteView):
    model = Group 
    success_url = reverse_lazy('group-list')

def album(request):
    """
    View function for home page of site.
    """
    template = 'album_list.html'
    album_list = Album.objects.all()

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        template,
        context={
            'album_list':album_list,
             },
    )
    
def AlbumDeView(request, id):
    template_name = 'album_detail.html'
    album_detail = Album.objects.get(id=id) 
    album_song_list = AudioFile.objects.all().filter(group_album__id=album_detail.pk).order_by('track_number')
    
    return render(
        request,
        template_name,
        context={
            'album_detail':album_detail,
            'album_song_list':album_song_list
             }, 
    )

class AlbumListView(generic.ListView):
    model = Album
    queryset = Album.objects.filter(title__icontains='').order_by('-release_date')
    template_name = 'album_list.html'  # Specify your own template name/location
    paginate_by = 20

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AlbumListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class AlbumCreate(CreateView):
    model = Album
    fields = ['title', 
              'group',
              'release_date',
              'genre',
              'cover_art',
              'description',
              'record_label',
              'total_tracks',
              'duration',
              'spotify_link',
              'apple_music_link']

class AlbumUpdate(UpdateView):
    model = Album
    fields = ['title', 
              'group',
              'release_date',
              'genre',
              'cover_art',
              'description',
              'record_label',
              'total_tracks',
              'duration',
              'spotify_link',
              'apple_music_link']
    
class AlbumDelete(DeleteView):
    model = Album 
    success_url = reverse_lazy('album-list')