from django import forms
from django.forms import ClearableFileInput
from .models import UploadPdf, Job_discUpload

class ResumeUpload(forms.ModelForm):
    class Meta:
        model = UploadPdf
        fields = ['resumes']
        widgets = {
            'resumes': ClearableFileInput(attrs={'multiple': True}),
        }
        
class Job_discUpload(forms.ModelForm):
    class Meta:
        model = Job_discUpload
        fields = ['Job_disc']
