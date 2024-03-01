from backend import connection,cursor

def insert_participant(name, college_name, phone_number, email, password):
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

def insert_student(roll_no,dept,name,phone_number,email,password):
    try:
        cursor.execute("INSERT INTO student (roll_no,dept,name,phone_number,email,password) VALUES (%s, %s, %s, %s, %s, %s)",
                    (roll_no,dept,name,phone_number,email,password))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
    
def insert_organiser(email,password,name,phone_number):
    try:
        cursor.execute("SELECT COALESCE(MAX(o_id), 0) + 1 FROM organiser")
        o_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO organiser (o_id, email, password, name, phone_number) VALUES (%s, %s, %s, %s, %s)",
                    (o_id,email,password,name,phone_number))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)
    
def fetch_all_events():
    try:
        cursor.execute("SELECT * FROM event;")
        rows = cursor.fetchall()
        return True,rows
    
    except Exception as e:
        return False,str(e)
    