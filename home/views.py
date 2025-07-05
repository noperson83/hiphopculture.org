from django.shortcuts import render, redirect
from munkz.models import ArtistProfile
from music.models import AudioFile

from django.contrib import messages
from .forms import SubscriberForm, ContactForm

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

from .models import Subscriber
from django.contrib.admin.views.decorators import staff_member_required
from .utils import send_mailing_list_email  # Import your utility function

from posts.models import Post

def index(request):
    template_name = 'index.html'

    posts = Post.objects.filter(is_public=True).order_by("-created_at")[:20]  # Fetch latest 20 posts
    artistprofile_detail = ArtistProfile.objects.filter(id=request.user.id)
    doll_hair = AudioFile.objects.filter(group_album=1).order_by('track_number')

    return render(
                request,
                template_name,
                context={
                'artistprofile_detail':artistprofile_detail,
                'doll_hair':doll_hair,
                "posts": posts,
                },
        )   

def subscribe(request):
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing!")
            return redirect('home:subscribe')
    else:
        form = SubscriberForm()
    return render(request, 'subscribe.html', {'form': form})

def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['labmunkzink@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')

@staff_member_required
def send_newsletter(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        send_mailing_list_email(subject, message)
        messages.success(request, "Newsletter sent successfully.")
        return redirect('send_newsletter')
    return render(request, 'send_newsletter.html')

def unsubscribe(request, email):
    try:
        subscriber = Subscriber.objects.get(email=email)
        subscriber.delete()
        messages.success(request, "You have been unsubscribed.")
    except Subscriber.DoesNotExist:
        messages.error(request, "Email not found.")
    return redirect('home:home')