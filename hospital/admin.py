import django
from django.contrib import admin
from .models import Doctor, Patient, Report


admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Report)
