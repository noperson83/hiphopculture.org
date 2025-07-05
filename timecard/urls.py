from django.urls import path
from django.conf.urls import url
from . import views
from .views import TimeCardWeekArchiveView
urlpatterns = [
    path('', views.index, name='timecard'),
    path('<int:year>/week/<int:week>/', TimeCardWeekArchiveView.as_view(), name="timecard_archive_week"),
    #path('upload-timecard/', views.impor, name='timecardup'),
    path('create-timecard/', views.TimeCardCreate.as_view(), name='create-timecard'),
    url(r'update-timecard/(?P<pk>[0-9]+)/$', views.TimeCardUpdate.as_view(), name='update-timecard'),
    url(r'(?P<pk>[0-9]+)/delete/$', views.TimeCardDelete.as_view(), name='delete-timecard')
]