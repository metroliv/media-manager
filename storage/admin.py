from django.contrib import admin
from django.utils.html import format_html
from .models import Album, MediaFile, Profile


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)
    list_filter = ('created_at',)


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('file_thumbnail', 'file_name', 'file_type', 'album', 'uploaded_at')
    search_fields = ('file_name', 'album__name', 'file_type')
    list_filter = ('file_type', 'uploaded_at')
    ordering = ('-uploaded_at',)

    def file_thumbnail(self, obj):
        if obj.file_type == 'image' and obj.file:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;"/>', obj.file.url)
        return "No Image"

    file_thumbnail.short_description = "Preview"

    def file_name(self, obj):
        return obj.file.name.split("/")[-1]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone', 'profile_image', 'created_at')
    search_fields = ('user__username', 'email', 'phone')
    list_filter = ('created_at',)

    def profile_image(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;"/>', obj.profile_picture.url)
        return "No Image"

    profile_image.short_description = "Profile Picture"
