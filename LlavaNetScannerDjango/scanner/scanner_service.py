import os
import logging
from datetime import datetime
from django.utils.timezone import make_aware
from .utils import is_valid_file, is_image_file, is_design_file, is_pdf_file, CUTOFF_DATE
from .models import ScanResult
from .ai_services import generate_image_description, describe_design, describe_pdf

# Set up logger
logger = logging.getLogger(__name__)

def process_file(file_path, directory, description_mode='detailed'):
    """Process a file and return its metadata and description"""
    try:
        logger.debug(f"Processing file: {file_path}")
        
        # Get relative path components for contractor/project info
        relative_path = os.path.relpath(file_path, directory)
        path_parts = relative_path.split(os.sep)
        contractor = path_parts[0] if len(path_parts) >= 2 else 'unknown'
        project = path_parts[1] if len(path_parts) >= 3 else 'unknown'
        
        # Get the actual filename from the path
        filename = os.path.basename(file_path)
        
        # Get file type
        file_type = os.path.splitext(filename)[1].lower()
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Get last modified time - make timezone aware
        last_modified = make_aware(datetime.fromtimestamp(os.path.getmtime(file_path)))
        
        # Log file details
        logger.debug(f"File details - Filename: {filename}, Type: {file_type}, Size: {file_size}")
        logger.debug(f"File organization - Contractor: {contractor}, Project: {project}")
        
        # Get file description based on type
        description = ''
        if is_image_file(filename):
            logger.debug(f"Identified as image file, generating description")
            description = generate_image_description(file_path, mode=description_mode)
        elif is_design_file(filename):
            logger.debug(f"Identified as design file, generating description")
            description = describe_design(file_path)
        elif is_pdf_file(filename):
            logger.debug(f"Identified as PDF file, generating description")
            description = describe_pdf(file_path)
        else:
            logger.debug(f"Unknown file type: {file_type}")
            description = f'File with extension {file_type}'
            
        # Create result dictionary
        result = {
            'filename': filename,
            'file_path': file_path,
            'contractor': contractor,
            'project': project,
            'description': description,
            'file_type': file_type,
            'file_size': file_size,
            'last_modified': last_modified
        }
        
        logger.debug(f"Successfully processed file: {filename}")
        return result
        
    except Exception as e:
        logger.exception(f"Error processing file {file_path}: {str(e)}")
        # Return a basic result with error message
        return {
            'filename': os.path.basename(file_path),
            'file_path': file_path,
            'contractor': 'unknown',
            'project': 'unknown',
            'description': f'Error processing file: {str(e)}',
            'file_type': os.path.splitext(file_path)[1].lower(),
            'file_size': 0,
            'last_modified': make_aware(datetime.now())  # Make timezone aware
        }

def scan_directory(directory_path, description_mode='detailed', cutoff_date=None):
    """
    Scan files in directory and add them to database
    Returns a dict with statistics and list of processed files
    """
    logger.info(f"Starting directory scan: {directory_path}")
    logger.info(f"Description mode: {description_mode}")
    logger.info(f"Cutoff date: {cutoff_date}")
    
    if cutoff_date is None:
        cutoff_date = CUTOFF_DATE
    
    stats = {
        'files_found': 0,
        'files_processed': 0,
        'files_skipped': 0,
        'errors': []
    }
    
    processed_files = []
    
    try:
        # Walk through directory tree
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                try:
                    stats['files_found'] += 1
                    file_path = os.path.join(root, filename)
                    
                    # Check if file is valid
                    if not is_valid_file(file_path):
                        logger.debug(f"Skipping invalid file: {file_path}")
                        stats['files_skipped'] += 1
                        continue
                    
                    # Check if file modified after cutoff date - make timezone aware
                    file_modified = make_aware(datetime.fromtimestamp(os.path.getmtime(file_path)))
                    if cutoff_date and file_modified < cutoff_date:
                        logger.debug(f"Skipping file older than cutoff: {file_path}")
                        stats['files_skipped'] += 1
                        continue
                    
                    # Process the file
                    logger.debug(f"Processing file: {file_path}")
                    result = process_file(file_path, directory_path, description_mode)
                    
                    # Create or update database entry
                    try:
                        # Try to get existing entry
                        scan_result, created = ScanResult.objects.update_or_create(
                            file_path=file_path,
                            defaults={
                                'filename': result['filename'],
                                'contractor': result['contractor'],
                                'project': result['project'],
                                'description': result['description'],
                                'file_type': result['file_type'],
                                'file_size': result['file_size'],
                                'scan_date': make_aware(datetime.now()),  # Make timezone aware
                                'last_modified': result['last_modified']
                            }
                        )
                        
                        if created:
                            logger.debug(f"Created new database entry for: {file_path}")
                        else:
                            logger.debug(f"Updated existing database entry for: {file_path}")
                            
                        processed_files.append(result)
                        stats['files_processed'] += 1
                        
                    except Exception as e:
                        logger.exception(f"Error saving to database: {str(e)}")
                        stats['errors'].append(f"Database error for {filename}: {str(e)}")
                
                except Exception as e:
                    logger.exception(f"Error processing file {filename}: {str(e)}")
                    stats['errors'].append(f"Error processing {filename}: {str(e)}")
        
        logger.info(f"Scan complete. Stats: {stats}")
        
    except Exception as e:
        logger.exception(f"Error scanning directory {directory_path}: {str(e)}")
        stats['errors'].append(f"Error scanning directory: {str(e)}")
    
    return {
        'stats': stats,
        'processed_files': processed_files
    } 