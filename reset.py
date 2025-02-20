import os
import shutil
import sqlite3
import time
from pathlib import Path

def reset_all():
    """Reset everything - clear cache and database"""
    print("\nResetting LlavaNetScanner...")
    
    # Get the script's directory
    script_dir = Path(__file__).parent.absolute()
    
    # 1. Clear __pycache__ directories
    cache_cleared = False
    for root, dirs, files in os.walk(script_dir):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
                print(f"✓ Cleared cache: {cache_dir}")
                cache_cleared = True
            except Exception as e:
                print(f"✗ Error clearing cache {cache_dir}: {e}")
    
    if not cache_cleared:
        print("ℹ No cache directories found")
    
    # 2. Reset database
    db_file = os.path.join(script_dir, 'scanner_results.db')
    db_reset = False
    
    if os.path.exists(db_file):
        try:
            # Try to drop tables first
            with sqlite3.connect(db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('DROP TABLE IF EXISTS scan_results')
                conn.commit()
            
            # Close connection before removing file
            conn.close()
            
            # Wait a moment to ensure connection is closed
            time.sleep(0.1)
            
            # Remove the file
            os.remove(db_file)
            print(f"✓ Removed database: {db_file}")
            db_reset = True
            
        except Exception as e:
            print(f"✗ Error removing database: {e}")
            try:
                # If we can't remove the file, try to just clear the table
                with sqlite3.connect(db_file) as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM scan_results')
                    conn.commit()
                print("✓ Cleared database contents")
                db_reset = True
            except Exception as e2:
                print(f"✗ Error clearing database contents: {e2}")
    else:
        print("ℹ No database file found")
    
    if not (cache_cleared or db_reset):
        print("\nNothing needed to be reset!")
    else:
        print("\nReset complete! Start the app to create a fresh database.")

if __name__ == "__main__":
    response = input("This will reset everything (clear cache and database). Continue? (y/N): ")
    if response.lower() == 'y':
        reset_all()
    else:
        print("Operation cancelled") 