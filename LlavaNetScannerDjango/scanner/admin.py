from django.contrib import admin
from .models import ScanResult

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('filename', 'contractor', 'project', 'file_type', 'file_size_mb', 'scan_date')
    list_filter = ('contractor', 'project', 'file_type')
    search_fields = ('filename', 'description', 'contractor', 'project')
    readonly_fields = ('scan_date',)
    
    def file_size_mb(self, obj):
        """Display file size in MB"""
        return f"{obj.file_size / (1024 * 1024):.2f} MB"
    file_size_mb.short_description = "Size (MB)"
