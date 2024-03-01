import psycopg2
from flask import Flask, request, jsonify
from database import *

app = Flask(__name__)

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
 



@app.route('/create_participant', methods=['POST'])
def create_participant():
        info=request.json
        name = info.get('name')
        college_name = info.get('college_name')
        phone_number = info.get('phone_number')
        email = info.get('email')
        password = info.get('password')
        success, error = insert_participant(name, college_name, phone_number, email, password)
                
        if success:
            return jsonify({"message": "Participant added successfully"}), 201
        else:
            return jsonify({"error": error}), 500
            

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

def create_event(info):
    
    try:
        e_id = info.get('e_id')
        date_and_time = info.get('date_and_time')
        name = info.get('name')
        description = info.get('description')
        first = info.get('first')
        second = info.get('second')
        third = info.get('third')
        venue = info.get('venue')

        query = """
            INSERT INTO event (e_id, date_and_time, name, description, first, second, third, venue)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (e_id, date_and_time, name, description, first, second, third, venue))
        
    except Exception as err:
        connection.rollback()
        print(f"Error while inserting event data: {err}")
        

def create_event_volunteer(info):
    try:
        e_id = info.get('e_id')
        roll_no = info.get('roll_no')
        
        query = """
            INSERT INTO event_has_volunteer (e_id, roll_no)
            VALUES (%s, %s)
        """
        cursor.execute(query, (e_id, roll_no))
        connection.commit()
        
    except:
        connection.rollback()
        print(f"Error while inserting volunteer data: {err}")
        
@app.route('/create_accommodation', methods=['POST'])
def create_accomodation():
    try:
        info=request.json
        acc_id = info.get('acc_id')
        price = info.get('price')
        days = info.get('days')
        name = info.get('name')
        num_of_participants = info.get('num_of_participants')

        query = """
            INSERT INTO accommodation (acc_id, price, days, name, num_of_participants)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (acc_id, price, days, name, num_of_participants))
        
        connection.commit()
        return jsonify({'message': 'Accommodation entry created successfully.'})
    
    except Exception as err:
        connection.rollback()
        return jsonify({'error': str(err)})  
    
      
def create_food(info):
    try:
        food_id=info.get('food_id')
        food_type=info.get('food_type')
        days=info.get('days')
        description=info.get('description')
        num_of_participants=info.get('num_of_participants')   
        query = """
            INSERT INTO food (food_id, type, days, description, num_of_participants)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (food_id, food_type, days, description, num_of_participants))
        connection.commit()
        print("Food data inserted successfully.")

    except Exception as err:
        connection.rollback()
        print(f"Error while inserting food data: {err}")



def create_task_for_volunteer():
    
    pass



@app.route('/fetch_accommodation_plans', methods=['GET'])
def fetch_accomodation_plans():
    try:
        cursor.execute("SELECT * FROM accommodation")
        accommodation_data = cursor.fetchall()

        accommodation_list = []
        for row in accommodation_data:
            accommodation_dict = {
                'acc_id': row[0],
                'price': row[1],
                'days': row[2],
                'name': row[3],
            }
            accommodation_list.append(accommodation_dict)
            
        return jsonify({'message':accommodation_list})

    except Exception as err:
        return jsonify({'error': str(err)})
    

@app.route('/fetch_food_plans', methods=['GET'])
def fetch_food_plans():
    try:
        cursor.execute("SELECT * FROM food")
        food_data = cursor.fetchall()

        food_list = []
        for row in food_data:
            food_dict = {
                'acc_id': row[0],
                'price': row[1],
                'days': row[2],
                'name': row[3],
            }
            food_list.append(food_dict)
            
        return jsonify({'message':food_list})

    except Exception as err:
        return jsonify({'error': str(err)})
    

@app.route('/event_volunteers/<int:e_id>', methods=['GET'])
def fetch_volunteers_of_event(e_id):
    try:
        cursor.execute("""
            SELECT s.roll_no, s.name, s.dept, s.phone_number, s.email
            FROM student s
            NATURAL JOIN event_has_volunteer ev
            WHERE ev.e_id = %s
        """, (e_id,))
        volunteers_data = cursor.fetchall()

        volunteers_list = []
        for row in volunteers_data:
            volunteer_dict = {
                'roll_no': row[0],
                'name': row[1],
                'dept': row[2],
                'phone_number': row[3],
                'email': row[4]
            }
            volunteers_list.append(volunteer_dict)

        return jsonify({'message':volunteers_list,'status':200})
    except Exception as err:
        return jsonify({'message': str(err),'status':500})


@app.route('/organiser_events/<int:o_id>', methods=['GET'])
def fetch_events_of_organiser(o_id):
    try:
        cursor.execute("""
            SELECT e.e_id, e.name, e.date_and_time, e.venue
            FROM event e
            NATURAL JOIN event_has_organiser eo
            WHERE eo.o_id = %s
        """, (o_id,))
        
        events_data = cursor.fetchall()

        events_list = []
        for row in events_data:
            event_dict = {
                'e_id': row[0],
                'name': row[1],
                'date_and_time': row[2],
                'venue': row[3]
            }
            events_list.append(event_dict)

        return jsonify({'message':events_list})

    except Exception as err:
        return jsonify({'error': str(err)})


@app.route('/volunteered_events/<int:roll_no>', methods=['GET'])
def fetch_events_of_volunteer(roll_no):
    try:
        cursor.execute("""
            SELECT e.e_id, e.name, e.date_and_time, e.venue
            FROM event e
            NATURAL JOIN event_has_volunteer ev
            WHERE ev.roll_no = %s
        """, (roll_no,))
        events_data = cursor.fetchall()

        events_list = []
        for row in events_data:
            event_dict = {
                'e_id': row[0],
                'name': row[1],
                'date_and_time': row[2],
                'venue': row[3]
            }
            events_list.append(event_dict)

        return jsonify({'message':events_list})

    except Exception as err:
        return jsonify({'error': str(err)})


# @app.route('/your_events/<string:type_of_p>/<int:id>', methods=['GET'])
# def fetch_events_of_participant(id,type_of_p):
#     try:
        
#         if type_of_p=='Student':
#             cursor.execute("""
#                 SELECT e.e_id, e.name, e.date_and_time, e.venue
#                 FROM event e
#                 JOIN event_has_participant ep ON e.e_id = ep.e_id
#                 WHERE ep.type = 'Participant' AND ep.id = %s
#             """, (participant_id))
#             events_data = cursor.fetchall()

#             # Convert the fetched data into a list of dictionaries
#             events_list = []
#             for row in events_data:
#                 event_dict = {
#                     'e_id': row[0],
#                     'name': row[1],
#                     'date_and_time': row[2],
#                     'venue': row[3]
#                 }
#                 events_list.append(event_dict)

#             # Close the cursor and connection
#             cursor.close()
#             connection.close()

#             # Return the list of events as JSON response
#             return jsonify(events_list)
            
#         elif type_of_p=='Participant':
#             pass
        
#         else:
#             return jsonify({'error','No such type'})

#     except Exception as err:
#         return jsonify({'error': str(err)})

def fetch_tasks_for_volunteer():
    pass



# participant_data = {
#     "p_id": 1,
#     "name": "Random",
#     "college_name": "ExampleUniversity",
#     "phone_number": "1234567890",
#     "email": "john@example.com",
#     "password": "password123",
#     "acc_id": None,
#     "food_id": None
# }
# create_account_participant(participant_data)


# student_data = {
#     "roll_no": 101,
#     "dept": "Computer Science",
#     "name": "John Doe",
#     "phone_number": "1234567890",
#     "email": "john@example.com",
#     "password": "password123"
# }
# create_acc_student(student_data)

    
# organiser_data = {
#     "o_id": 1,
#     "email": "organiser@example.com",
#     "password": "password123",
#     "name": "Organiser Name",
#     "phone_number": "1234567890"
# }
# create_acc_organiser(organiser_data)


if __name__ == '__main__':
    app.run(debug=True)
