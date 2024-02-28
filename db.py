import psycopg2

try:
    connection = psycopg2.connect(
        user = "postgres",
        password = "pass@1234",
        host = "localhost",
        database = "event_management"
    )
    cursor = connection.cursor()
except Exception as err:
    print(f"Error: {err}")
    
    

def create_account_participant(info):
        p_id = info.get('p_id')
        name = info.get('name')
        college_name = info.get('college_name')
        phone_number = info.get('phone_number')
        email = info.get('email')
        password = info.get('password')
        acc_id = info.get('acc_id')
        food_id = info.get('food_id')

        query = """
            INSERT INTO participant (p_id, name, college_name, phone_number, email, password, acc_id, food_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            cursor.execute(query, (p_id, name, college_name, phone_number, email, password, acc_id, food_id))
            connection.commit()
            print("Participant data inserted successfully.")
        except Exception as err:
            connection.rollback()
            print(f"Error while inserting participant data: {err}")
            

def create_acc_student(info):
    try:
        roll_no = info.get('roll_no')
        dept = info.get('dept')
        name = info.get('name')
        phone_number = info.get('phone_number')
        email = info.get('email')
        password = info.get('password')

        query = """
            INSERT INTO student (roll_no, dept, name, phone_number, email, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (roll_no, dept, name, phone_number, email, password))
        connection.commit()
        print("Student data inserted successfully.")

    except Exception as err:
        connection.rollback()
        print(f"Error while inserting student data: {err}")

def create_acc_organiser(info):
    try:
        o_id = info.get('o_id')
        email = info.get('email')
        password = info.get('password')
        name = info.get('name')
        phone_number = info.get('phone_number')

        query = """
            INSERT INTO organiser (o_id, email, password, name, phone_number)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (o_id, email, password, name, phone_number))
        
        connection.commit()
        print("Organiser data inserted successfully.")

    except Exception as err:
        connection.rollback()
        print(f"Error while inserting organiser data: {err}")

def create_event():
    pass

def create_event_volunteer():
    pass

def create_accomadation():
    pass

def create_food():
    pass

def create_task_for_volunteer():
    pass


def fetch_accomodation_plans():
    pass

def fecth_food_plans():
    pass

def fetch_volunteers_of_event():
    pass

def fetch_events_of_organiser():
    pass

def fetch_events_of_volunteer():
    pass

def fetch_events_of_participant():
    pass

def fetch_tasks_for_volunteer():
    pass



participant_data = {
    "p_id": 1,
    "name": "Random",
    "college_name": "ExampleUniversity",
    "phone_number": "1234567890",
    "email": "john@example.com",
    "password": "password123",
    "acc_id": None,
    "food_id": None
}
create_account_participant(participant_data)


student_data = {
    "roll_no": 101,
    "dept": "Computer Science",
    "name": "John Doe",
    "phone_number": "1234567890",
    "email": "john@example.com",
    "password": "password123"
}
create_acc_student(student_data)

    
organiser_data = {
    "o_id": 1,
    "email": "organiser@example.com",
    "password": "password123",
    "name": "Organiser Name",
    "phone_number": "1234567890"
}
create_acc_organiser(organiser_data)
