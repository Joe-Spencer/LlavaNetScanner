from django import forms
from datetime import datetime

class ScanDirectoryForm(forms.Form):
    """Form for scanning a directory"""
    directory_path = forms.CharField(
        label="Directory Path to Scan",
        max_length=1024,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    DESCRIPTION_CHOICES = [
        ('detailed', 'Detailed - Technical and comprehensive'),
        ('concise', 'Concise - Brief, focused'),
        ('creative', 'Creative - Narrative style')
    ]
    
    description_mode = forms.ChoiceField(
        label="Description Style",
        choices=DESCRIPTION_CHOICES,
        initial='detailed',
        widget=forms.RadioSelect
    )
    
    cutoff_date = forms.DateField(
        label="Process files after date",
        initial=datetime(2023, 10, 1).date(),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
class SearchForm(forms.Form):
    """Form for searching scan results"""
    search_term = forms.CharField(
        label="Search descriptions",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search...'})
    )
    
    contractors = forms.MultipleChoiceField(
        label="Contractors",
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    
    projects = forms.MultipleChoiceField(
        label="Projects",
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    
    file_types = forms.MultipleChoiceField(
        label="File Types",
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        # Get the available choices from the database
        contractor_choices = kwargs.pop('contractor_choices', [])
        project_choices = kwargs.pop('project_choices', [])
        file_type_choices = kwargs.pop('file_type_choices', [])
        
        super(SearchForm, self).__init__(*args, **kwargs)
        
        # Set the choices for the fields
        self.fields['contractors'].choices = [(c, c) for c in contractor_choices]
        self.fields['projects'].choices = [(p, p) for p in project_choices]
        self.fields['file_types'].choices = [(t, t) for t in file_type_choices] 