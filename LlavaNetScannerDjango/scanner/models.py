from django.db import models
from datetime import datetime

class ScanResult(models.Model):
    """Model to store scan results for files"""
    # Basic file information
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=1024, unique=True)
    file_type = models.CharField(max_length=20)
    file_size = models.BigIntegerField(default=0)
    
    # Metadata
    contractor = models.CharField(max_length=255, default="Unknown")
    project = models.CharField(max_length=255, default="Unknown")
    description = models.TextField(blank=True)
    
    # Timestamps
    scan_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField()
    
    def __str__(self):
        return f"{self.filename} ({self.contractor}/{self.project})"
    
    class Meta:
        ordering = ['-scan_date']
        indexes = [
            models.Index(fields=['contractor']),
            models.Index(fields=['project']),
            models.Index(fields=['file_type']),
        ]
