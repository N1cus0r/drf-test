from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.db.models import Q
from .models import Doctor, Patient, Report
from .serializers import(
    DoctorSerializer, 
    PatientSerializer, 
    PatientDetailSerializer, 
    ReportSerializer,
    RegisterSerializer) 


class DoctorViewSet(ModelViewSet):
    queryset =  Doctor.objects.all()
    serializer_class = DoctorSerializer
    

class PatientListCreateView(ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return Patient.objects.prefetch_related('doctor').filter(doctor=self.kwargs.get('doctor_id'))

    def post(self, request, *args, **kwargs):
        serialized_data = PatientSerializer(data=request.data)  
        serialized_data.is_valid(raise_exception=True)

        object = Patient.objects.create(
            name=serialized_data.validated_data['name'],
            surname=serialized_data.validated_data['surname'],
            disease=serialized_data.validated_data['disease'] ,
        )
        object.doctor.set(self.kwargs.get('doctor_id'))
        serialized_object = PatientSerializer(object)

        return Response(serialized_object.data)


class PatientDetailReportCreateView(ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            patient = Patient.objects.prefetch_related('reports').get(
            Q(pk=self.kwargs.get('patient_id')) & 
            Q(doctor=self.kwargs.get('doctor_id')))
            reports = patient.reports.all()[:5]

        except:
            return Response({'error': 'Patient Not Found Or Belongs To Other Doctor'})    

        patient_sr = PatientDetailSerializer(patient)
        report_sr = ReportSerializer(reports, many=True)

        return Response({
            'patient':patient_sr.data,
            'reports':report_sr.data,
        })

    def post(self, request, *args, **kwargs):
        try:
            patient = Patient.objects.get(
            Q(pk=self.kwargs.get('patient_id')) & Q(doctor=self.kwargs.get('doctor_id'))
            )
        except:
            return Response({'error': 'Patient Not Found Or Belongs To Other Doctor'})    

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            report = Report.objects.create(
                content=serializer.validated_data['content'],
                patient=patient, 
            )
            report_serializer = ReportSerializer(report)
            return Response(report_serializer.data)
        else:
            return Response({'error': 'Invalid Data'})


class PatientRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_patient(self, request, *args, **kwargs):
        try:
            return Patient.objects.prefetch_related('doctor').get(
                Q(pk=self.kwargs.get('patient_id')) &
                Q(doctor=self.kwargs.get('doctor_id'))              
            )
        except:
            return None 

    def get(self, request, *args, **kwargs):
        patient = self.get_patient(request)

        if patient is None:
            return Response({'error': 'Patient Not Found Or Belongs To Other Doctor'})    

        serializer = PatientDetailSerializer(patient)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        patient = self.get_patient(request)    

        if patient is None:
            return Response({'error': 'Patient Not Found Or Belongs To Other Doctor'})  

        patient.delete()
        return Response({'success': 'Patient Deleted'})    

    def put(self, request, *args, **kwargs):
        patient = self.get_patient(request)    

        if patient is None:
            return Response({'error': 'Patient Not Found Or Belongs To Other Doctor'})  

        data = request.data

        patient.name = data.get('name', patient.name)     
        patient.surname = data.get('surname', patient.surname)     
        patient.surname = data.get('surname', patient.surname)     
        patient.disease = data.get('disease', patient.disease) 
        patient.save()
        
        serializer = PatientDetailSerializer(patient)
        
        url_doc = self.kwargs.get('doctor_id')
        post_doc_list = data.get('doctor', None)

        if post_doc_list is not None:
            if url_doc not in post_doc_list.split():
                patient.doctor.remove(url_doc)
            for doc in post_doc_list.split():    
                patient.doctor.add(doc)    

        return Response(serializer.data)


class RegisterView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = User.objects.create_user(
            username = data.get('username'),
            email = data.get('email'),
            password = data.get('password'),
        ) 
        serialized_user = RegisterSerializer(user)
        return Response({'cerated': serialized_user.data})

        
