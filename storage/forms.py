from django import forms
from .models import MediaFile
from .models import Profile 

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['album', 'file', 'file_type']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'profile_picture']
        

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['file']
