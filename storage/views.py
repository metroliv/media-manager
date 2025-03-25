from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .models import Album, MediaFile, Profile
from .forms import MediaFileForm, ProfileForm
import json
import logging
from django.contrib import messages



# Configure logging
logger = logging.getLogger(__name__)

# Home view
def home(request):
    return render(request, 'storage/home.html')  # Ensure you have this template.

# Album list view
@login_required
def album_list(request):
    albums = Album.objects.all()
    return render(request, 'storage/album_list.html', {'albums': albums})

# Album detail view
@login_required
def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    media_files = album.media_files.all()
    return render(request, 'storage/album_detail.html', {'album': album, 'media_files': media_files})


def upload_media(request, album_id):
    album = get_object_or_404(Album, id=album_id)

    if request.method == "POST" and request.FILES.get("file"):
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            media_file = form.save(commit=False)
            media_file.album = album
            media_file.save()
            return JsonResponse({"success": "File uploaded successfully!"})
        else:
            return JsonResponse({"error": "Invalid file format or missing data."})

    return JsonResponse({"error": "Invalid request!"})

# Create a new album (JSON API)
@csrf_exempt
@login_required
def create_album(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            description = data.get("description")

            if not name or not description:
                return JsonResponse({"success": False, "error": "Both name and description are required."}, status=400)

            album = Album.objects.create(name=name, description=description)
            return JsonResponse({"success": True, "album_id": album.id})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format."}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

# User profile view
@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'storage/profile.html', {'profile': profile})

# Edit user profile
@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'storage/edit_profile.html', {'form': form})

# Change password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents logout after password change
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'storage/change_password.html', {'form': form})

# User login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')  # Redirect to home after login
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

# User logout
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
