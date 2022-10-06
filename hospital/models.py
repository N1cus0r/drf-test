from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ' ' + self.surname


class Patient(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    disease = models.TextField()
    doctor = models.ManyToManyField(Doctor)

    def __str__(self):
        return self.name + ' ' + self.surname


class Report(models.Model):
    content = models.TextField(default=None)
    time_create = models.DateField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, related_name='reports', on_delete=models.CASCADE)

    def __str__(self):
        return self.time_update.strftime('%d.%m | %H:%M') + f'\t{self.patient.name}\t{self.patient.surname}'
         