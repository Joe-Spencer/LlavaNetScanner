import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_file='scanner_results.db'):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Create main results table with unique constraint on file_path
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scan_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL UNIQUE,
                    contractor TEXT,
                    project TEXT,
                    description TEXT,
                    file_type TEXT,
                    file_size INTEGER,
                    scan_date TIMESTAMP,
                    last_modified TIMESTAMP
                )
            ''')
            
            conn.commit()

    def add_scan_result(self, result):
        """Add or update a scan result"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Get file stats
            try:
                file_stats = os.stat(result['Path'])
                file_size = file_stats.st_size
                last_modified = datetime.fromtimestamp(file_stats.st_mtime)
            except (FileNotFoundError, OSError):
                file_size = 0
                last_modified = datetime.now()
            
            # Get file type
            file_type = os.path.splitext(result['Filename'])[1].lower()
            
            try:
                # Use INSERT OR REPLACE to handle duplicates
                cursor.execute('''
                    INSERT OR REPLACE INTO scan_results 
                    (filename, file_path, contractor, project, description, 
                     file_type, file_size, scan_date, last_modified)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    result['Filename'],
                    result['Path'],
                    result.get('Contractor', 'Unknown'),
                    result.get('Project', 'Unknown'),
                    result.get('Description', ''),
                    file_type,
                    file_size,
                    datetime.now(),
                    last_modified
                ))
                
                conn.commit()
            except Exception as e:
                print(f"Error inserting record for {result['Path']}: {str(e)}")
                raise

    def get_results(self, filters=None):
        """Get scan results with optional filtering"""
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM scan_results"
            params = []
            
            if filters:
                conditions = []
                if 'file_path' in filters:
                    # Use exact path matching
                    conditions.append("LOWER(file_path) = LOWER(?)")
                    params.append(filters['file_path'])
                if 'contractors' in filters and filters['contractors']:
                    conditions.append("contractor IN (" + ",".join("?" * len(filters['contractors'])) + ")")
                    params.extend(filters['contractors'])
                if 'projects' in filters and filters['projects']:
                    conditions.append("project IN (" + ",".join("?" * len(filters['projects'])) + ")")
                    params.extend(filters['projects'])
                if 'file_types' in filters and filters['file_types']:
                    conditions.append("file_type IN (" + ",".join("?" * len(filters['file_types'])) + ")")
                    params.extend(filters['file_types'])
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_statistics(self):
        """Get scanning statistics"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Total files
            cursor.execute("SELECT COUNT(*) FROM scan_results")
            stats['total_files'] = cursor.fetchone()[0]
            
            # Files by type
            cursor.execute("""
                SELECT file_type, COUNT(*) as count, SUM(file_size) as total_size 
                FROM scan_results 
                GROUP BY file_type
            """)
            stats['file_types'] = {row[0]: {'count': row[1], 'size': row[2]} 
                                 for row in cursor.fetchall()}
            
            # Contractors and projects
            cursor.execute("SELECT DISTINCT contractor FROM scan_results")
            stats['contractors'] = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT DISTINCT project FROM scan_results")
            stats['projects'] = [row[0] for row in cursor.fetchall()]
            
            return stats 

    def clear_database(self):
        """Clear all records from the database"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM scan_results')
            conn.commit() 