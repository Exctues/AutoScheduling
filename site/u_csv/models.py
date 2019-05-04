from django.contrib.auth.models import User
from django.db import models


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class UploadedCSV(models.Model):
    original_file_name = models.CharField(max_length=255, blank=False)
    file_location = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class GeneratedSchedules(models.Model):
    date_generated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    google_sheet = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255)
    used_csv_files = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="New")
