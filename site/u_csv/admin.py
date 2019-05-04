from django.contrib import admin
from .models import Document, GeneratedSchedules, UploadedCSV

# Register your models here.
admin.site.register(Document)
admin.site.register(GeneratedSchedules)
admin.site.register(UploadedCSV)