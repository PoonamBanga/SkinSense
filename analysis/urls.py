from django.urls import path
from .views import ScanUploadView, ScanHistoryView

urlpatterns = [
    path('scan/', ScanUploadView.as_view(), name= 'scan_upload'),
    path('scans/', ScanHistoryView.as_view(), name = 'scan_history'),
]