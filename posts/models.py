from django.db import models
from django.conf import settings
from polls.models import Question  # Assuming you already have a polls app

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_comments")
    text = models.TextField(max_length=2000, blank=True, help_text="Post text content (Max 2000 characters)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    youtube_url = models.URLField(blank=True, null=True, help_text="YouTube video URL")
    is_public = models.BooleanField(default=True, help_text="Public post or private")
    tags = models.ManyToManyField("Hashtag", blank=True, related_name="post_comments")

    # Relationships to media
    images = models.ManyToManyField("Image", blank=True, related_name="post_comments")
    video = models.ForeignKey("Video", on_delete=models.SET_NULL, blank=True, null=True)
    audio = models.ForeignKey("Audio", on_delete=models.SET_NULL, blank=True, null=True)
    poll = models.ForeignKey(Question, on_delete=models.SET_NULL, blank=True, null=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Post by {self.author.display_name()} on {self.created_at.strftime('%Y-%m-%d')}"

class Image(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/posts/images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Video(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.FileField(upload_to="uploads/posts/videos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Audio(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    audio = models.FileField(upload_to="uploads/posts/audio/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Share(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="shares")
    created_at = models.DateTimeField(auto_now_add=True)

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"#{self.name}"
    
class Timeline(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")  # Prevent duplicate entries
