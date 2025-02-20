import pandas as pd
from database import Database
from datetime import datetime
import os

def migrate_csv_to_db(csv_file=r'C:\Users\Joseph\Documents\code\misc\LlavaNetScanner\ouput.csv'):
    # Initialize database
    db = Database()
    
    print(f"Reading CSV file: {csv_file}")
    
    # Read CSV file
    df = pd.read_csv(csv_file)
    print(f"Found {len(df)} records in CSV")
    
    success_count = 0
    error_count = 0
    
    # Migrate each row to database
    for _, row in df.iterrows():
        try:
            data = row.to_dict()
            
            # Add placeholder file stats since we can't access the original files
            data['_file_stats'] = {
                'size': 0,  # We'll update this when we actually scan the file
                'mtime': datetime.now().timestamp()
            }
            
            # Clean up the path - remove any problematic characters
            if 'Path' in data:
                data['Path'] = data['Path'].strip()
            
            # Ensure we have all required fields
            if 'Filename' not in data and 'Path' in data:
                data['Filename'] = os.path.basename(data['Path'])
            
            db.add_scan_result(data)
            success_count += 1
            
            # Print progress every 100 records
            if success_count % 100 == 0:
                print(f"Processed {success_count} records...")
            
        except Exception as e:
            print(f"Error processing record: {str(e)}")
            error_count += 1
    
    print(f"\nMigration complete:")
    print(f"Successfully migrated: {success_count} records")
    print(f"Errors encountered: {error_count} records")
    print(f"Total processed: {len(df)} records")

if __name__ == "__main__":
    migrate_csv_to_db() 