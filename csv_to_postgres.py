import pandas as pd
import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    'dbname': 'heirloom_db',
    'user': 'postgres',
    'password': '0xc097294c1c01fdcc',
    'host': '192.168.1.177',
    'port': '5432'
}

# Read the CSV file into a DataFrame
csv_file_path = 'ouput.csv'
df = pd.read_csv(csv_file_path)

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Create table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS files (
    Filename TEXT,
    Path TEXT,
    Contractor TEXT,
    Project TEXT,
    Description TEXT
)
"""
cur.execute(create_table_query)
conn.commit()

# Insert DataFrame data into the PostgreSQL table
for index, row in df.iterrows():
    insert_query = sql.SQL("""
    INSERT INTO files (Filename, Path, Contractor, Project, Description)
    VALUES (%s, %s, %s, %s, %s)
    """)
    cur.execute(insert_query, tuple(row))

# Commit the transaction and close the connection
conn.commit()
cur.close()
conn.close()