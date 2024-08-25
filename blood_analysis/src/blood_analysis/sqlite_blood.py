import sqlite3
import csv
import os

def create_database(db_name):
    """Create a new SQLite database and return the connection object."""
    conn = sqlite3.connect(db_name)  # Connect to the database (creates it if it doesn't exist)
    return conn  # Return the connection object

def create_table(conn, table_name):
    """Create a new table in the database if it doesn't already exist."""
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    # Create a table if it doesn't already exist with the following structure:
    # - id: Auto-incrementing ID for each record
    # - date: Date of the test
    # - test_name: Name of the test
    # - result: Result of the test
    # - range: Range of healthy values for the test
    # - unit: Unit of measurement for the test
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        test_name TEXT,
        result REAL,
        range TEXT,
        unit TEXT
    )
    ''')
    conn.commit()  # Commit the changes to the database

def create_log_table(conn):
    """Create a log table to track processed CSV files."""
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS processed_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT UNIQUE
    )
    ''')  # Execute the SQL command to create the table if it doesn't exist
    conn.commit()  # Commit the changes to the database

def is_file_processed(conn, filename):
    """Check if a file has already been processed."""
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    cursor.execute('SELECT 1 FROM processed_files WHERE filename = ?', (filename,))  # Execute the SQL command to check if the file is already processed
    return cursor.fetchone() is not None  # Return True if the file is found, otherwise False

def log_processed_file(conn, filename):
    """Log a file as processed."""
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    cursor.execute('INSERT INTO processed_files (filename) VALUES (?)', (filename,))  # Execute the SQL command to insert the filename into the log table
    conn.commit()  # Commit the changes to the database

def process_csv_files(folder_path, conn):
    """Process all CSV files in the specified folder and insert data into the database."""
    for filename in os.listdir(folder_path):  # Iterate through all files in the folder
        if filename.endswith('.csv') and not is_file_processed(conn, filename):  # Check if the file is a CSV and not processed
            file_path = os.path.join(folder_path, filename)  # Get the full file path
            with open(file_path, 'r') as csvfile:  # Open the CSV file for reading
                csv_reader = csv.DictReader(csvfile)  # Create a CSV reader object
                for row in csv_reader:  # Iterate through each row in the CSV
                    name = row['Name']  # Extract the name from the row
                    surname = row['Surname']  # Extract the surname from the row
                    table_name = f"{name}_{surname}".lower()  # Create a table name based on name and surname
                    
                    create_table(conn, table_name)  # Create the table if it doesn't exist
                    
                    cursor = conn.cursor()  # Create a new cursor object
                    cursor.execute(f'''
                    INSERT INTO {table_name} (date, test_name, result, range, unit)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (row['Date'], row['Test Name'], row['Result'], row['Reference Range'], row['Units']))  # Insert the date, test name, result, range, and unit
            
            log_processed_file(conn, filename)  # Log the file as processed
    
    conn.commit()  # Commit all changes to the database

def main():
    """Main function to create the database and process CSV files."""
    db_name = 'data/sqlite/blood_analysis.db'  # Name of the database
    csv_folder = 'data/tamara_cibrozzi'  # Replace with the actual path to your CSV folder
    
    conn = create_database(db_name)  # Create the database and get the connection
    create_log_table(conn)  # Create the log table
    process_csv_files(csv_folder, conn)  # Process the CSV files and insert data
    conn.close()  # Close the database connection
    
    print(f"Database '{db_name}' has been created and populated with data from CSV files.")  # Print a success message

if __name__ == "__main__":
    main()  # Run the main function