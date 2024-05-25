import mysql.connector
from db_connector import setup

# Define the classes for each table
class Committee:
    def __init__(self, comm_name, comm_code=None):
        self.comm_name = comm_name
        self.comm_code = comm_code

class Constituent:
    def __init__(self, start_date, contact_info, constituent_name, constituent_id=None, comm_code=None):
        self.start_date = start_date
        self.contact_info = contact_info
        self.constituent_name = constituent_name
        self.constituent_id = constituent_id
        self.comm_code = comm_code

class Event:
    def __init__(self, date_start, date_end, location, description, event_id=None):
        self.date_start = date_start
        self.date_end = date_end
        self.location = location
        self.description = description
        self.event_id = event_id

class Award:
    def __init__(self, date_awarded, award_name, award_id=None):
        self.date_awarded = date_awarded
        self.award_name = award_name
        self.award_id = award_id

# CRUDL class
class CRUDL:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="eventtracker_db"
        )
        self.cursor = self.db.cursor()

    def create(self, table_name, data):
        auto_increment_columns = self.get_auto_increment_columns(table_name)
        filtered_data = {k: v for k, v in data.__dict__.items() if k not in auto_increment_columns or v is not None}
        columns = ", ".join(filtered_data.keys())
        values = ", ".join(["%s"] * len(filtered_data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.cursor.execute(query, list(filtered_data.values()))
        self.db.commit()
        for col in auto_increment_columns:
            setattr(data, col, self.cursor.lastrowid)

    def get_auto_increment_columns(self, table_name):
        self.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        return [col[0] for col in self.cursor.fetchall() if col[5] == 'auto_increment']

    def read(self, table_name, key_column, key_value):
        query = f"SELECT * FROM {table_name} WHERE {key_column} = %s"
        self.cursor.execute(query, (key_value,))
        return self.cursor.fetchone()

    def update(self, table_name, data, key_column, key_value):
        set_clause = ", ".join([f"{key} = %s" for key in data.__dict__.keys() if key!= key_column])
        values = list(data.__dict__.values()) + [getattr(data, key_column)]
        query = f"UPDATE {table_name} SET {set_clause} WHERE {key_column} = %s"
        try:
            self.cursor.execute(query, tuple(values[:-1]))  # Exclude the last value (key_column) from the tuple
            self.db.commit()
        except Error as e:
            print(f"Error updating record: {e}")
            self.db.rollback()



    def delete(self, table_name, key_column, key_value):
        query = f"DELETE FROM {table_name} WHERE {key_column} = %s"
        self.cursor.execute(query, (key_value,))
        self.db.commit()

    def list(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_columns(self, table_name):
        query = f"SHOW COLUMNS FROM {table_name}"
        self.cursor.execute(query)
        columns = [column[0] for column in self.cursor.fetchall()]
        return columns

    def count_columns(self, table_name):
        query = f"SELECT COUNT(*) AS column_count FROM information_schema.columns WHERE table_name = '{table_name}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0]
    
    def count_rows(self, table_name):
        query = f"SELECT COUNT(*) AS row_count FROM {table_name}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0]
    
    def executeQuery(self, query):
        try:
            self.cursor.execute(query)
            if query.strip().lower().startswith("select"):
                result = self.cursor.fetchall()
                return result
            else:
                self.db.commit()
        except Error as e:
            print(f"Error: {e}")
            self.db.rollback()
    
    
import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import QApplication, QMessageBox

# Assuming you have the setup() function to create the database and tables

def display_members_by_comm_code(comm_code):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="eventtracker_db"
        )
        cursor = db.cursor()
        query = """
            SELECT c.constituent_name, c.contact_info, c.start_date, co.comm_name
            FROM constituent c
            JOIN committee co ON c.comm_code = co.comm_code
            WHERE co.comm_code = %s
        """
        cursor.execute(query, (comm_code,))
        members = cursor.fetchall()
        output = "Members of Committee: {}\n".format(members[0][3])
        for member in members:
            output += "Name: {}, Contact Info: {}, Start Date: {}\n".format(*member[:3])
        show_message_box(output)
    except Error as e:
        print("Error:", e)

def display_constituents_by_award_id(award_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="eventtracker_db"
        )
        cursor = db.cursor()
        query = """
            SELECT c.constituent_name, c.contact_info, c.start_date, a.award_name
            FROM constituent c
            JOIN constituent_award ca ON c.constituent_id = ca.constituent_id
            JOIN award a ON ca.award_id = a.award_id
            WHERE a.award_id = %s
        """
        cursor.execute(query, (award_id,))
        constituents = cursor.fetchall()
        output = "Constituents with Award: {}\n".format(constituents[0][3])
        for constituent in constituents:
            output += "Name: {}, Contact Info: {}, Start Date: {}\n".format(*constituent[:3])
        show_message_box(output)
    except Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()

def display_events_by_constituent_id(constituent_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="eventtracker_db"
        )
        cursor = db.cursor()
        query = """
            SELECT e.description, e.date_start, e.date_end, e.location, c.constituent_name
            FROM event e
            JOIN constituent_event ce ON e.event_id = ce.event_id
            JOIN constituent c ON ce.constituent_id = c.constituent_id
            WHERE c.constituent_id = %s
        """
        cursor.execute(query, (constituent_id,))
        events = cursor.fetchall()
        output = "Events for Constituent: {}\n".format(events[0][4])
        for event in events:
            output += "Description: {}, Start Date: {}, End Date: {}, Location: {}\n".format(*event[:4])
        show_message_box(output)
    except Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()

def display_awards_by_constituent_id(constituent_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="eventtracker_db"
        )
        cursor = db.cursor()
        query = """
            SELECT a.award_name, a.date_awarded, c.constituent_name
            FROM award a
            JOIN constituent_award ca ON a.award_id = ca.award_id
            JOIN constituent c ON ca.constituent_id = c.constituent_id
            WHERE c.constituent_id = %s
        """
        cursor.execute(query, (constituent_id,))
        awards = cursor.fetchall()
        output = "Awards for Constituent: {}\n".format(awards[0][2])
        for award in awards:
            output += "Award Name: {}, Date Awarded: {}\n".format(*award[:2])
        show_message_box(output)
    except Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()

def display_events_and_awards_by_constituent_id(constituent_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="eventtracker_db"
        )
        cursor = db.cursor()
        query = """
            SELECT e.description, e.date_start, e.date_end, e.location, a.award_name, a.date_awarded, c.constituent_name
            FROM constituent c
            JOIN constituent_event ce ON c.constituent_id = ce.constituent_id
            JOIN event e ON ce.event_id = e.event_id
            LEFT JOIN constituent_award ca ON c.constituent_id = ca.constituent_id
            LEFT JOIN award a ON ca.award_id = a.award_id
            WHERE c.constituent_id = %s
        """
        cursor.execute(query, (constituent_id,))
        results = cursor.fetchall()
        output = "Events and Awards for Constituent: {}\n".format(results[0][6])
        for result in results:
            event_details = result[:4]
            award_details = result[4:6]
            output += "Event - Description: {}, Start Date: {}, End Date: {}, Location: {}\n".format(*event_details)
            if award_details[0] is not None:
                output += "Award - Name: {}, Date Awarded: {}\n".format(*award_details)
            output += "\n"
        show_message_box(output)
    except Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()
        
def display_awards_for_event(event_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="eventtracker_db"
        )
        cursor = db.cursor()

        query = f"""
            SELECT event.description AS event_description, award.award_name, award.date_awarded
            FROM event
            LEFT JOIN award ON event.event_id = award.event_id
            WHERE event.event_id = {event_id};
        """
        
        cursor.execute(query)
        awards = cursor.fetchall()
        
        if awards:
            output = "Awards for Event: {}\n".format(awards[0][0])  # Using the first award's description as the header
            for award in awards:
                output += "Award Name: {}, Date Awarded: {}\n".format(award[1], award[2])
        else:
            output = "No awards found for this event."

        show_message_box(output)
    except Error as e:
        print(e)

                

def show_message_box(message_text):
    app = QApplication.instance()  # Get the existing QApplication instance
    if app is None:
        app = QApplication([])  # Create a new QApplication instance if none exists
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Information")
    msg_box.setText(message_text)
    msg_box.exec_()
    
def create_or_update(self, table_name, data):
        if hasattr(data, 'constituent_id') and data.constituent_id:
            self.update(table_name, data, "constituent_id", data.constituent_id)
        else:
            self.create(table_name, data)
  