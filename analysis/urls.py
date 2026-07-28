from django.urls import path
from .views import ScanUploadView

urlpatterns = [
    path('scan/', ScanUploadView.as_view(), name= 'scan_upload'),
]