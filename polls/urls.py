from django.urls import path

from . import views
app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='polls'),
    path('questions/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('questions/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('questions/<int:question_id>/vote/', views.vote, name='vote'),
]

