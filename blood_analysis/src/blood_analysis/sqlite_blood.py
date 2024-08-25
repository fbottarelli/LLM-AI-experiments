import sqlite3
import csv
import os

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def create_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        test_name TEXT,
        result REAL
    )
    ''')
    conn.commit()

def process_csv_files(folder_path, conn):
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    name = row['name']
                    surname = row['surname']
                    table_name = f"{name}_{surname}".lower()
                    
                    create_table(conn, table_name)
                    
                    cursor = conn.cursor()
                    cursor.execute(f'''
                    INSERT INTO {table_name} (date, test_name, result)
                    VALUES (?, ?, ?)
                    ''', (row['date'], row['test_name'], row['result']))
    
    conn.commit()

def main():
    db_name = 'blood_analysis.db'
    csv_folder = 'path/to/your/csv/folder'  # Replace with the actual path to your CSV folder
    
    conn = create_database(db_name)
    process_csv_files(csv_folder, conn)
    conn.close()
    
    print(f"Database '{db_name}' has been created and populated with data from CSV files.")

if __name__ == "__main__":
    main()