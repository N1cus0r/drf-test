from unittest import registerResult
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import(
    DoctorViewSet, 
    PatientListCreateView, 
    PatientDetailReportCreateView,
    PatientRetrieveUpdateDestroyView,
    RegisterView,
) 

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('doctors/<str:doctor_id>/edit-patients/<str:patient_id>/', PatientRetrieveUpdateDestroyView.as_view()),
    path('doctors/<str:doctor_id>/patients/<str:patient_id>/', PatientDetailReportCreateView.as_view()),
    path('doctors/<str:doctor_id>/patients/', PatientListCreateView.as_view()),
    path('__debug__/', include('debug_toolbar.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('rest_framework.urls')),
    path('auth/register/', RegisterView.as_view())
]