import sqlite3
import csv
import os
from typing import List, Dict, Any

db_path = '/home/admin/ouroboros_data/local_db/inventory.db'

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This allows access by column name
    return conn

def init_db():
    """Initialize the database and create the inventory table if it doesn't exist."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the inventory table with the new CSV schema
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        system_id TEXT,
        system_name TEXT,
        domain TEXT,
        owner TEXT,
        tech_lead TEXT,
        criticality TEXT,
        lifecycle TEXT,
        frontend TEXT,
        backend TEXT,
        db TEXT,
        integrations TEXT,
        hosting TEXT,
        vendor_custom TEXT,
        last_update TEXT
    )
    ''')
    conn.commit()
    conn.close()
    
    return {'success': True, 'message': f'Database initialized at {db_path}'}

def load_csv_to_db(csv_data: str):
    """Parse the CSV data and load it into the SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Prepare the CSV reader
    from io import StringIO
    csv_file = StringIO(csv_data)
    reader = csv.DictReader(csv_file, delimiter=';')
    
    # Clear existing data
    cursor.execute('DELETE FROM inventory')
    
    # Insert new data
    for row in reader:
        cursor.execute('''
            INSERT INTO inventory (
                system_id, system_name, domain, owner, tech_lead, criticality, 
                lifecycle, frontend, backend, db, integrations, hosting, 
                vendor_custom, last_update
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['System ID'],
            row['System Name'],
            row['Domain'],
            row['Owner'],
            row['Tech Lead'],
            row['Criticality'],
            row['Lifecycle'],
            row['Frontend'],
            row['Backend'],
            row['DB'],
            row['Integrations'],
            row['Hosting'],
            row['Vendor / Custom'],
            row['Last Update']
        ))
    
    conn.commit()
    conn.close()
    
    return {'success': True, 'message': f'Data loaded successfully. Total rows: {list(reader)[-1]}'}

def query_systems_by_criticality(criticality: str) -> List[Dict[str, Any]]:
    """Query the database for systems with a specific criticality."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT system_id, system_name, domain, owner, criticality FROM inventory WHERE criticality = ?', 
        (criticality,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_all_systems() -> List[Dict[str, Any]]:
    """Get all systems from the inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT system_id, system_name, domain, owner, criticality FROM inventory')
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]