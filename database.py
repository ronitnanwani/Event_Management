from Event_Management.backend import connection,cursor

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