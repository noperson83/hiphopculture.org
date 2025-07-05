from django.shortcuts import render
from django.template import RequestContext
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Client
from jobsite.models import Jobsite

def client(request):
    """
    View function for home page of site.
    """
    template = 'base_client.html'
    num_clients = Client.objects.all().count()
    client_list_num = '#'
    client_list_a = 'A'
    client_list_b = 'B'
    client_list_c = 'C'
    client_list_d = 'D'
    client_list_e = 'E'
    client_list_f = 'F'
    client_list_g = 'G'
    client_list_h = 'H'
    client_list_i = 'I'
    client_list_j = 'J'
    client_list_k = 'K'
    client_list_l = 'L'
    client_list_m = 'M'
    client_list_n = 'N'
    client_list_o = 'O'
    client_list_p = 'P'
    client_list_q = 'Q'
    client_list_r = 'R'
    client_list_s = 'S'
    client_list_t = 'T'
    client_list_u = 'U'
    client_list_v = 'V'
    client_list_w = 'W'
    client_list_x = 'X'
    client_list_y = 'Y'
    client_list_z = 'Z'

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        template,
        context={
            'client_list_num':client_list_num,
            'client_list_a':client_list_a,
            'client_list_b':client_list_b,
            'client_list_c':client_list_c,
            'client_list_d':client_list_d,
            'client_list_e':client_list_e,
            'client_list_f':client_list_f,
            'client_list_g':client_list_g,
            'client_list_h':client_list_h,
            'client_list_i':client_list_i,
            'client_list_j':client_list_j,
            'client_list_k':client_list_k,
            'client_list_l':client_list_l,
            'client_list_m':client_list_m,
            'client_list_n':client_list_n,
            'client_list_o':client_list_o,
            'client_list_p':client_list_p,
            'client_list_q':client_list_q,
            'client_list_r':client_list_r,
            'client_list_s':client_list_s,
            'client_list_t':client_list_t,
            'client_list_u':client_list_u,
            'client_list_v':client_list_v,
            'client_list_w':client_list_w,
            'client_list_x':client_list_x,
            'client_list_y':client_list_y,
            'client_list_z':client_list_z,
            'num_clients':num_clients
             },
    )

def clientresults(request, firststr):
    template_name = 'client_list.html'  # Specify your own template name/location
    queryset = Client.objects.filter(company_name__istartswith=firststr) 
    client_list = queryset
    
    return render(
        request,
        template_name,
        context={
            'client_list':client_list,
            'firststr':firststr,
             },
    )
    
class ClientListView(generic.ListView):
    template_name = 'client_list.html'  
    model = Client
    context_object_name = 'client_list'   
    queryset = Client.objects.filter(company_name__icontains='')

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

def ClientDeView(request, id):
    template_name = 'client_detail.html'
    context_object_name = 'jobsite_list_detail'
    client_detail = Client.objects.get(id=id) 
    client_job_list = Jobsite.objects.all().filter(job_client__company_name__contains=client_detail.company_name)
    
    return render(
        request,
        template_name,
        context={
            'client_detail':client_detail,
            'client_job_list':client_job_list
             }, 
    )

class ClientCreate(CreateView):
    model = Client
    fields = ['company_name',
              'company_url',
              'logo',
              'first_name', 
              'last_name',
              'contact_email',
              'contact_phone',
              'billing_top_address', 
              'billing_address', 
              'billing_address_city', 
              'billing_address_state', 
              'billing_address_zipcode', 
              'summary', 
              'date_of_contact', 
              'date_of_contract']

class ClientUpdate(UpdateView):
    model = Client
    fields = ['company_name',
              'company_url',
              'logo',
              'first_name', 
              'last_name',
              'contact_email',
              'contact_phone',
              'billing_top_address', 
              'billing_address', 
              'billing_address_city', 
              'billing_address_state', 
              'billing_address_zipcode', 
              'summary', 
              'date_of_contact', 
              'date_of_contract']
    template_name_suffix = '_update_form'

class ClientDelete(DeleteView):
    model = Client
    success_url = reverse_lazy('clients-list')