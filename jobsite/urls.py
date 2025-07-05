from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.jobsite, name='jobsite'),
    path('list/', views.JobsiteListView.as_view(), name='jobsite-list'),
    re_path(r'^detail/(?P<pk>\d+)$', views.JobsiteDetailView.as_view(), name='jobsite-detail'),
    url(r'create-jobsite-from/(?P<client>[0-9]+)$', views.JobsiteCreateView, name='create-jobsite-from'),
    url(r'update-jobsite/(?P<pk>[0-9]+)/$', views.JobsiteUpdate.as_view(), name='update-jobsite'),
    url(r'jobsite/(?P<pk>[0-9]+)/delete/$', views.JobsiteDelete.as_view(), name='delete-jobsite'),

    path('app/', views.appListView, name='app-list'),
    
]