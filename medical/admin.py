from django.contrib import admin
from .models import Patient, Doctor, Appointment, MedicalRecord


# Change Header Name & Title
admin.site.site_header = 'Medical Center Admin Panel'
admin.site.site_title = 'Medical Center Admin Panel'


# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)



