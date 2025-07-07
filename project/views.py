from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from decimal import *
from client.models import Client 
from .models import Project, ScopeOfWork, Device, Wire, Hardware, Software, License, Travel
from jobsite.models import Jobsite
from schedule.models import Event
from timecard.models import TimeCard
from todo.models import Task, TaskList
from django.db.models import Sum
import datetime
from datetime import date
from django.views import generic
#from .forms import WipForm
from django.http import HttpResponse, HttpResponseRedirect
#from .render import Render
from collections import Counter

from .forms import ProjectForm, ScopeOfWorkForm, DeviceForm, WireForm, HardwareForm, SoftwareForm, LicenseForm, TravelForm

def ProjectMain(request):
    """
    View function for home page of site.
    """
    template = 'project/base_project.html'
    # Generate counts of some of the main objects
    num_clients = Client.objects.all().count()
    num_jobs = Project.objects.all().count()
    # Open installs (status = 'o')
    num_jobs_open = Project.objects.filter(job_status__exact='o').count()

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        template,
        context={
            'num_clients':num_clients,
            'num_jobs':num_jobs,
            'num_jobs_open':num_jobs_open,
             },
    )

class ProjectListView(generic.ListView):
    model = Project
    context_object_name = 'project_list'   # your own name for the list as a template variable
    queryset = Project.objects.filter(job_name__icontains='').order_by('-job_num')
    template_name = 'project/project_list.html'  # Specify your own template name/location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ProjectListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

def ProjectDeView(request, job_num):
    template_name = 'project/project_detail.html'  # Specify your own template name/location
    context_object_name = 'project_list_detail'   # your own name for the list as a template variable
    
    project_detail = Project.objects.get(job_num=job_num) 
    scope_list = ScopeOfWork.objects.filter(project__job_num__exact=job_num).order_by('-priority')
    task_list = TaskList.objects.filter(scope__project__job_num__exact=job_num).order_by('priority')
    device_mate_list = Device.objects.filter(project__job_num__exact=job_num).order_by('device__dmfg')
    wire_mate_list = Wire.objects.filter(task__task_list__scope__project__job_num__exact=job_num).order_by('wire__wmfg')
    hardware_mate_list = Hardware.objects.filter(task__task_list__scope__project__job_num__exact=job_num).order_by('hardware__hmfg')
    software_mate_list = Software.objects.filter(task__task_list__scope__project__job_num__exact=job_num).order_by('software__smfg')
    license_mate_list = License.objects.filter(task__task_list__scope__project__job_num__exact=job_num).order_by('license__dmfg')
    travel_mate_list = Travel.objects.filter(task__task_list__scope__project__job_num__exact=job_num)
    scheduling_event_list = Event.objects.all().filter(project__job_num__exact=job_num).order_by('-start')
    tasks_for_time = Task.objects.all().filter(task_list__scope__project__job_num__exact=job_num)
    timecard_add = TimeCard.objects.all().filter(project__job_num__exact=job_num)

    devicelistCounted = []
    devicelistr = []
    for devi in device_mate_list:
        for x in range(devi.qty):
            devicelistCounted.append(devi.device)
        devicelistr = Counter(devicelistCounted)
    devicelist = dict(devicelistr)

    time_cost = 0
    allocated_time_total = 0
    for ttime in tasks_for_time:
        allocated_time_total += ttime.total_hours
        if ttime.position:
            pay = Decimal(ttime.position.hourly) * Decimal(project_detail.burden)
            event_pay = pay * Decimal(ttime.total_hours)
            time_cost += event_pay
        else:
            event_pay = 0

    event_pay = 0
    event_time = 0
    scheduled_cost = 0
    for eventer in scheduling_event_list:
        workers = eventer.artist.count()
        event_time += workers * eventer.hours
        for worker in eventer.artist.all():
            pay = Decimal(worker.hourly) * Decimal(project_detail.burden)
            event_pay = pay * Decimal(eventer.hours)
            scheduled_cost += event_pay
    
    used_cost = 0
    overall_hours = 0
    timecard_total = datetime.timedelta(0,0,0)
    for card in timecard_add:
        timecard_total += card.day_total
        days_to_hours = card.day_total.days * 24
        sec_to_hours = (card.day_total.seconds) / 3600
        overall_hours = days_to_hours + sec_to_hours
        payed = Decimal(card.worker.hourly) * Decimal(project_detail.burden)
        event_payed = payed * Decimal(overall_hours)
        used_cost += event_payed

    return render(
        request,
        template_name,
        context={
            'project_detail': project_detail,
            'scope_list':scope_list,
            'task_list':task_list,
            'devicelist':devicelist,
            'device_mate_list':device_mate_list,
            'wire_mate_list':wire_mate_list,
            'hardware_mate_list':hardware_mate_list,
            'software_mate_list':software_mate_list,
            'license_mate_list':license_mate_list,
            'travel_mate_list':travel_mate_list,
            'scheduling_event_list':scheduling_event_list,
            'event_time':event_time,
            'scheduled_cost':scheduled_cost,
            'allocated_time_total':allocated_time_total,
            'time_cost':time_cost,
            'overall_hours':overall_hours,
            'used_cost':used_cost
             }, 
    )

def ProjectCreateView(request, jobsi):
    model = Project
    jsite = Jobsite.objects.get(pk=jobsi) 
    client = jsite.job_client.id
    template = 'project/project_form.html'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)
        form.save()
        return HttpResponseRedirect('/project/list')
    else:
        form = ProjectForm(initial={"jobsite": jobsi})
    return render(
        request,
        template,
        context={
            'form':form, 
            'client':client           
        },
    )

class ProjectUpdate(UpdateView):
    model = Project
    fields = ['job_num', 
              'jobsite', 
              'job_name',
              'revision', 
              'install_overview', 
              'pricing_disclaim',
              'site_contact', 
              'date_requested', 
              'due_date', 
              'finished_date', 
              'paid_date',
              'job_status',
              'tax_status',
              'division_status',
              'type_status',
              'estimator',
              'projectmanager',
              'foremen',
              'lead',
              'artist',
              'burden',
              'markup',
              'estimated_cost',
              'contract_value']
    template_name_suffix = '_update_form'

class ProjectDelete(DeleteView):
    model = Project 
    success_url = reverse_lazy('project-list')

def project_detail_pdf(request, job_num): 
    project_detail = Project.objects.get(job_num=job_num) 
    template_name = 'project_detail_pdf.html'
    scope_list = ScopeOfWork.objects.filter(project__job_num__exact=job_num).order_by('-priority')
    task_list = TaskList.objects.filter(scope__project__job_num__exact=job_num).order_by('priority')
    device_mate_list = Device.objects.filter(task__task_list__scope__project__job_num__exact=job_num).order_by('device__dmfg')
    wire_mate_list = Wire.objects.filter(task__task_list__scope__project__job_num__exact=job_num).order_by('wire__wmfg')
    hardware_mate_list = Hardware.objects.filter(task__task_list__scope__project__job_num__exact=job_num).order_by('hardware__hmfg')
    software_mate_list = Software.objects.filter(task__task_list__scope__project__job_num__exact=job_num).order_by('software__smfg')
    license_mate_list = License.objects.filter(task__task_list__scope__project__job_num__exact=job_num).order_by('license__dmfg')
    travel_mate_list = Travel.objects.filter(task__task_list__scope__project__job_num__exact=job_num)
    scheduling_event_list = Event.objects.all().filter(project__job_num__exact=job_num).order_by('-start')
    tasks_for_time = Task.objects.all().filter(task_list__scope__project__job_num__exact=job_num)
    timecard_add = TimeCard.objects.all().filter(project__job_num__exact=job_num)
    
    devicelistCounted = []
    devicelistr = []
    for devi in device_mate_list:
        for x in range(devi.qty):
            devicelistCounted.append(devi.device)
        devicelistr = Counter(devicelistCounted)
    devicelist = dict(devicelistr)

    time_cost = 0
    allocated_time_total = 0
    for ttime in tasks_for_time:
        allocated_time_total += ttime.total_hours
        pay = Decimal(ttime.position.hourly) * Decimal(project_detail.burden)
        event_pay = pay * Decimal(ttime.total_hours)
        time_cost += event_pay

    device_add_total = 0
    for devi in device_mate_list:
        device_add_total += devi.total

    wire_add_total = 0
    for wir in wire_mate_list:
        wire_add_total += wir.total

    hardware_add_total = 0
    for hardwa in hardware_mate_list:
        hardware_add_total += hardwa.total
    
    software_add_total = 0
    for softwa in software_mate_list:
        software_add_total += softwa.total
    software_total = Decimal(software_add_total) * Decimal(project_detail.licmarkup)

    license_add_total = 0
    for licwa in license_mate_list:
        license_add_total += licwa.total
    license_total = Decimal(license_add_total) * Decimal(project_detail.licmarkup)

    travel_add_total = 0
    for travwa in travel_mate_list:
        travel_add_total += travwa.total
    time_cost += travel_add_total
    
    materi_total = Decimal(device_add_total + wire_add_total + hardware_add_total) * Decimal(project_detail.markup)
    if project_detail.tax_status == 'x':
        tax_on_materi = 0
    else:
        tax_on_materi = materi_total * Decimal(.081)
        
    quote_total = time_cost + materi_total + software_total + license_total + tax_on_materi

    return render(
        request,
        template_name,
        context={
            'project_detail': project_detail,
            'scope_list':scope_list,
            'task_list':task_list,
            'devicelist':devicelist,
            'device_mate_list':device_mate_list,
            'wire_mate_list':wire_mate_list,
            'hardware_mate_list':hardware_mate_list,
            'software_mate_list':software_mate_list,
            'license_mate_list':license_mate_list,
            'allocated_time_total':allocated_time_total,
            'time_cost':time_cost,
            'materi_total':materi_total,
            'tax_on_materi':tax_on_materi,
            'license_add_total':license_total,
            'quote_total':quote_total
             },
    )

""" def project_quote_view(request, job_num):   

    project_detail = Project.objects.get(job_num=job_num) 
    # Create the HttpResponse object with the appropriate PDF headers.
    filenam = job_num+project_detail.job_name
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s-project-quote.pdf' % str(filenam)
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    p.setFont("Helvetica", 11)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(70, 780, "Structured Cabling    |    Network Solutions    |    A/V Solutions    |    Physical Layers")
    p.drawString(10, 610, project_detail.job_name)
    p.drawString(26, 40, "4500 E. Speedway, Suite 50     |     Tucson, AZ 85712     |     Phone(520) 585-5959     |     ROC 311659")
    
    s_o_w = project_detail.scope_of_work
    text = "J2 Technology Solutions"
    x = 3.8*inch
    y = 7.2*inch
    p.drawString(x,y,text)
    p.drawString(x-80,y-80,s_o_w)

    p.drawString(x,y-10,text)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response """

def ScopeMain(request):
    """
    View function for home page of site.
    """
    template = 'base_scope.html'
    num_scope = ScopeOfWork.objects.all().count()
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        template,
        context={
            'num_scope':num_scope
             },
    )

def ScopeOfWorkDeView(request, id):
    template_name = 'scope/scope_detail.html' 
    context_object_name = 'scope_detail'
    scope_detail = ScopeOfWork.objects.get(id=id)
    other_scopes = ScopeOfWork.objects.all().filter(project__job_num=scope_detail.project.job_num)
    task_list = TaskList.objects.filter(scope_id=id).order_by('priority')
    project = scope_detail.project.pk
    device_mate_list = Device.objects.filter(task__task_list__scope__exact=scope_detail).order_by('device__dmfg')
    wire_mate_list = Wire.objects.filter(task__task_list__scope__exact=scope_detail).order_by('wire__wmfg')
    hardware_mate_list = Hardware.objects.filter(task__task_list__scope__exact=scope_detail).order_by('hardware__hmfg')
    software_mate_list = Software.objects.filter(task__task_list__scope__exact=scope_detail).order_by('software__smfg')
    license_mate_list = License.objects.filter(task__task_list__scope__exact=scope_detail).order_by('license__dmfg')

    return render(
        request,
        template_name,
        context={
            'scope_detail':scope_detail,
            'other_scopes':other_scopes,
            'task_list':task_list,
            'project':project,
            'device_mate_list':device_mate_list,
            'wire_mate_list':wire_mate_list,
            'hardware_mate_list':hardware_mate_list,
            'software_mate_list':software_mate_list,
            'license_mate_list':license_mate_list,
             }, 
    )

def ScopeOfWorkCreateView(request, proj):
    model = ScopeOfWork 
    psite = Project.objects.get(job_num=proj) 
    jobsite = psite.jobsite.id
    template = 'scope/scopeofwork_form.html'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ScopeOfWorkForm(request.POST)
        form.save()
        return HttpResponseRedirect('/project/detail/'+proj)
    else:
        form = ScopeOfWorkForm(initial={"project": psite.id})
    return render(
        request,
        template,
        context={
            'form':form, 
            'jobsite':jobsite
        },
    )

class ScopeOfWorkUpdate(UpdateView):
    model = ScopeOfWork
    fields = ['project',
              'area', 
              'system_type']
    template_name = 'scope/scopeofwork_update_form.html'

class ScopeOfWorkDelete(DeleteView):
    model = ScopeOfWork
    template_name = 'scope/scopeofwork_confirm_delete.html'
    success_url = reverse_lazy('project-list')

def ProjectDevice(request):
    """
    View function for home page of site.
    """
    template = 'base_device.html'
    num_device = Device.objects.all().count()
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        template,
        context={
            'num_device':num_device
             },
    )

def ProjectDeviceDeView(request, id):
    template_name = 'device/device_detail.html' 
    context_object_name = 'device_detail'
    device_detail = Device.objects.get(id=id)
    other_devices = Device.objects.all().filter(project__job_num=device_detail.project.job_num).order_by('device__dmfg')
    return render(
        request,
        template_name,
        context={
            'device_detail':device_detail,
            'other_devices':other_devices,
             }, 
    )

def ProjectDeviceCreateView(request, proj, tas):
    model = Device 
    psite = Project.objects.get(job_num=proj) 
    jobsite = psite.jobsite.id
    template = 'device/device_form.html'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DeviceForm(proj, request.POST)
        form.save()
        return HttpResponseRedirect('/project/detail/'+proj)
    else:
        form = DeviceForm(proj, initial={"project": psite.id, "task":tas})
    return render(
        request,
        template,
        context={
            'form':form, 
            'project':psite.job_num,
            'jobsite':jobsite,
            'psite':psite
        },
    )

class ProjectDeviceUpdate(UpdateView):
    model = Device
    fields = ['project',
              'task',  
              'device',
              'purchased_date',
              'onsite_date',
              'installed_date',
              'qty',
              'cost',
              'device_status' ]
    template_name = 'device/device_update_form.html'

class ProjectDeviceDelete(DeleteView):
    model = Device
    template_name = 'device/device_confirm_delete.html'
    success_url = reverse_lazy('project-list')
    
def ProjectWire(request):
    """
    View function for home page of site.
    """
    template = 'base_wire.html'
    num_wire = Wire.objects.all().count()
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        template,
        context={
            'num_wire':num_wire
             },
    )

def ProjectWireDeView(request, id):
    template_name = 'wire/wire_detail.html' 
    context_object_name = 'wire_detail'
    wire_detail = Wire.objects.get(id=id)
    other_wires = Wire.objects.all().filter(project__job_num=wire_detail.project.job_num).order_by('wire__wmfg')
    project = wire_detail.project.pk
    return render(
        request,
        template_name,
        context={
            'wire_detail':wire_detail,
            'other_wires':other_wires,
            'project':project,
             }, 
    )

def ProjectWireCreateView(request, proj, tas):
    model = Wire 
    psite = Project.objects.get(job_num=proj) 
    jobsite = psite.jobsite.id
    template = 'wire/wire_form.html'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WireForm(proj, request.POST)
        form.save()
        return HttpResponseRedirect('/project/detail/'+proj)
    else:
        form = WireForm(proj, initial={"project": psite.id, "task":tas})
    return render(
        request,
        template,
        context={
            'form':form, 
            'project':psite.job_num,
            'jobsite':jobsite,
            'psite':psite
        },
    )

class ProjectWireUpdate(UpdateView):
    model = Wire
    fields = ['project',
              'task',  
              'wire',
              'purchased_date',
              'onsite_date',
              'installed_date',
              'length',
              'cost_per_foot',
              'wire_status']
    template_name = 'wire/wire_update_form.html'

class ProjectWireDelete(DeleteView):
    model = Wire
    template_name = 'wire/wire_confirm_delete.html'
    success_url = reverse_lazy('project-list')
    
def ProjectHardware(request):
    """
    View function for home page of site.
    """
    template = 'base_hardware.html'
    num_hardware = Hardware.objects.all().count()
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        template,
        context={
            'num_hardware':num_hardware
             },
    )

def ProjectHardwareDeView(request, id):
    template_name = 'hardware/hardware_detail.html' 
    context_object_name = 'hardware_detail'
    hardware_detail = Hardware.objects.get(id=id)
    other_hardwares = Hardware.objects.all().filter(project__job_num=hardware_detail.project.job_num).order_by('hardware__hmfg')
    project = hardware_detail.project.pk
    return render(
        request,
        template_name,
        context={
            'hardware_detail':hardware_detail,
            'other_hardwares':other_hardwares,
            'project':project,
             }, 
    )

def ProjectHardwareCreateView(request, proj, tas):
    model = Hardware 
    psite = Project.objects.get(job_num=proj) 
    jobsite = psite.jobsite.id
    template = 'hardware/hardware_form.html'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HardwareForm(proj, request.POST)
        form.save()
        return HttpResponseRedirect('/project/detail/'+proj)
    else:
        form = HardwareForm(proj, initial={"project": psite.id, "task":tas})
    return render(
        request,
        template,
        context={
            'form':form, 
            'project':psite.job_num,
            'jobsite':jobsite,
            'psite':psite
        },
    )

class ProjectHardwareUpdate(UpdateView):
    model = Hardware
    fields = ['project',
              'task',  
              'hardware',
              'purchased_date',
              'onsite_date',
              'installed_date',
              'qty',
              'cost',
              'hardware_status']
    template_name = 'hardware/hardware_update_form.html'

class ProjectHardwareDelete(DeleteView):
    model = Hardware
    template_name = 'hardware/hardware_confirm_delete.html'
    success_url = reverse_lazy('project-list')

def ProjectSoftware(request):
    """
    View function for home page of site.
    """
    template = 'base_software.html'
    num_software = Software.objects.all().count()
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        template,
        context={
            'num_software':num_software
             },
    )

def ProjectSoftwareDeView(request, id):
    template_name = 'software/software_detail.html' 
    context_object_name = 'software_detail'
    software_detail = Software.objects.get(id=id)
    other_softwares = Software.objects.all().filter(project__job_num=software_detail.project.job_num).order_by('software__smfg')
    return render(
        request,
        template_name,
        context={
            'software_detail':software_detail,
            'other_softwares':other_softwares,
             }, 
    )

def ProjectSoftwareCreateView(request, proj, tas):
    model = Software 
    psite = Project.objects.get(job_num=proj) 
    jobsite = psite.jobsite.id
    template = 'software/software_form.html'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SoftwareForm(proj, request.POST)
        form.save()
        return HttpResponseRedirect('/project/detail/'+proj)
    else:
        form = SoftwareForm(proj, initial={"project": psite.id, "task":tas})
    return render(
        request,
        template,
        context={
            'form':form, 
            'project':psite.job_num,
            'jobsite':jobsite,
            'psite':psite
        },
    )

class ProjectSoftwareUpdate(UpdateView):
    model = Software
    fields = ['project',
              'task',  
              'software',
              'purchased_date',
              'onsite_date',
              'installed_date',
              'qty',
              'cost',
              'software_status' ]
    template_name = 'software/software_update_form.html'

class ProjectSoftwareDelete(DeleteView):
    model = Software
    template_name = 'software/software_confirm_delete.html'
    success_url = reverse_lazy('project-list')

def ProjectLicense(request):
    """
    View function for home page of site.
    """
    template = 'base_license.html'
    num_license = License.objects.all().count()
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        template,
        context={
            'num_license':num_license
             },
    )

def ProjectLicenseDeView(request, id):
    template_name = 'license/license_detail.html' 
    context_object_name = 'license_detail'
    license_detail = License.objects.get(id=id)
    other_licenses = License.objects.all().filter(project__job_num=license_detail.project.job_num).order_by('license__dmfg')
    return render(
        request,
        template_name,
        context={
            'license_detail':license_detail,
            'other_licenses':other_licenses,
             }, 
    )

def ProjectLicenseCreateView(request, proj, tas):
    model = License 
    psite = Project.objects.get(job_num=proj) 
    jobsite = psite.jobsite.id
    template = 'license/license_form.html'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LicenseForm(proj, request.POST)
        form.save()
        return HttpResponseRedirect('/project/detail/'+proj)
    else:
        form = LicenseForm(proj, initial={"project": psite.id, "task":tas})
    return render(
        request,
        template,
        context={
            'form':form, 
            'project':psite.job_num,
            'jobsite':jobsite,
            'psite':psite
        },
    )

class ProjectLicenseUpdate(UpdateView):
    model = License
    fields = ['project',
              'task',  
              'license',
              'purchased_date',
              'onsite_date',
              'installed_date',
              'qty',
              'cost',
              'license_status' ]
    template_name = 'license/license_update_form.html'

class ProjectLicenseDelete(DeleteView):
    model = License
    template_name = 'license/license_confirm_delete.html'
    success_url = reverse_lazy('project-list')

def ProjectTravel(request):
    """
    View function for home page of site.
    """
    template = 'base_travel.html'
    num_travel = Travel.objects.all().count()
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        template,
        context={
            'num_travel':num_travel
             },
    )

def ProjectTravelDeView(request, id):
    template_name = 'travel/travel_detail.html' 
    context_object_name = 'travel_detail'
    travel_detail = Travel.objects.get(id=id)
    other_travels = Travel.objects.all().filter(project__job_num=travel_detail.project.job_num)
    return render(
        request,
        template_name,
        context={
            'travel_detail':travel_detail,
            'other_travels':other_travels,
             }, 
    )

def ProjectTravelCreateView(request, proj, tas):
    model = Travel 
    psite = Project.objects.get(job_num=proj) 
    jobsite = psite.jobsite.id
    template = 'travel/travel_form.html'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TravelForm(proj, request.POST)
        form.save()
        return HttpResponseRedirect('/project/detail/'+proj)
    else:
        form = TravelForm(proj, initial={"project": psite.id, "task":tas})
    return render(
        request,
        template,
        context={
            'form':form, 
            'project':psite.job_num,
            'jobsite':jobsite,
            'psite':psite
        },
    )

class ProjectTravelUpdate(UpdateView):
    model = Travel
    fields = ['project',
              'task',  
              'travel_name',
              'hotel_name',
              'cost',
              'gas_estimate',
              'hotel_status',
              'purchased_date', ]
    template_name = 'travel/travel_update_form.html'

class ProjectTravelDelete(DeleteView):
    model = Travel
    template_name = 'travel/travel_confirm_delete.html'
    success_url = reverse_lazy('project-list')

