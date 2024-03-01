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
    

def insert_event(date_time,name,description,venue):
    try:
        cursor.execute("SELECT COALESCE(MAX(e_id), 0) + 1 FROM event")
        e_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO event (e_id, date_and_time, name, description, first, second, third, venue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (e_id, date_time, name, description, None, None, None, venue))
        connection.commit()
        return True, None
    except Exception as e:
        connection.rollback()
        return False, str(e)