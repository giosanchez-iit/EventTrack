import mysql.connector
from datetime import datetime
from db_connector import setup

class DatabaseCRUDL:
    
    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.connect()
        setup()
        
    def connect(self):
        try:
            self.cnx = mysql.connector.connect(host="127.0.0.1", user="root", password="123", database="eventtracker_db")
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            pass
            
    def executeQuery(self, query):
        try:
            self.cursor.execute(query)
            self.cnx.commit()
        except mysql.connector.Error as e:
            pass
            
    def executeQueryWithReturn(self, query):
        try:
            self.cursor.execute(query)
            self.cnx.commit()
        except mysql.connector.Error as e:
            pass
        return self.cursor.fetchall()
    
    def formatforSQL(self, attrib):
        if attrib is None or attrib =='' or attrib=='None':
            return 'NULL'
        elif isinstance(attrib, int):
            return str(attrib)
        return f"'{attrib}'"
    
    def dateToday(self):
        today = datetime.today()
        formatted_date = today.strftime("%Y-%m-%d")
        return formatted_date
    
    # ===========================================
    # Committee
    # ===========================================
    
    def createCommittee(self, comm_name):
        comm_name = self.formatforSQL(comm_name)
        query = f"""
            INSERT INTO committee (comm_name) VALUES ({comm_name});
        """
        self.executeQuery(query)
    
    def readCommittee(self, comm_code):
        comm_code = self.formatforSQL(comm_code)
        query = f"""
            SELECT * FROM committee WHERE comm_code={comm_code};        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result[0] 
        
    def updateCommittee(self, comm_code, new_comm_name):
        new_comm_name = self.formatforSQL(new_comm_name)
        comm_code = self.formatforSQL(comm_code)
        query = f"""
            UPDATE committee SET comm_name = '{new_comm_name}' WHERE comm_code={comm_code};
        """
        self.executeQuery(query)
        
    def deleteCommittee(self, comm_code):
        comm_code = self.formatforSQL(comm_code)
        
        update_query = f"""UPDATE constituent SET comm_code = NULL WHERE comm_code = {comm_code};"""
        delete_query = f"""DELETE FROM committee WHERE comm_code={comm_code};"""
        
        self.executeQuery(update_query)
        self.executeQuery(delete_query)

        
    def listCommittee(self):
        query = f"""
            SELECT * FROM committee
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def listCommitteeForTable(self, thingtoquery=None):
        query1 = f"""
            SELECT * FROM committee
        """
        query2 = ''
        if thingtoquery:
            query2 = f""" WHERE comm_name LIKE '%{thingtoquery}%';"""
        final = query1 + query2
        self.cursor.execute(final)
        result = self.cursor.fetchall()
        return result
    
    # ===========================================
    # Constituent
    # ===========================================
    
    def createConstituent(self, constituent_name, contact_info, start_date, comm_code):
        constituent_name = self.formatforSQL(constituent_name)
        contact_info = self.formatforSQL(contact_info)
        start_date = self.formatforSQL(start_date)
        comm_code = self.formatforSQL(comm_code)
        query = f"""
            INSERT INTO constituent (constituent_name, contact_info, start_date, comm_code)
            VALUES ({constituent_name}, {contact_info}, {start_date}, {comm_code});
        """
        self.executeQuery(query)
    
    def readConstituent(self, constituent_id):
        constituent_id = self.formatforSQL(constituent_id)
        query = f"""
            SELECT * FROM constituent WHERE constituent_id={constituent_id}
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def updateConstituent(self, constituent_id, new_constituent_name, new_contact_info, new_comm_code):
        new_constituent_name = self.formatforSQL(new_constituent_name)
        new_contact_info = self.formatforSQL(new_contact_info)
        new_comm_code = self.formatforSQL(new_comm_code)
        constituent_id = self.formatforSQL(constituent_id)

        query = f"""
            UPDATE Constituent
            SET constituent_name={new_constituent_name},
            contact_info={new_contact_info},
            comm_code={new_comm_code}
            WHERE constituent_id={constituent_id} 
        """
        print(query)
        self.executeQuery(query)
    
    def deleteConstituent(self, constituent_id):
        constituent_id = self.formatforSQL(constituent_id)
        query1 = f"""DELETE FROM constituent_award WHERE constituent_id = {constituent_id};"""
        query2 = f"""DELETE FROM constituent_event WHERE constituent_id = {constituent_id};"""
        query3 = f"""DELETE FROM constituent WHERE constituent_id = {constituent_id};"""
        self.executeQuery(query1)
        self.executeQuery(query2)
        self.executeQuery(query3)

    def listConstituent(self):
        query = f"""
            SELECT * FROM constituent
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def listConstituentForTable(self, constituent_id=None, thingtoquery=None):
        base_query = """
            SELECT c.constituent_id, c.constituent_name, c.contact_info, c.start_date, committee.comm_name
            FROM constituent as c
            LEFT JOIN committee ON c.comm_code = committee.comm_code
        """

        where_clause = where_clause1 = where_clause2 = ''
        and_clause = ''

        if constituent_id or thingtoquery:
            where_clause = "WHERE "

        if constituent_id:
            where_clause1 = f"c.constituent_id={constituent_id}"

        if constituent_id and thingtoquery:
            and_clause = """
                AND
            """
            
        if thingtoquery:
            where_clause2 = f"(c.constituent_name LIKE '%{thingtoquery}%')"

        final_query = base_query + where_clause + where_clause1 + and_clause + where_clause2
        self.cursor.execute(final_query)
        result = self.cursor.fetchall()
        return result
    
    # ===========================================
    # Event
    # ===========================================
    
    def createEvent(self, description, date_start, date_end, location):
        description = self.formatforSQL(description)
        date_start = self.formatforSQL(date_start)
        date_end = self.formatforSQL(date_end)
        location = self.formatforSQL(location)
        
        query = f"""
            INSERT INTO event (description, date_start, date_end, location)
            VALUES ({description}, {date_start}, {date_end}, {location})
        """
        self.executeQuery(query)
        
    def readEvent(self, event_id):
        event_id = self.formatforSQL(event_id)
        query = f"""
            SELECT * FROM event WHERE event_id={event_id}
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def updateEvent(self, event_id, description, date_start, date_end, location):
        event_id = self.formatforSQL(event_id)
        description = self.formatforSQL(description)
        date_start = self.formatforSQL(date_start)
        date_end = self.formatforSQL(date_end)
        query = f"""
            UPDATE event
            SET description = {description}, date_start = {date_start}, date_end = {date_end}, location = {location}
            WHERE event_id = {event_id};
        """
        self.executeQuery(query)
        
    def deleteEvent(self, event_id):
        event_id = self.formatforSQL(event_id)
        query1 = f"""
            DELETE FROM constituent_event WHERE event_id = {event_id};
        """
        query2 = f"""
            DELETE FROM constituent_award
            WHERE award_id IN (
                SELECT award_id FROM award WHERE event_id = {event_id}
            );
        """
        query3 = f"""
            DELETE FROM award WHERE event_id = {event_id};
        """
        query4 = f"""
            DELETE FROM event WHERE event_id = {event_id};
        """
        
        self.executeQuery(query1)
        self.executeQuery(query2)
        self.executeQuery(query3)
        self.executeQuery(query4)
        
    def listEvent(self):
        query = f"""
            SELECT * FROM event
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    # ===========================================
    # Award
    # ===========================================

    def createAward(self, award_name, date_awarded, event_id):
        award_name = self.formatforSQL(award_name)
        date_awarded = self.formatforSQL(date_awarded)
        event_id = self.formatforSQL(event_id)
        
        query = f"""
            INSERT INTO award (award_name, date_awarded, event_id)
            VALUES ({award_name}, {date_awarded}, {event_id});
        """
        self.executeQuery(query)
    
    def readAward(self, award_id):
        award_id = self.formatforSQL(award_id)
        query = f"""
            SELECT * FROM award WHERE award_id={award_id}
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result[0] if result else None
    
    def updateAward(self, award_id, award_name, date_awarded):
        award_name = self.formatforSQL(award_name)
        date_awarded = self.formatforSQL(date_awarded)
        award_id = self.formatforSQL(award_id)

        query = f"""
            UPDATE award
            SET award_name = {award_name}, date_awarded = {date_awarded}
            WHERE award_id = {award_id};
        """
        self.executeQuery(query)
    
    def deleteAward(self, award_id):
        award_id = self.formatforSQL(award_id)
        query1 = f"""DELETE FROM constituent_award WHERE award_id = {award_id};"""
        query2 = f"""DELETE FROM award WHERE award_id={award_id};"""
        self.executeQuery(query1)
        self.executeQuery(query2)
    
    def listAward(self):
        query = f"""
            SELECT * FROM award
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def listAwardForTable(self):
        query = f"""
            SELECT a.award_name, a.date_awarded, e.description
            FROM award as a
            LEFT JOIN event AS e ON a.event_id = e.event_id
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    # ===========================================
    # Constituent Award
    # ===========================================

    def createConstituentAward(self, constituent_id, award_id):
        constituent_id = self.formatforSQL(constituent_id)
        award_id = self.formatforSQL(award_id)
        query = f"""
            INSERT INTO constituent_award (constituent_id, award_id)
            VALUES ({constituent_id}, {award_id});
        """
        self.executeQuery(query)

    def readConstituentAward(self, constituent_id, award_id):
        constituent_id = self.formatforSQL(constituent_id)
        award_id = self.formatforSQL(award_id)
        query = f"""
            SELECT * FROM constituent_award
            WHERE constituent_id={constituent_id} AND award_id={award_id};
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def deleteConstituentAward(self, constituent_id, award_id):
        constituent_id = self.formatforSQL(constituent_id)
        award_id = self.formatforSQL(award_id)
        query = f"""
            DELETE FROM constituent_award
            WHERE constituent_id={constituent_id} AND award_id={award_id};
        """
        self.executeQuery(query)
        
    def listConstituentAwardForTable(self, constituentid=None, thingtoquery=None):
        base_query = where_clause = where_clause1 = and_clause = where_clause2 = ''
        base_query = f"""
            SELECT ca. constituent_id, ca.award_id, c.constituent_name, a.award_name, e.description
            FROM constituent_award as ca
            LEFT JOIN constituent as c ON ca.constituent_id = c.constituent_id
            LEFT JOIN award as a ON ca.award_id = a.award_id
            LEFT JOIN event as e ON a.event_id = e.event_id
        """
        if constituentid or thingtoquery:
            where_clause = """
                WHERE
            """
        if constituentid:
            where_clause1 = f"""
                c.constituent_id={constituentid}
            """
        if constituentid and thingtoquery:
            and_clause = """
                AND
            """
        if thingtoquery:
            where_clause2 = f"""
                ( c.constituent_name LIKE '%{thingtoquery}%'
                OR a.award_name LIKE '%{thingtoquery}%')
            """
        
        final_query = base_query+where_clause+where_clause1+and_clause+where_clause2
        self.cursor.execute(final_query)
        result = self.cursor.fetchall()
        return result
    
    # ===========================================
    # Constituent Event
    # ===========================================

    def createConstituentEvent(self, constituent_id, event_id):
        constituent_id = self.formatforSQL(constituent_id)
        event_id = self.formatforSQL(event_id)
        query = f"""
            INSERT INTO constituent_event (constituent_id, event_id)
            VALUES ({constituent_id}, {event_id});
        """
        self.executeQuery(query)

    def readConstituentEvent(self, constituent_id, event_id):
        constituent_id = self.formatforSQL(constituent_id)
        event_id = self.formatforSQL(event_id)
        query = f"""
            SELECT * FROM constituent_event
            WHERE constituent_id={constituent_id} AND event_id={event_id};
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def deleteConstituentEvent(self, constituent_id, event_id):
        constituent_id = self.formatforSQL(constituent_id)
        event_id = self.formatforSQL(event_id)
        query = f"""
            DELETE FROM constituent_event
            WHERE constituent_id={constituent_id} AND event_id={event_id};
        """
        self.executeQuery(query)
    
    def listConstituentEventForTable(self, constituentid=None, thingtoquery=None):
        base_query = where_clause = where_clause1 = and_clause = where_clause2 = ''
        base_query = f"""
            SELECT ce.event_id, ce.constituent_id, e.description, c.constituent_name
            FROM constituent_event AS ce
            LEFT JOIN event AS e ON ce.event_id = e.event_id
            LEFT JOIN constituent AS c ON c.constituent_id = ce.constituent_id
        """
        if constituentid or thingtoquery:
            where_clause = " WHERE "
        if constituentid:
            where_clause1 = f"c.constituent_id={constituentid}"
        if constituentid and thingtoquery:
            and_clause = """
                AND
            """
        if thingtoquery:
            where_clause2 = f"(c.constituent_name LIKE '%{thingtoquery}%' OR e.description LIKE '%{thingtoquery}%')"
        
        final_query = base_query + where_clause + where_clause1 + and_clause + where_clause2
        self.cursor.execute(final_query)
        result = self.cursor.fetchall()
        return result

