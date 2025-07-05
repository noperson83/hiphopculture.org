from django.urls import path, re_path
from .views import (
    register_artist, artist_dashboard, artist_logout, edit_artist_profile, clock_in, clock_out, activate_account, artist_profile, 
    artist_edit, artist_calendar, artist_task_list, ArtistView, ArtistList, ArtistCreate, ArtistUpdate, ArtistDelete
)
from . import views
from django.views.generic import TemplateView

app_name = 'munkz'
urlpatterns = [
    path('', views.index, name='munkz'),
    path('signup/', register_artist, name='register_artist'),
    path("activate/<uidb64>/<token>/", activate_account, name="activate_account"),
    path('email-verification-sent/', TemplateView.as_view(template_name="registration/email_verification_sent.html"), name='email_verification_sent'),
    path('dashboard/', artist_dashboard, name='artist-dashboard'),
    path("profile/<int:pk>/", artist_profile, name="artist-profile"),  # Public Profile Page
    path("profile/edit/<int:pk>/", artist_edit, name="artist-edit"),  # Edit Profile Page
    path("logout/", artist_logout, name="artist-logout"),
    path('edit-profile/', edit_artist_profile, name='edit_artist_profile'),
    path('clock-in/', clock_in, name='clock_in'),
    path('clock-out/', clock_out, name='clock_out'),
    path('calendar/', artist_calendar, name='artist_calendar'), 
    path('tasks/', artist_task_list, name='artist_task_list'),
    re_path(r'^artist/(?P<id>\d+)$', views.ArtistProfileView, name='artist-detail'),

    # Class-based views
    path('<int:pk>/', ArtistView.as_view(), name='artist_detail'),
    path('', ArtistList.as_view(), name='artist_list'),
    path('create/', ArtistCreate.as_view(), name='artist_create'),
    path('<int:pk>/update/', ArtistUpdate.as_view(), name='artist_update'),
    path('<int:pk>/delete/', ArtistDelete.as_view(), name='artist_delete'),




]
