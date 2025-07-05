from django.contrib import admin
from .models import Post, Image, Video, Audio, Like, Comment, Share, Hashtag, Timeline

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "created_at", "is_public")
    list_filter = ("is_public", "created_at")
    search_fields = ("author__email", "text", "youtube_url")
    date_hierarchy = "created_at"
    filter_horizontal = ("tags", "images")

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("author", "uploaded_at")
    search_fields = ("author__email",)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("author", "uploaded_at")
    search_fields = ("author__email",)

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ("author", "uploaded_at")
    search_fields = ("author__email",)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    search_fields = ("user__email", "post__text")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    search_fields = ("user__email", "post__text", "text")

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    search_fields = ("user__email", "post__text")

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    search_fields = ("user__email", "post__text")
