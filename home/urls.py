from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import contactView, successView

app_name = 'home'
urlpatterns = [
    path('', views.index, name='home'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('contact/', contactView, name='contact'),
    path('success/', successView, name='success'),
    path('send-newsletter/', views.send_newsletter, name='send_newsletter'),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


