from django.shortcuts import redirect, render
#from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from client.models import Client 
from project.models import Project
from .models import Jobsite
from django.views import generic
from django.db.models import Sum
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .forms import JobsiteForm

def jobsite(request):
    """
    View function for home page of site.
    """
    template = 'base_jobsite.html'
    # Generate counts of some of the main objects
    num_clients = Client.objects.all().count()
    num_jobs = Jobsite.objects.all().count()
    num_project = Project.objects.all().count()
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        template,
        context={
            'num_clients':num_clients,
            'num_jobs':num_jobs,
            'num_project':num_project
             },
    )

class JobsiteListView(generic.ListView):
    model = Jobsite
    context_object_name = 'jobsite_list'   # your own name for the list as a template variable
    queryset = Jobsite.objects.order_by('-job_title')
    template_name = 'jobsite_list.html'
    paginate_by = 10

class JobsiteDetailView(generic.DetailView):
    model = Jobsite
    template_name = 'jobsite_detail.html'

def JobsiteCreateView(request, client):
    model = Jobsite
    template = 'jobsite/jobsite_form_from.html'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = JobsiteForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('client-detail', kwargs={"id": client}))
    else:
        form = JobsiteForm(initial={"job_client": client})
    return render(
        request,
        template,
        context={
            'form':form,            
        },
    )
    
class JobsiteUpdate(UpdateView):
    model = Jobsite
    fields = ['job_title', 'job_client', 'job_summary', 'google_maps_link', 'latlng', 'signed_contract', 'top_address', 'street_address', 'city', 'state', 'zipcode']
    template_name_suffix = '_update_form'

class JobsiteDelete(DeleteView):
    model = Jobsite
    success_url = reverse_lazy('jobsite-list')

def appListView(request):
    template_name = 'app_list.html' 
    return render(
        request,
        template_name
    )

