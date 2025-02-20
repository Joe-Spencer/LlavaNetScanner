import sqlite3
import pandas as pd
from tabulate import tabulate

def view_database(db_file='scanner_results.db'):
    try:
        # Connect to database
        conn = sqlite3.connect(db_file)
        
        # Get all results
        query = """
        SELECT 
            filename,
            contractor,
            project,
            description,
            file_type,
            file_size,
            scan_date,
            last_modified
        FROM scan_results
        ORDER BY scan_date DESC
        """
        
        # Load into pandas for nice display
        df = pd.read_sql_query(query, conn)
        
        # Convert file sizes to MB
        df['file_size'] = df['file_size'] / (1024 * 1024)
        df['file_size'] = df['file_size'].round(2)
        df = df.rename(columns={'file_size': 'size_mb'})
        
        # Display results
        print("\nDatabase Contents:")
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
        
        # Print summary
        print(f"\nTotal Records: {len(df)}")
        print(f"Unique Contractors: {df['contractor'].nunique()}")
        print(f"Unique Projects: {df['project'].nunique()}")
        print(f"Total Size: {df['size_mb'].sum():.2f} MB")
        
    except Exception as e:
        print(f"Error viewing database: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    view_database() 