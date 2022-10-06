from rest_framework import serializers

from .models import Doctor, Patient, Report

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ['doctor']

    doctors = serializers.SerializerMethodField('get_doctor_names')

    def get_doctor_names(self, obj):
        return [f'{d.name} {d.surname}' for d in obj.doctor.all()] 


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude = ['patient']


class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()    
