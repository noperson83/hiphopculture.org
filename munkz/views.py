from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import ArtistProfile
from .forms import ArtistProfileForm, ArtistChangeForm, ArtistCreationForm, ArtistClockInForm, ArtistClockOutForm
from django.utils.timezone import now
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model, logout
from django.contrib import messages
from schedule.models import Event
from posts.models import Post

def upcoming_events(request):
    events = Event.objects.filter(start__gte=now()).order_by("start")[:5]
    return render(request, "schedule/upcoming_events.html", {"events": events})

def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link.")
        return redirect("signup")

def index(request):
    """
    View function for hr page of site.
    """
    template = 'base_hr.html'
    
    num_workers = ArtistProfile.objects.all().count()

    return render(
        request,
        template,
        context={
            'num_workers':num_workers
            },
    )

def register_artist(request):
    if request.method == "POST":
        form = ArtistCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Require email verification
            user.is_superuser = False  # FIX: Explicitly set to False
            user.is_staff = False  # Ensure this is set explicitly
            user.save()

            # Generate email verification link
            current_site = get_current_site(request)
            mail_subject = "Activate Your Artist Account - LabMunkz"
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = f"https://{current_site.domain}{reverse('munkz:activate_account', kwargs={'uidb64': uid, 'token': token})}"
            
            message = render_to_string("registration/activation_email.html", {
                "user": user,
                "verification_link": verification_link,
            })
            send_mail(mail_subject, message, "letsreaddad@gmail.com", [user.email])
            # Redirect to the "Check your email" page
            return redirect("munkz:email_verification_sent")
        else:
            messages.error(request, "There were errors in your submission. Please check below.")
    else:
        form = ArtistCreationForm()
    
    return render(request, "registration/register.html", {"form": form})

def artist_logout(request):
    logout(request)
    return render(request, "registration/logged_out.html")

@login_required
def artist_dashboard(request):
    artist = request.user
    return render(request, "dashboard.html", {"artist": artist})

@login_required
def edit_artist_profile(request):
    artist = request.user
    if request.method == "POST":
        form = ArtistChangeForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            return redirect("munkz:artist_dashboard")
    else:
        form = ArtistChangeForm(instance=artist)
    return render(request, "edit_profile.html", {"form": form})

@login_required
def artist_edit(request, pk):
    """
    View function for editing the artist's profile.
    """
    artist = get_object_or_404(ArtistProfile, pk=pk)

    # Ensure the logged-in user is editing their own profile
    if request.user != artist:
        return redirect("munkz:artist-detail", id=artist.pk)

    if request.method == "POST":
        form = ArtistProfileForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            return redirect("munkz:artist-detail", id=artist.pk)
    else:
        form = ArtistProfileForm(instance=artist)

    return render(request, "artist_edit.html", {"form": form, "artist": artist})

@login_required
def clock_in(request):
    artist = request.user
    if request.method == "POST":
        form = ArtistClockInForm(request.POST)
        if form.is_valid():
            artist.clock_in(now())
            return redirect("artist_dashboard")
    else:
        form = ArtistClockInForm()
    return render(request, "clock_in.html", {"form": form})


@login_required
def clock_out(request):
    artist = request.user
    if request.method == "POST":
        form = ArtistClockOutForm(request.POST)
        if form.is_valid():
            artist.clock_out(now())
            return redirect("artist_dashboard")
    else:
        form = ArtistClockOutForm()
    return render(request, "clock_out.html", {"form": form})


@login_required
def artist_calendar(request):
    artist = request.user
    events = artist.artistevent_set.all()
    return render(request, "artist_calendar.html", {"artist": artist, "events": events})


@login_required
def artist_task_list(request):
    artist = request.user
    tasks = artist.artisttask_set.all()
    return render(request, "artist_tasks.html", {"artist": artist, "tasks": tasks})

def artist_profile(request, pk):
    """
    View function for displaying the artist's public profile.
    """
    artist = get_object_or_404(ArtistProfile, pk=pk)
    return render(request, "artist_profile.html", {"artist": artist})

def ArtistProfileView(request, id):
    template_name = 'artist_detail.html'  # Specify your own template name/location
    artist_detail = ArtistProfile.objects.get(id=id)
    public_events = Event.objects.filter(start__gte=now()).order_by("start")[:5]
    posts = Post.objects.all().filter(author__id__contains=id)
    #worker_project_list = Project.objects.all().filter(workers__id__contains=id)
    #project_event_list = Event.objects.all().filter(workers__id__contains=id)
    
    #ladder_list = Ladder.objects.filter(worker__id__exact=id)
    #vehicle_list = Vehicle.objects.filter(worker__id__exact=id)
    #power_tool_list = Power_Tool.objects.filter(worker__id__exact=id)
    #tester_list = Tester.objects.filter(worker__id__exact=id)
    #fiber_list = Fiber_Equipment.objects.filter(worker__id__exact=id)
    #tool_list = Tool.objects.filter(worker__id__exact=id)

    return render(
        request,
        template_name,
        context={
            'artist': artist_detail,
            'public_events': public_events,
            'posts': posts
               #'project_event_list':project_event_list,
               # 'ladder_list':ladder_list,
               # 'vehicle_list':vehicle_list,
               # 'power_tool_list':power_tool_list,
               #'tester_list':tester_list,
               # 'fiber_list':fiber_list,
               # 'tool_list':tool_list
             }, 
    )

class ArtistView(DetailView):
    model = ArtistProfile
    template_name = "artist_detail.html"
    context_object_name = "artist"


class ArtistList(ListView):
    model = ArtistProfile
    template_name = "artist_list.html"
    context_object_name = "artists"
    ordering = ['first_name']


class ArtistCreate(CreateView):
    model = ArtistProfile
    form_class = ArtistProfileForm
    template_name = "artist_form.html"
    success_url = reverse_lazy("artist_dashboard")


class ArtistUpdate(UpdateView):
    model = ArtistProfile
    form_class = ArtistProfileForm
    template_name = "artist_form.html"
    success_url = reverse_lazy("artist_dashboard")


class ArtistDelete(DeleteView):
    model = ArtistProfile
    template_name = "artist_confirm_delete.html"
    success_url = reverse_lazy("artist_list")
