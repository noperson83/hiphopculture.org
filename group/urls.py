from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.conf.urls import url

app_name = 'group'
urlpatterns = [
    path('', views.group, name='group'),
    path('grouplist/', views.GroupListView.as_view(), name='group-list'),  
    re_path(r'^group-detail/(?P<id>\d+)$', views.GroupDeView, name='group-detail'),
    path('create-group/', views.GroupCreate.as_view(), name='create-group'),
    url(r'update-group/(?P<pk>[0-9]+)/$', views.GroupUpdate.as_view(), name='update-group'),
    url(r'group/(?P<pk>[0-9]+)/delete/$', views.GroupDelete.as_view(), name='delete-group'),
    path('albums', views.album, name='album'),
    path('albumlist/', views.AlbumListView.as_view(), name='album-list'),  
    re_path(r'^album-detail/(?P<id>\d+)$', views.AlbumDeView, name='album-detail'),
    path('create-album/', views.AlbumCreate.as_view(), name='create-album'),
    url(r'update-album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='update-album'),
    url(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='delete-album')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)