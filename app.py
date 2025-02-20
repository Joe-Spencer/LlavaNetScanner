import streamlit as st
import os
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from NetScanner import scan_files_in_directory, is_image_file, is_design_file, is_pdf_file
from image_describer import generate_description
from design_describer import describe_design
from pdf_describer import describe_pdf
from database import Database
import subprocess
import platform

st.set_page_config(page_title="LlavaNetScanner", layout="wide")

# Initialize database
db = Database()

def open_file_location(path):
    """Open the folder containing the file in the system's file explorer"""
    try:
        if platform.system() == "Windows":
            # On Windows, use explorer and select the file
            subprocess.run(['explorer', '/select,', path])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(['open', '-R', path])
        else:  # Linux
            subprocess.run(['xdg-open', os.path.dirname(path)])
        return True
    except Exception as e:
        st.error(f"Error opening folder: {str(e)}")
        return False

def main():
    st.title("LlavaNetScanner")
    
    # Main content area with tabs
    tab1, tab2 = st.tabs(["Database View", "Add New Data"])

    with tab1:
        st.subheader("Database Contents")
        
        # Get all results from database
        results = db.get_results()
        if results:
            df = pd.DataFrame(results)
            
            # Convert file sizes to MB
            df['file_size'] = df['file_size'] / (1024 * 1024)
            df['file_size'] = df['file_size'].round(2)
            df = df.rename(columns={'file_size': 'size_mb'})
            
            # Add summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Unique Contractors", df['contractor'].nunique())
            with col3:
                st.metric("Unique Projects", df['project'].nunique())
            with col4:
                st.metric("Total Size (MB)", f"{df['size_mb'].sum():.2f}")
            
            # Filters in sidebar
            st.sidebar.header("Filters")
            
            # Contractor filter
            contractors = st.sidebar.multiselect(
                "Select Contractors",
                options=sorted(df['contractor'].unique())
            )
            
            # Project filter
            projects = st.sidebar.multiselect(
                "Select Projects",
                options=sorted(df['project'].unique())
            )
            
            # File type filter
            file_types = st.sidebar.multiselect(
                "Select File Types",
                options=sorted(df['file_type'].unique())
            )
            
            # Apply filters
            if contractors:
                df = df[df['contractor'].isin(contractors)]
            if projects:
                df = df[df['project'].isin(projects)]
            if file_types:
                df = df[df['file_type'].isin(file_types)]
            
            # Search functionality
            search_term = st.text_input("Search descriptions:")
            if search_term:
                df = df[df['description'].str.contains(search_term, case=False, na=False)]
            
            # Display filtered data
            st.dataframe(
                df[[
                    'filename', 'file_path', 'contractor', 'project', 'description',
                    'file_type', 'size_mb', 'scan_date', 'last_modified'
                ]],
                use_container_width=True,
                column_config={
                    "filename": st.column_config.Column(
                        "Filename",
                        help="Click to open file location",
                        width="medium"
                    ),
                    "file_path": st.column_config.Column(
                        "File Path",
                        help="Full path to file",
                        width="large"
                    ),
                    "size_mb": st.column_config.NumberColumn("Size (MB)"),
                    "scan_date": st.column_config.DatetimeColumn("Scan Date"),
                    "last_modified": st.column_config.DatetimeColumn("Last Modified")
                }
            )
            
            # Visualizations
            st.subheader("Data Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                # File types distribution
                fig1 = px.pie(
                    df, 
                    names='file_type',
                    values='size_mb',
                    title='Storage by File Type'
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Top contractors by project count
                contractor_projects = df.groupby('contractor')['project'].nunique().sort_values(ascending=False).head(10)
                fig2 = px.bar(
                    x=contractor_projects.index,
                    y=contractor_projects.values,
                    title='Top 10 Contractors by Number of Projects',
                    labels={'x': 'Contractor', 'y': 'Number of Projects'}
                )
                fig2.update_layout(showlegend=False)
                st.plotly_chart(fig2, use_container_width=True)
            
            # Download filtered results
            st.download_button(
                label="Download Filtered Results",
                data=df.to_csv(index=False),
                file_name="scan_results.csv",
                mime="text/csv"
            )
            
        else:
            st.info("No records found in database. Add data using the 'Add New Data' tab.")

    with tab2:
        st.subheader("Scan New Directory")
        
        # Directory Selection
        directory_path = st.text_input("Enter Directory Path to Scan")
        
        # Scan Settings
        col1, col2 = st.columns(2)
        with col1:
            description_mode = st.radio(
                "Description Style",
                ["detailed", "concise", "creative"],
                help="""
                detailed: Technical and comprehensive description
                concise: Brief, focused description
                creative: Narrative style description
                """
            )
        with col2:
            cutoff_date = st.date_input(
                "Process files after date",
                value=datetime(2023, 10, 1)
            )
        
        if st.button("Start Scan"):
            if not directory_path or not os.path.exists(directory_path):
                st.error("Please enter a valid directory path")
                return
                
            with st.spinner(f"Scanning directory using {description_mode} mode..."):
                # Update CUTOFF_DATE in NetScanner
                import NetScanner
                NetScanner.CUTOFF_DATE = datetime.combine(cutoff_date, datetime.min.time())
                
                # Pass description_mode to process_file
                def process_with_mode(file_path, directory):
                    try:
                        # Get basic file info first
                        result = {
                            'Filename': os.path.basename(file_path),
                            'Path': file_path,
                            'Contractor': 'unknown',
                            'Project': 'unknown',
                            'Description': '',
                            'file_type': os.path.splitext(file_path)[1].lower()
                        }
                        
                        # Get path-based info
                        relative_path = os.path.relpath(file_path, directory)
                        path_parts = relative_path.split(os.sep)
                        if len(path_parts) >= 2:
                            result['Contractor'] = path_parts[0]
                        if len(path_parts) >= 3:
                            result['Project'] = path_parts[1]
                        
                        # Generate description based on file type and selected mode
                        if is_image_file(file_path):
                            result['Description'] = generate_description(
                                file_path, 
                                mode=description_mode
                            )
                        elif is_design_file(file_path):
                            result['Description'] = describe_design(file_path)
                        elif is_pdf_file(file_path):
                            result['Description'] = describe_pdf(file_path)
                        else:
                            result['Description'] = 'Unknown file type'
                            
                        return result
                        
                    except Exception as e:
                        print(f"Error in process_with_mode: {str(e)}")
                        return {
                            'Filename': os.path.basename(file_path),
                            'Path': file_path,
                            'Contractor': 'unknown',
                            'Project': 'unknown',
                            'Description': f'Error processing file: {str(e)}',
                            'file_type': os.path.splitext(file_path)[1].lower()
                        }
                
                # Temporarily replace process_file with our modified version
                original_process = NetScanner.process_file
                NetScanner.process_file = process_with_mode
                
                try:
                    # Run the scan
                    results = scan_files_in_directory(directory_path, db)
                    
                    st.success(f"Scan complete! Added {len(results)} new records to database.")
                    
                    # Show preview of new data
                    if results:
                        st.subheader("Preview of Added Data")
                        preview_df = pd.DataFrame(results)
                        st.dataframe(
                            preview_df[[
                                'Filename',
                                'Contractor',
                                'Project',
                                'Description',
                                'file_type'
                            ]],
                            use_container_width=True
                        )
                finally:
                    # Restore original process_file
                    NetScanner.process_file = original_process

if __name__ == "__main__":
    main() 