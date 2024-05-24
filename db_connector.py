import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQLpassword101",
            database="eventtracker_db",
            port="3306"
        )
        if connection.is_connected():
            print("Successfully connected to the database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query, values=None):
    cursor = connection.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query, values=None):
    cursor = connection.cursor()
    result = None
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

# CRUDL operations for members table
def create_member(connection, name, email, phone, join_date):
    query = "INSERT INTO members (name, email, phone, join_date) VALUES (%s, %s, %s, %s)"
    values = (name, email, phone, join_date)
    execute_query(connection, query, values)

def read_member(connection, member_id):
    query = "SELECT * FROM members WHERE id = %s"
    values = (member_id,)
    return execute_read_query(connection, query, values)

def update_member(connection, member_id, name, email, phone, join_date):
    query = "UPDATE members SET name = %s, email = %s, phone = %s, join_date = %s WHERE id = %s"
    values = (name, email, phone, join_date, member_id)
    execute_query(connection, query, values)

def delete_member(connection, member_id):
    query = "DELETE FROM members WHERE id = %s"
    values = (member_id,)
    execute_query(connection, query, values)

def list_members(connection):
    query = "SELECT * FROM members"
    return execute_read_query(connection, query)

# Similarly, you can create CRUDL operations for the other tables (committees, events, awards)

# CRUDL operations for committees table
def create_committee(connection, name, description):
    query = "INSERT INTO committees (name, description) VALUES (%s, %s)"
    values = (name, description)
    execute_query(connection, query, values)

def read_committee(connection, committee_id):
    query = "SELECT * FROM committees WHERE id = %s"
    values = (committee_id,)
    return execute_read_query(connection, query, values)

def update_committee(connection, committee_id, name, description):
    query = "UPDATE committees SET name = %s, description = %s WHERE id = %s"
    values = (name, description, committee_id)
    execute_query(connection, query, values)

def delete_committee(connection, committee_id):
    query = "DELETE FROM committees WHERE id = %s"
    values = (committee_id,)
    execute_query(connection, query, values)

def list_committees(connection):
    query = "SELECT * FROM committees"
    return execute_read_query(connection, query)

# CRUDL operations for events table
def create_event(connection, name, date, location, description):
    query = "INSERT INTO events (name, date, location, description) VALUES (%s, %s, %s, %s)"
    values = (name, date, location, description)
    execute_query(connection, query, values)

def read_event(connection, event_id):
    query = "SELECT * FROM events WHERE id = %s"
    values = (event_id,)
    return execute_read_query(connection, query, values)

def update_event(connection, event_id, name, date, location, description):
    query = "UPDATE events SET name = %s, date = %s, location = %s, description = %s WHERE id = %s"
    values = (name, date, location, description, event_id)
    execute_query(connection, query, values)

def delete_event(connection, event_id):
    query = "DELETE FROM events WHERE id = %s"
    values = (event_id,)
    execute_query(connection, query, values)

def list_events(connection):
    query = "SELECT * FROM events"
    return execute_read_query(connection, query)

# CRUDL operations for awards table
def create_award(connection, member_id, name, year):
    query = "INSERT INTO awards (member_id, name, year) VALUES (%s, %s, %s)"
    values = (member_id, name, year)
    execute_query(connection, query, values)

def read_award(connection, award_id):
    query = "SELECT * FROM awards WHERE id = %s"
    values = (award_id,)
    return execute_read_query(connection, query, values)

def update_award(connection, award_id, member_id, name, year):
    query = "UPDATE awards SET member_id = %s, name = %s, year = %s WHERE id = %s"
    values = (member_id, name, year, award_id)
    execute_query(connection, query, values)

def delete_award(connection, award_id):
    query = "DELETE FROM awards WHERE id = %s"
    values = (award_id,)
    execute_query(connection, query, values)

def list_awards(connection):
    query = "SELECT * FROM awards"
    return execute_read_query(connection, query)
