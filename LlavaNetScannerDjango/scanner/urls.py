from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scan/', views.scan_new_directory, name='scan_directory'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('open-location/', views.open_location, name='open_location'),
    path('test-ollama/', views.test_ollama, name='test_ollama'),
] 