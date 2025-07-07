"""labmunkznetwork URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.conf.urls import url

admin.site.site_header = "Labmunkz Network"
admin.site.index_title = "Database administration configuration."

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    #path('api/', include('api.urls')),
    path('group/', include('group.urls')),
    path('munkz/', include('munkz.urls')),
    path("music/", include("music.urls")),
    path("polls/", include("polls.urls")),
    path('shop/', include('shop.urls')),
   # path('asset/', include('asset.urls')),
    path('client/', include('client.urls')),
   # url(r'^filer/', include('filer.urls')),
   # path('helpdesk/', include('helpdesk.urls')),
    path('jobsite/', include('jobsite.urls')),
    path('project/', include('project.urls')),
    path('material/', include('material.urls')),
    path('posts/', include('posts.urls')),
    path('schedule/', include('schedule.urls', namespace='schedule')),
    path('timecard/', include('timecard.urls')),
    path('todo/', include('todo.urls', namespace="todo")),
   # path('wip/', include('wip.urls')),
]
#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
