from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.client, name='client'),
    re_path(r'^list/(?P<firststr>[0-9a-zA-Z#])$', views.clientresults, name='client-results'),
    path('list/', views.ClientListView.as_view(), name='clients-list'),       
    re_path(r'^detail/(?P<id>\d+)$', views.ClientDeView, name='client-detail'),
    path('create-client/', views.ClientCreate.as_view(), name='create-client'),
    url(r'update-client/(?P<pk>[0-9]+)/$', views.ClientUpdate.as_view(), name='update-client'),
    url(r'client/(?P<pk>[0-9]+)/delete/$', views.ClientDelete.as_view(), name='delete-client')
]