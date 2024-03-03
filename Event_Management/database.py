def insert_participant(connection,cursor,name, college_name, phone_number, email, password):
    try:
        cursor.execute("SELECT COALESCE(MAX(p_id), 0) + 1 FROM participant")
        p_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO participant (p_id, name, college_name, phone_number, email, password, acc_id, food_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (p_id, name, college_name, phone_number, email, password, None, None))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
    

def insert_event(connection,cursor,date_time,name,type,description,prize,venue,o_id,tags):
    try:
        cursor.execute("SELECT COALESCE(MAX(e_id), 0) + 1 FROM event")
        e_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO event (e_id, date_and_time, name, type_event, description, first, second, third, prize, venue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (e_id, date_time, name,type,description,None,None,None,prize,venue))
        
        cursor.execute("INSERT INTO event_has_organiser (e_id, o_id) VALUES (%s, %s)", (e_id, o_id))

        for tag in tags:
            cursor.execute("INSERT INTO event_has_tag (e_id, tag) VALUES (%s, %s)", (e_id, tag))
        connection.commit()
        
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)

def insert_student(connection,cursor,roll_no,dept,name,phone_number,email,password):
    try:
        cursor.execute("INSERT INTO student (roll_no,dept,name,phone_number,email,password) VALUES (%s, %s, %s, %s, %s, %s)",
                    (roll_no,dept,name,phone_number,email,password))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
    
def insert_organiser(connection,cursor,email,password,name,phone_number,can_create):
    try:
        cursor.execute("SELECT COALESCE(MAX(o_id), 0) + 1 FROM organiser")
        o_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO organiser (o_id, email, password, name, phone_number,can_create) VALUES (%s, %s, %s, %s, %s,%s)",
                    (o_id,email,password,name,phone_number,can_create))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
    
    
def insert_volunteer(connection,cursor,e_id,roll_no):
    try:
        cursor.execute("INSERT INTO event_has_volunteer (e_id,roll_no) VALUES (%s, %s)",
                    (e_id,roll_no))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)

def insert_accomodation(connection,cursor,price,days,name):
    try:
        cursor.execute("SELECT COALESCE(MAX(acc_id), 0) + 1 FROM accomodation")
        acc_id = cursor.fetchone()[0]
        cursor.execute("""INSERT INTO accomodation (acc_id, price, days, name, num_of_participants) 
                       VALUES (%s, %s, %s, %s, %s)""",(acc_id, price, days, name, 0))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
    
def insert_food(connection,cursor,food_type,days,description):
    try:
        cursor.execute("SELECT COALESCE(MAX(food_id), 0) + 1 FROM food")
        food_id = cursor.fetchone()[0]
        cursor.execute("""
        INSERT INTO food (food_id, type, days, description, num_of_participants)
        VALUES (%s, %s, %s, %s, %s)
        """,(food_id, food_type, days, description, 0))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
    
def check_participant_login(connection,cursor,email,password):
    try:
        cursor.execute("SELECT * FROM participant WHERE email = %s AND password = %s", (email, password))
        row = cursor.fetchone()
        if row:
            return True, row
        else:
            return False, None
    except Exception as e:
        return False, str(e)

def check_student_login(connection,cursor,roll_no,password):
    try:
        cursor.execute("SELECT * FROM student WHERE roll_no = %s AND password = %s", (roll_no, password))
        row = cursor.fetchone()
        if row:
            return True, row
        else:
            return False, None
    except Exception as e:
        return False, str(e)

def check_organiser_login(connection,cursor,email,password):
    try:
        cursor.execute("SELECT * FROM organiser WHERE email = %s AND password = %s", (email, password))
        row = cursor.fetchone()
        if row:
            return True, row
        else:
            return False, None
    except Exception as e:
        return False, str(e)
        
def fetch_all_events(connection,cursor):
    try:
        cursor.execute("SELECT e_id,date_and_time,name,type_event,description,first,second,third,prize,venue,num_p FROM event;")
        rows = cursor.fetchall()
        return True,rows
    
    except Exception as e:
        return False,str(e)
    
def fetch_event_details(connection,cursor,e_id):
    try:
        cursor.execute("SELECT e_id,date_and_time,name,type_event,description,first,second,third,prize,venue FROM event where e_id = %s",(e_id,))
        rows = cursor.fetchall()
        return True,rows
    
    except Exception as e:
        return False,str(e)
    
def fetch_all_tags_of_event(connection,cursor,id):
    try:
        cursor.execute("SELECT tag FROM event_has_tag where e_id=%s",(id,))
        rows=cursor.fetchall()
        return True,rows
    except Exception as e:
        return False,str(e)
    
def fetch_all_organisers_of_event(connection,cursor,id):
    try:
        cursor.execute("SELECT email,name,phone_number FROM event_has_organiser NATURAL JOIN organiser where e_id=%s",(id,))
        rows=cursor.fetchall()
        return True,rows[0]
    except Exception as e:
        return False,str(e)
    
    
    
    
def fetch_all_acc_plans(connection,cursor):
    try:
        cursor.execute("SELECT * FROM accomodation")
        rows=cursor.fetchall()
        return True,rows
    
    except Exception as e:
        return False,str(e)
    
def fetch_all_food_plans(connection,cursor):
    try:
        cursor.execute("SELECT * FROM food")
        rows=cursor.fetchall()
        return True,rows
    
    except Exception as e:
        return False,str(e)
    
def fetch_all_volunteers_of_event(connection,cursor,e_id):
    try:
        cursor.execute("""
            SELECT s.roll_no, s.name, s.dept, s.phone_number, s.email
            FROM student s
            NATURAL JOIN event_has_volunteer ev
            WHERE ev.e_id = %s
        """, (e_id,))
        rows=cursor.fetchall()
        return True,rows

    except Exception as e:
        return False,str(e)
    
def fetch_all_events_of_organiser(connection,cursor,o_id):
    try:
        cursor.execute(
            """
            SELECT e.e_id, e.name, e.date_and_time, e.venue
            FROM event e
            NATURAL JOIN event_has_organiser eo
            WHERE eo.o_id = %s
            """, (o_id,)
        )
        rows=cursor.fetchall()
        return True,rows

    except Exception as e:
        return False,str(e)

def fetch_all_events_of_volunteer(connection,cursor,roll_no):
    try:
        cursor.execute("""
            SELECT e.e_id, e.name, e.date_and_time, e.venue
            FROM event e
            NATURAL JOIN event_has_volunteer ev
            WHERE ev.roll_no = %s
        """, (roll_no,))
        rows=cursor.fetchall()
        return True,rows

    except Exception as e:
        return False,str(e)

def fetch_reg_events_of_student(connection,cursor,id):
    try:
        cursor.execute("""
            SELECT e.e_id, e.name, e.date_and_time, e.venue
            FROM event e
            JOIN event_has_participant ep ON e.e_id = ep.e_id
            WHERE ep.type = 'Student' AND ep.id = %s
        """, (id,))
        rows=cursor.fetchall()
        return True,rows

    except Exception as e:
        return False,str(e)

def fetch_reg_events_of_participant(connection,cursor,id):
    try:
        cursor.execute("""
            SELECT e.e_id, e.name, e.date_and_time, e.venue
            FROM event e
            JOIN event_has_participant ep ON e.e_id = ep.e_id
            WHERE ep.type = 'Participant' AND ep.id = %s
        """, (id,))
        rows=cursor.fetchall()
        return True,rows

    except Exception as e:
        return False,str(e)
    
def register_participant(connection,cursor,e_id,participant_id,participant_type):
    try:
        cursor.execute("""
            INSERT INTO event_has_participant (e_id, type, id)
            VALUES (%s, %s, %s)
        """, (e_id, participant_type, participant_id))

        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)

def update_accomodation(connection,cursor,p_id,acc_id):     #if participant not in table
    try:
        cursor.execute("""
            UPDATE participant
            SET acc_id = %s
            WHERE p_id = %s            
        """,(acc_id, p_id))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
        
def update_food(connection,cursor,p_id,food_id):     #if participant not in table
    try:
        cursor.execute("""
            UPDATE participant
            SET food_id = %s
            WHERE p_id = %s            
        """,(food_id, p_id))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
    
def update_event_results(connection,cursor,e_id,first,second,third):
    try:
        print(e_id,first,second,third)
        cursor.execute("""
            UPDATE event
            SET first = %s, second = %s, third = %s
            WHERE e_id = %s
        """,(first,second,third,e_id))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
    
def update_event_details(connection,cursor,e_id,venue,date_time):
    try:
        cursor.execute("""
            UPDATE event
            SET venue = %s, date_and_time = %s
            WHERE e_id = %s
        """,(venue,date_time,e_id))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
    
def insert_task(connection,cursor,roll_no,description):
    try:
        cursor.execute("""
            INSERT INTO tasks (roll_no, task_description)
            VALUES (%s, %s)
        """,(roll_no,description))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
    

def fetch_task_of_volunter(connection,cursor,roll_no):
    try:
        cursor.execute("""
            SELECT task_description
            FROM tasks
            WHERE roll_no = %s
        """,(roll_no,))
        rows=cursor.fetchall()
        return True,rows
    
    except Exception as e:
        connection.rollback()
        return False, str(e)
    
def check_duplicate_username_participant(connection,cursor,email):
    try:
        query = """
            SELECT EXISTS (
                SELECT 1
                FROM participant
                WHERE email = %s
            );
        """

        cursor.execute(query, (email,))
        exists = cursor.fetchone()[0]
        
        return True,exists
    except Exception as e:
        return False,str(e)     
   
def check_duplicate_username_student(connection,cursor,email):
    try:
        query = """
            SELECT EXISTS (
                SELECT 1
                FROM student
                WHERE email = %s
            );
        """

        cursor.execute(query, (email,))
        exists = cursor.fetchone()[0]
        
        return True,exists
    except Exception as e:
        return False,str(e) 
       
def check_duplicate_username_organiser(connection,cursor,email):
    try:
        query = """
            SELECT EXISTS (
                SELECT 1
                FROM organiser
                WHERE email = %s
            );
        """
        
        cursor.execute(query, (email,))
        exists = cursor.fetchone()[0]
        
        return True,exists
    except Exception as e:
        return False,str(e)        

def check_user_type(connection,cursor,email):

    cursor.execute(("SELECT roll_no,dept,name,phone_number,email FROM student WHERE email=%s"), (email,))
    student_data = cursor.fetchone()
    if student_data:
        student_dict = {
            "roll_no": student_data[0],
            "dept": student_data[1],
            "name": student_data[2],
            "phone_number": student_data[3],
            "email": student_data[4]
        }
        return {"utype":"Student","data":student_dict}

    cursor.execute(("SELECT p_id,name,college_name,phone_number,email,acc_id,food_id FROM participant WHERE email=%s"), (email,))
    participant_data = cursor.fetchone()
    if participant_data:
        participant_dict = {
            "p_id": participant_data[0],
            "name": participant_data[1],
            "college_name": participant_data[2],
            "phone_number": participant_data[3],
            "email": participant_data[4],
            "acc_id": participant_data[5],
            "food_id": participant_data[6]
        }
        return {"utype":"Participant","data":participant_dict}

    cursor.execute(("SELECT o_id,email,name,phone_number,can_create FROM organiser WHERE email=%s"), (email,))
    organiser_data = cursor.fetchone()
    if organiser_data:
        organiser_dict = {
            "o_id": organiser_data[0],
            "email": organiser_data[1],
            "name": organiser_data[2],
            "phone_number": organiser_data[3],
            "can_create": organiser_data[4]
        }
        return {"utype":"Organiser","data":organiser_dict}

    return {"utype":"Anonymous","data":None}
