import mysql.connector
from mysql.connector import Error

# Setup database and tables
def setup():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123"
    )

    cursor = db.cursor()

    # Create a new database
    cursor.execute("CREATE DATABASE IF NOT EXISTS eventtracker_db")

    # Use the new database
    cursor.execute("USE eventtracker_db")

    # Create the tables with adjusted column orders
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS committee (
        comm_code INT AUTO_INCREMENT PRIMARY KEY,
        comm_name VARCHAR(255) NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS constituent (
        constituent_id INT AUTO_INCREMENT PRIMARY KEY,
        constituent_name VARCHAR(255) NOT NULL, 
        contact_info VARCHAR(255),
        start_date DATE,
        comm_code INT,
        FOREIGN KEY (comm_code) REFERENCES committee(comm_code)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS event (
        event_id INT AUTO_INCREMENT PRIMARY KEY,
        description TEXT,
        date_start DATE,
        date_end DATE,
        location VARCHAR(255)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS award (
        award_id INT AUTO_INCREMENT PRIMARY KEY,
        award_name VARCHAR(255),
        date_awarded DATE,
        event_id INT,
        FOREIGN KEY (event_id) REFERENCES event(event_id)
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS constituent_event (
        constituent_id INT NOT NULL,
        event_id INT NOT NULL,
        PRIMARY KEY (constituent_id, event_id),
        FOREIGN KEY (constituent_id) REFERENCES constituent(constituent_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS constituent_award (
        constituent_id INT NOT NULL,
        award_id INT NOT NULL,
        PRIMARY KEY (constituent_id, award_id),
        FOREIGN KEY (constituent_id) REFERENCES constituent(constituent_id),
        FOREIGN KEY (award_id) REFERENCES award(award_id)
    );
    """)


    # Commit the changes and close the connection
    db.commit()
    cursor.close()
    db.close()

setup()

# Instantiate CRUDL class and execute left join query