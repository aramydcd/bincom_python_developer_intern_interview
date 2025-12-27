import sqlite3
import re
import os

def initialize_database():
    sql_file = 'bincom_test.sql'
    db_file = 'election_results.db'

    # SAFETY CHECK: Check if the SQL file actually exists
    if not os.path.exists(sql_file):
        print(f"Error: {sql_file} not found in this folder!")
        return

    # CONNECTIVITY: Connect to SQLite
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    print("Reading and cleaning SQL file...")
    
    # ACCESSING: Read the SQL file (using latin1 to avoid encoding errors)
    with open(sql_file, 'r', encoding='latin1') as f:
        lines = f.readlines()

    cleaned_sql = []
    
    # FORMATTING
    for line in lines:
        # Skip MySQL specific headers/settings that crash SQLite
        if line.strip().startswith(('SET', '/*', '/*!', 'LOCK TABLES', 'UNLOCK TABLES', 'ALTER TABLE')):
            continue
        
        # Remove MySQL "ENGINE=..." and "AUTO_INCREMENT=..." from CREATE TABLE statements
        # SQLite doesn't use these.
        line = re.sub(r'ENGINE=.*?;', ';', line)
        line = line.replace('AUTO_INCREMENT', '')
        
        cleaned_sql.append(line)

    # Combine back into one script
    full_script = "".join(cleaned_sql)

    try:
        print("Executing SQL script... This might take 5-10 seconds.")
        # EXECUTING: Use executescript to run the whole file at once
        cursor.executescript(full_script)
        conn.commit()
        print(f"Successfully created {db_file}!")
    except Exception as e:
        print(f"Error during initialization: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()