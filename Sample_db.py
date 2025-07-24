import sqlite3
import os

# Define the database file name
DB_FILE = "student.db"

# Remove the database file if it already exists to start fresh
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Existing database '{DB_FILE}' removed.")

# Connect to the SQLite database. It will be created if it doesn't exist.
connection = sqlite3.connect(DB_FILE)

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Create the STUDENT table
table_info = """
CREATE TABLE STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""
cursor.execute(table_info)

# Insert sample records into the STUDENT table
records_to_insert = [
    ('Alice Smith','10th','A',95),
    ('Bob Johnson','10th','B',88),
    ('Charlie Brown','9th','A',72),
    ('Diana Prince','11th','C',91),
    ('Ethan Hunt','10th','A',78),
    ('Fiona Green','9th','B',65),
    ('George White','12th','A',80),
    ('Hannah Rose','11th','B',93),
    ('Ivy Black','10th','C',70),
    ('Jack Ryan','9th','A',85),
    ('Karen Lee','12th','B',98),
    ('Liam Miller','11th','A',75),
    ('Mia Davis','10th','B',90),
    ('Noah Wilson','9th','C',68),
    ('Olivia Taylor','12th','C',82),
    ('Peter Jones','11th','B',79),
    ('Quinn Martin','10th','A',92),
    ('Rachel Hall','9th','B',71),
    ('Sam Baker','12th','A',86),
    ('Tina Clark','11th','C',94),
    ('Umar Khan','10th','C',60),
    ('Vera Singh','9th','A',89),
    ('Will Turner','12th','B',77),
    ('Xenia Chen','11th','A',96),
    ('Yara Lopez','10th','B',83),
    # --- Additional records added below ---
    ('Zoe Adams', '10th', 'A', 87),
    ('David Lee', '9th', 'B', 76),
    ('Emily White', '11th', 'C', 90),
    ('Frank Green', '12th', 'A', 81),
    ('Grace Hall', '10th', 'B', 73),
    ('Henry King', '9th', 'C', 69),
    ('Isla Scott', '11th', 'A', 97),
    ('Jacob Bell', '12th', 'B', 84),
    ('Kelly Ross', '10th', 'C', 74),
    ('Leo Turner', '9th', 'A', 88)
]

# Use executemany for efficient insertion of multiple records
cursor.executemany("INSERT INTO STUDENT VALUES(?,?,?,?);", records_to_insert)

# Commit the changes to save the inserted records to the database file
connection.commit()

print(f"Database '{DB_FILE}' created and populated successfully with {len(records_to_insert)} records.")

# Optional: Verify records
print("\nVerifying inserted records:")
data = cursor.execute('''SELECT * FROM STUDENT''')
for row in data:
    print(row)

# Close the database connection
connection.close()
