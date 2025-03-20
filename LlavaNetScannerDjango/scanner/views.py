from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils.timezone import make_aware
from datetime import datetime
import pandas as pd
import json
import os
import logging

from .models import ScanResult
from .forms import ScanDirectoryForm, SearchForm
from .scanner_service import scan_directory
from .utils import open_file_location

# Set up logger
logger = logging.getLogger(__name__)

def index(request):
    """Main page with tabs for database view and scanning"""
    # Get unique values for form choices
    contractor_choices = ScanResult.objects.values_list('contractor', flat=True).distinct()
    project_choices = ScanResult.objects.values_list('project', flat=True).distinct()
    file_type_choices = ScanResult.objects.values_list('file_type', flat=True).distinct()
    
    # Initialize forms
    scan_form = ScanDirectoryForm()
    search_form = SearchForm(
        contractor_choices=contractor_choices,
        project_choices=project_choices,
        file_type_choices=file_type_choices
    )
    
    # Initialize with all results (will be filtered if search is submitted)
    queryset = ScanResult.objects.all()
    
    # Handle search form submission
    if request.method == 'GET' and 'search' in request.GET:
        search_form = SearchForm(
            request.GET,
            contractor_choices=contractor_choices,
            project_choices=project_choices,
            file_type_choices=file_type_choices
        )
        
        if search_form.is_valid():
            # Get form data
            search_term = search_form.cleaned_data.get('search_term')
            contractors = search_form.cleaned_data.get('contractors')
            projects = search_form.cleaned_data.get('projects')
            file_types = search_form.cleaned_data.get('file_types')
            
            # Apply filters
            if search_term:
                queryset = queryset.filter(description__icontains=search_term)
            if contractors:
                queryset = queryset.filter(contractor__in=contractors)
            if projects:
                queryset = queryset.filter(project__in=projects)
            if file_types:
                queryset = queryset.filter(file_type__in=file_types)
    
    # Calculate summary metrics
    total_records = queryset.count()
    unique_contractors = queryset.values('contractor').distinct().count()
    unique_projects = queryset.values('project').distinct().count()
    total_size_mb = queryset.aggregate(total=Sum('file_size'))['total'] or 0
    total_size_mb = round(total_size_mb / (1024 * 1024), 2)
    
    # Prepare data for charts
    file_type_data = list(queryset.values('file_type')
                        .annotate(size=Sum('file_size'))
                        .order_by('-size'))
    
    # Convert file sizes to MB
    for item in file_type_data:
        item['size'] = round(item['size'] / (1024 * 1024), 2)
    
    contractor_data = list(queryset.values('contractor')
                          .annotate(project_count=Count('project', distinct=True))
                          .order_by('-project_count')[:10])
    
    context = {
        'scan_form': scan_form,
        'search_form': search_form,
        'results': queryset,
        'total_records': total_records,
        'unique_contractors': unique_contractors,
        'unique_projects': unique_projects,
        'total_size_mb': total_size_mb,
        'file_type_data': json.dumps(file_type_data),
        'contractor_data': json.dumps(contractor_data),
        'active_tab': 'database' if 'search' in request.GET else 'scan'
    }
    
    return render(request, 'scanner/index.html', context)

def scan_new_directory(request):
    """Handle form submission for directory scanning"""
    if request.method == 'POST':
        logger.debug(f"Received POST request: {request.POST}")
        form = ScanDirectoryForm(request.POST)
        
        if form.is_valid():
            logger.debug("Form is valid")
            directory_path = form.cleaned_data['directory_path']
            description_mode = form.cleaned_data['description_mode']
            cutoff_date = form.cleaned_data['cutoff_date']
            
            logger.debug(f"Directory path: {directory_path}")
            logger.debug(f"Description mode: {description_mode}")
            logger.debug(f"Cutoff date: {cutoff_date}")
            
            # Check if directory exists
            if not os.path.exists(directory_path):
                logger.error(f"Directory does not exist: {directory_path}")
                messages.error(request, "Directory does not exist")
                return redirect('index')
            
            # Convert cutoff_date to datetime
            cutoff_datetime = make_aware(datetime.combine(cutoff_date, datetime.min.time()))
            
            try:
                # Scan the directory
                logger.debug("Starting directory scan")
                result = scan_directory(
                    directory_path, 
                    description_mode, 
                    cutoff_datetime
                )
                logger.debug(f"Scan results: {result['stats']}")
                
                # Display success message with stats
                messages.success(
                    request, 
                    f"Scan complete! Found {result['stats']['files_found']} files, "
                    f"processed {result['stats']['files_processed']} files, "
                    f"skipped {result['stats']['files_skipped']} files."
                )
                
                # Add any errors as warnings
                for error in result['stats']['errors']:
                    logger.warning(f"Scan error: {error}")
                    messages.warning(request, error)
                
            except Exception as e:
                logger.exception(f"Error scanning directory: {str(e)}")
                messages.error(request, f"Error scanning directory: {str(e)}")
                
            return redirect('index')
        else:
            logger.error(f"Form is invalid: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        logger.debug(f"Received {request.method} request instead of POST")
    
    # If not POST or form invalid, redirect to index
    return redirect('index')

def export_csv(request):
    """Export filtered results as CSV"""
    # Get the queryset based on the same filters from index view
    queryset = ScanResult.objects.all()
    
    # Apply search filters if any
    if request.GET:
        contractor_choices = ScanResult.objects.values_list('contractor', flat=True).distinct()
        project_choices = ScanResult.objects.values_list('project', flat=True).distinct()
        file_type_choices = ScanResult.objects.values_list('file_type', flat=True).distinct()
        
        search_form = SearchForm(
            request.GET,
            contractor_choices=contractor_choices,
            project_choices=project_choices,
            file_type_choices=file_type_choices
        )
        
        if search_form.is_valid():
            # Get form data
            search_term = search_form.cleaned_data.get('search_term')
            contractors = search_form.cleaned_data.get('contractors')
            projects = search_form.cleaned_data.get('projects')
            file_types = search_form.cleaned_data.get('file_types')
            
            # Apply filters
            if search_term:
                queryset = queryset.filter(description__icontains=search_term)
            if contractors:
                queryset = queryset.filter(contractor__in=contractors)
            if projects:
                queryset = queryset.filter(project__in=projects)
            if file_types:
                queryset = queryset.filter(file_type__in=file_types)
    
    # Convert to DataFrame
    data = list(queryset.values(
        'filename', 'file_path', 'contractor', 'project', 'description',
        'file_type', 'file_size', 'scan_date', 'last_modified'
    ))
    
    df = pd.DataFrame(data)
    
    # Convert file size to MB
    if not df.empty and 'file_size' in df.columns:
        df['file_size'] = df['file_size'] / (1024 * 1024)
        df['file_size'] = df['file_size'].round(2)
        df = df.rename(columns={'file_size': 'size_mb'})
    
    # Create a response with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scan_results.csv"'
    
    df.to_csv(path_or_buf=response, index=False)
    return response

def open_location(request):
    """Open the location of a file in the file explorer"""
    if request.method == 'POST':
        file_path = request.POST.get('file_path')
        
        if file_path and os.path.exists(file_path):
            success = open_file_location(file_path)
            return JsonResponse({'success': success})
    
    return JsonResponse({'success': False})

def test_ollama(request):
    """Test the Ollama service to make sure it's working properly"""
    try:
        logger.debug("Testing Ollama service")
        import ollama
        
        # Try to list models
        models = ollama.list()
        logger.debug(f"Ollama models: {models}")
        
        # Check if llava model is available
        llava_available = any('llava' in model.get('name', '').lower() for model in models.get('models', []))
        
        if llava_available:
            return JsonResponse({
                'success': True, 
                'message': 'Ollama service is working and llava model is available.'
            })
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Ollama service is working but llava model is not available. ' + 
                           'Please run "ollama pull llava" to download it.'
            })
            
    except Exception as e:
        logger.exception(f"Error testing Ollama service: {str(e)}")
        return JsonResponse({
            'success': False, 
            'message': f'Error connecting to Ollama service: {str(e)}'
        })
