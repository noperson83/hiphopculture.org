from django.urls import path, re_path
from django.conf.urls.static import static
from . import views
from django.conf.urls import url
from django.conf import settings
from .views import upload_mp3, analyze_mp3

app_name = 'music'
urlpatterns = [
    path('', views.MusicHomeView, name='music'),
    re_path(r'^music-detail/(?P<id>\d+)$', views.MusicDeView, name='music-detail'),
    path('contact/', views.contact, name='contact'),
    path('videos/', views.video_list, name='video_list'),
    path('upload/', upload_mp3, name='upload-mp3'),
    path('analyze/<int:mp3_id>/', analyze_mp3, name='analyze-mp3'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

