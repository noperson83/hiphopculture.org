from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path(    '',                                  views.ProjectMain,               name='project'),
    path(    'list/',                             views.ProjectListView.as_view(), name='project-list'),
    url(    r'create-project/(?P<jobsi>[0-9]+)$', views.ProjectCreateView,         name='create-project-from'),
    url(    r'update-project/(?P<pk>[0-9]+)/$',   views.ProjectUpdate.as_view(),   name='update-project'),
    url(    r'main/(?P<pk>[0-9]+)/delete/$',      views.ProjectDelete.as_view(),   name='delete-project'),
    re_path(r'^detail/(?P<job_num>\d+)$',         views.ProjectDeView,             name='project-detail'),

    #re_path(r'^project-quote/(?P<job_num>\d+)$',  views.project_quote_view,        name='project-quote'),  
    re_path(r'^render/pdf/(?P<job_num>\d+)$',     views.project_detail_pdf,        name='project-pdf'),
    
    path(    'project-scope/',                 views.ScopeMain,                   name='scope-of-work'),
    url(    r'create-scope/(?P<proj>[0-9]+)$', views.ScopeOfWorkCreateView,       name='create-scope-of-work'),
    re_path(r'^scope/detail/(?P<id>\d+)$',     views.ScopeOfWorkDeView,           name='scope-detail'),
    url(    r'update-scope/(?P<pk>[0-9]+)/$',  views.ScopeOfWorkUpdate.as_view(), name='update-scope-of-work'),
    url(    r'scope/(?P<pk>[0-9]+)/delete/$',  views.ScopeOfWorkDelete.as_view(), name='delete-scope-of-work'),

    path(    'project-device/',                            views.ProjectDevice,                 name='project-device'),
    url(    r'create-device/(?P<proj>\d+)/(?P<tas>\d+)/$', views.ProjectDeviceCreateView,       name='create-project-device'),
    re_path(r'^device-detail/(?P<id>\d+)$',                views.ProjectDeviceDeView,           name='project-device-detail'),
    url(    r'update-device/(?P<pk>[0-9]+)/$',             views.ProjectDeviceUpdate.as_view(), name='update-project-device'),
    url(    r'device/(?P<pk>[0-9]+)/delete/$',             views.ProjectDeviceDelete.as_view(), name='delete-project-device'),

    path(    'project-wire/',                            views.ProjectWire,                 name='project-wire'),
    url(    r'create-wire/(?P<proj>\d+)/(?P<tas>\d+)/$', views.ProjectWireCreateView,       name='create-project-wire'),
    re_path(r'^wire-detail/(?P<id>\d+)$',                views.ProjectWireDeView,           name='project-wire-detail'),
    url(    r'update-wire/(?P<pk>[0-9]+)/$',             views.ProjectWireUpdate.as_view(), name='update-project-wire'),
    url(    r'wire/(?P<pk>[0-9]+)/delete/$',             views.ProjectWireDelete.as_view(), name='delete-project-wire'),

    path(    'project-hardware/',                            views.ProjectHardware,                 name='project-hardware'),
    url(    r'create-hardware/(?P<proj>\d+)/(?P<tas>\d+)/$', views.ProjectHardwareCreateView,       name='create-project-hardware'),
    re_path(r'^hardware-detail/(?P<id>\d+)$',                views.ProjectHardwareDeView,           name='project-hardware-detail'),
    url(    r'update-hardware/(?P<pk>[0-9]+)/$',             views.ProjectHardwareUpdate.as_view(), name='update-project-hardware'),
    url(    r'hardware/(?P<pk>[0-9]+)/delete/$',             views.ProjectHardwareDelete.as_view(), name='delete-project-hardware'),

    path(    'project-software/',                            views.ProjectSoftware,                 name='project-software'),
    url(    r'create-software/(?P<proj>\d+)/(?P<tas>\d+)/$', views.ProjectSoftwareCreateView,       name='create-project-software'),
    re_path(r'^software-detail/(?P<id>\d+)$',                views.ProjectSoftwareDeView,           name='project-software-detail'),
    url(    r'update-software/(?P<pk>[0-9]+)/$',             views.ProjectSoftwareUpdate.as_view(), name='update-project-software'),
    url(    r'software/(?P<pk>[0-9]+)/delete/$',             views.ProjectSoftwareDelete.as_view(), name='delete-project-software'),

    path(    'project-license/',                            views.ProjectLicense,                 name='project-license'),
    url(    r'create-license/(?P<proj>\d+)/(?P<tas>\d+)/$', views.ProjectLicenseCreateView,       name='create-project-license'),
    re_path(r'^license-detail/(?P<id>\d+)$',                views.ProjectLicenseDeView,           name='project-license-detail'),
    url(    r'update-license/(?P<pk>[0-9]+)/$',             views.ProjectLicenseUpdate.as_view(), name='update-project-license'),
    url(    r'license/(?P<pk>[0-9]+)/delete/$',             views.ProjectLicenseDelete.as_view(), name='delete-project-license'),

    path(    'project-travel/',                            views.ProjectTravel,                 name='project-travel'),
    url(    r'create-travel/(?P<proj>\d+)/(?P<tas>\d+)/$', views.ProjectTravelCreateView,       name='create-project-travel'),
    re_path(r'^travel-detail/(?P<id>\d+)$',                views.ProjectTravelDeView,           name='project-travel-detail'),
    url(    r'update-travel/(?P<pk>[0-9]+)/$',             views.ProjectTravelUpdate.as_view(), name='update-project-travel'),
    url(    r'travel/(?P<pk>[0-9]+)/delete/$',             views.ProjectTravelDelete.as_view(), name='delete-project-travel'),
]