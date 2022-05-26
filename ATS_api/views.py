from django.shortcuts import render
from . models import UploadPdf, Job_discUpload
from . forms import ResumeUpload, Job_discUpload
import pandas as pd
import sys
import spacy
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
# Create your views here.
from rest_framework import viewsets

from ATS_api.serializers import UserSerializer, User_RoleSerializer,RoleSerializer,Skill_SetSerializer,job_platformsSerializer,CompanySerializer,applicant_cvSerializer,ExperianceSerializer,EducationSerializer,JobSerializer,job_categorySerializer,CandidateSerializer,applicant_DocumentSerializer,candidate_EvaluationSerializer,Job_Discription_DocumentSerializer
from ATS_api.models import User, User_Role,Role,Skill_Set, job_category,job_platforms,Company,applicant_cv,Experience,Education,Job,job_category,Candidate,Applicant_Document,candidate_Evaluation,Job_Description_Document


def upload_pdf(request):
    if request.method == "POST":
        form = ResumeUpload(request.POST, request.FILES)
        files = request.FILES.getlist('resumes')
        if form.is_valid():
            for f in files:
                file_instance = UploadPdf(resumes=f)
                file_instance.save()
        pec.main()
        return redirect('upload_resume')
    else:
        form = ResumeUpload()
    return render(request, '.html', {'form': form})

def upload_Job_disc(request):
    if request.method == "POST":
        form = Job_discUpload(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = Job_discUpload()
    data = pm.main()
    return render(request, '.html', index=False, render_links=True, escape=False)


class UserViewSet(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer


class User_RoleViewSet(viewsets.ModelViewSet):
   queryset = User_Role.objects.all()
   serializer_class = User_RoleSerializer

class RoleViewSet(viewsets.ModelViewSet):
   queryset = Role.objects.all()
   serializer_class = RoleSerializer

class Skill_SetViewSet(viewsets.ModelViewSet):
   queryset = Skill_Set.objects.all()
   serializer_class = Skill_SetSerializer
   
class job_platformsViewSet(viewsets.ModelViewSet):
   queryset = job_platforms.objects.all()
   serializer_class = job_platformsSerializer


class CompanyViewSet(viewsets.ModelViewSet):
   queryset = Company.objects.all()
   serializer_class = CompanySerializer
   
class applicant_cvViewSet(viewsets.ModelViewSet):
   queryset = applicant_cv.objects.all()
   serializer_class = applicant_cvSerializer


class ExperianceViewSet(viewsets.ModelViewSet):
   queryset = Experience.objects.all()
   serializer_class = ExperianceSerializer
   
class EducationViewSet(viewsets.ModelViewSet):
   queryset = Education.objects.all()
   serializer_class = EducationSerializer


class JobViewSet(viewsets.ModelViewSet):
   queryset = Job.objects.all()
   serializer_class = JobSerializer
   
class job_categoryViewSet(viewsets.ModelViewSet):
   queryset = job_category.objects.all()
   serializer_class = job_categorySerializer


class CandidateViewSet(viewsets.ModelViewSet):
   queryset = Candidate.objects.all()
   serializer_class = CandidateSerializer
   
class Applicant_DocuemntViewSet(viewsets.ModelViewSet):
   queryset = Applicant_Document.objects.all()
   serializer_class = applicant_DocumentSerializer

   
class candidate_EvaluationViewSet(viewsets.ModelViewSet):
   queryset = candidate_Evaluation.objects.all()
   serializer_class = candidate_EvaluationSerializer


class Job_Discription_DocumentViewSet(viewsets.ModelViewSet):
   queryset = Job_Description_Document.objects.all()
   serializer_class = Job_Discription_DocumentSerializer

