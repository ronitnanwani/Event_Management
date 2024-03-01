import psycopg2
from flask import Flask, request, jsonify
from database import *

app = Flask(__name__)

try:
    connection = psycopg2.connect(
        user = "postgres",
        password = "pass@1234",
        host = "localhost",
        database = "event_management",
        port = "5432"
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
        success, error = insert_participant(connection,cursor,name, college_name, phone_number, email, password)
                
        if success:
            return jsonify({"message": "Participant added successfully"}), 201
        else:
            return jsonify({"error": error}), 500
            

@app.route('/create_event/<int:o_id>', methods=['POST'])
def create_event(o_id):
    info=request.json
    date_and_time = info.get('date_and_time')
    name = info.get('name')
    description = info.get('description')
    venue = info.get('venue')
    success, error = insert_event(connection,cursor,date_and_time, name, description, venue,o_id)
    if success:
        return jsonify({"message": "Event added successfully"}), 201
    else:
        return jsonify({"error": error}), 500
    

@app.route('/create_student', methods=['POST'])
def create_student():
    info=request.json
    roll_no = info.get('roll_no')
    dept = info.get('dept')
    name = info.get('name')
    phone_number = info.get('phone_number')
    email = info.get('email')
    password = info.get('password')
    
    success, error = insert_student(connection,cursor,roll_no,dept,name,phone_number,email,password)
    
    if success:
        return jsonify({"message": "Student added successfully"}), 201
    else:
        return jsonify({"error": error}), 500


@app.route('/create_organiser', methods=['POST'])
def create_organiser():
    info = request.json
    email = info.get('email')
    password = info.get('password')
    name = info.get('name')
    phone_number = info.get('phone_number')
    
    success, error = insert_organiser(connection,cursor,email,password,name,phone_number)

    if success:
        return jsonify({"message": "Organiser added successfully"}), 201
    else:
        return jsonify({"error": error}), 500
       

@app.route('/create_event_volunteer', methods=['POST'])
def create_event_volunteer():
    info = request.json
    e_id = info.get('e_id')
    roll_no = info.get('roll_no')
    
    success, error = insert_volunteer(connection,cursor,e_id,roll_no)

    if success:
        return jsonify({"message": "Volunteer added successfully"}), 201
    else:
        return jsonify({"error": error}), 500

        
@app.route('/create_accomodation', methods=['POST'])
def create_accomodation():
    info=request.json
    price = info.get('price')
    days = info.get('days')
    name = info.get('name')
    
    success, error = insert_accomodation(connection,cursor,price,days,name)

    if success:
        return jsonify({"message": "Accomodation added successfully"}), 201
    else:
        return jsonify({"error": error}), 500
    
 
@app.route('/create_food', methods=['POST'])
def create_food():
    info = request.json
    food_type=info.get('food_type')
    days=info.get('days')
    description=info.get('description')

    success, error = insert_food(connection,cursor,food_type,days,description)
    if success:
        return jsonify({"message": "Food added successfully"}), 201
    else:
        return jsonify({"error": error}), 500



def create_task_for_volunteer():
    pass



@app.route('/fetch_accomodation_plans', methods=['GET'])
def fetch_accomodation_plans():
    success, rows = fetch_all_acc_plans(connection,cursor)
    if success:
        
        if len(rows)==0:
            return jsonify({"message": "No accomodation plans Available"}), 201
        
        plan_list = []
        for plan in rows:
            plan_dict = {
                'acc_id': plan[0],
                'price': plan[1],
                'days': plan[2],
                'name': plan[3]
            }
            plan_list.append(plan_dict)
        return jsonify({"message": plan_list}), 201
    else:
        return jsonify({"error": rows}), 500

@app.route('/fetch_accomodation_plans_org', methods=['GET'])
def fetch_accomodation_plans_org():
    success, rows = fetch_all_acc_plans(connection,cursor)
    if success:
        
        if len(rows)==0:
            return jsonify({"message": "No accomodation plans Available"}), 201
        
        plan_list = []
        for plan in rows:
            plan_dict = {
                'acc_id': plan[0],
                'price': plan[1],
                'days': plan[2],
                'name': plan[3],
                'num_of_participants': plan[4]
            }
            plan_list.append(plan_dict)
        return jsonify({"message": plan_list}), 201
    else:
        return jsonify({"error": rows}), 500
        

@app.route('/fetch_food_plans', methods=['GET'])
def fetch_food_plans():
    success, rows = fetch_all_food_plans(connection,cursor)
    if success:
        
        if len(rows)==0:
            return jsonify({"message": "No food plans Available"}), 201
        
        plan_list = []
        for plan in rows:
            plan_dict = {
                'food_id': plan[0],
                'type': plan[1],
                'days': plan[2],
                'description': plan[3]
            }
            plan_list.append(plan_dict)
        return jsonify({"message": plan_list}), 201
    else:
        return jsonify({"error": rows}), 500


@app.route('/fetch_food_plans_org', methods=['GET'])
def fetch_food_plans_org():
    success, rows = fetch_all_food_plans(connection,cursor)
    if success:
        
        if len(rows)==0:
            return jsonify({"message": "No food plans Available"}), 201
        
        plan_list = []
        for plan in rows:
            plan_dict = {
                'food_id': plan[0],
                'type': plan[1],
                'days': plan[2],
                'description': plan[3],
                'num_of_participants': plan[4]
            }
            plan_list.append(plan_dict)
        return jsonify({"message": plan_list}), 201
    else:
        return jsonify({"error": rows}), 500


    
@app.route('/fetch_events',methods=['GET'])
def fetch_events():
    success, rows = fetch_all_events(connection,cursor)
    
    if success:
        
        if len(rows)==0:
            return jsonify({"message": "No events Available"}), 201
        
        event_list = []
        for event in rows:
            event_dict = {
                'e_id': event[0],
                'date_and_time': str(event[1]),
                'name': event[2],
                'description': event[3],
                'first': event[4],
                'second': event[5],
                'third': event[6],
                'venue': event[7]
            }
            event_list.append(event_dict)
        return jsonify({"message": event_list}), 201
    else:
        return jsonify({"error": rows}), 500
    


@app.route('/event_volunteers/<int:e_id>', methods=['GET'])
def fetch_volunteers_of_event(e_id):
    success, rows = fetch_all_volunteers_of_event(connection,cursor,e_id)
    
    if success:
        
        if len(rows)==0:
            return jsonify({"message": "No volunteers for this event"}), 201
        
        volunteers_list = []
        for row in rows:
            volunteer_dict = {
                'roll_no': row[0],
                'name': row[1],
                'dept': row[2],
                'phone_number': row[3],
                'email': row[4]
            }
            volunteers_list.append(volunteer_dict)

        return jsonify({"message": volunteers_list}), 201
    else:
        return jsonify({"error": rows}), 500


@app.route('/organiser_events/<int:o_id>', methods=['GET'])
def fetch_events_of_organiser(o_id):
    success, rows = fetch_all_events_of_organiser(connection,cursor,o_id)
    
    if success:
        
        if len(rows)==0:
            return jsonify({"message": "No events organised by you"}), 201
        
        events_list = []
        for row in rows:
            event_dict = {
                'e_id': row[0],
                'name': row[1],
                'date_and_time': row[2],
                'venue': row[3]
            }
            events_list.append(event_dict)
        return jsonify({"message": events_list}), 201
    
    else:
        return jsonify({"error": rows}), 500

@app.route('/volunteered_events/<int:roll_no>', methods=['GET'])
def fetch_events_of_volunteer(roll_no):
    success, rows = fetch_all_events_of_volunteer(connection,cursor,roll_no)
    
    if success:
        
        if len(rows)==0:
            return jsonify({"message": "You have not volunteered for any events"}), 201
        
        events_list = []
        for row in rows:
            event_dict = {
                'e_id': row[0],
                'name': row[1],
                'date_and_time': row[2],
                'venue': row[3]
            }
            events_list.append(event_dict)
        return jsonify({"message": events_list}), 201
    
    else:
        return jsonify({"error": rows}), 500


@app.route('/registered_events/<string:type_of_p>/<int:id>', methods=['GET'])
def fetch_events_of_participant(type_of_p,id):        
    if type_of_p=='Student':
        success,rows=fetch_reg_events_of_student(connection,cursor,id)
        if success:
            
            if len(rows)==0:
                return jsonify({"message": "You have not registered for any events"}), 201
            
            events_list = []
            for row in rows:
                event_dict = {
                    'e_id': row[0],
                    'name': row[1],
                    'date_and_time': row[2],
                    'venue': row[3]
                }
                events_list.append(event_dict)
            return jsonify({"message": events_list}), 201
        
        else:
            return jsonify({"error": rows}), 500
        
    elif type_of_p=='Participant':
        success,rows=fetch_reg_events_of_participant(connection,cursor,id)
        if success:
            
            if len(rows)==0:
                return jsonify({"message": "You have not registered for any events"}), 201
            
            events_list = []
            for row in rows:
                event_dict = {
                    'e_id': row[0],
                    'name': row[1],
                    'date_and_time': row[2],
                    'venue': row[3]
                }
                events_list.append(event_dict)
            return jsonify({"message": events_list}), 201
        
        else:
            return jsonify({"error": rows}), 500
    
    else:
        return jsonify({'error','No such type of registrant'}), 500


def fetch_tasks_for_volunteer():
    pass


@app.route('/register_for_event', methods=['POST'])
def register_for_event():
    info = request.json
    e_id = info.get('e_id')
    participant_id = info.get('id')
    participant_type = info.get('type')

    success,error=register_participant(connection,cursor,e_id, participant_id, participant_type)

    if success:
        return jsonify({"message": "Registered successfully"}), 201
    else:
        return jsonify({"error": error}), 500 
    
@app.route('/choose_accomodation', methods=['POST'])
def choose_accomodation():
    data = request.json
    p_id = data.get('p_id')
    acc_id = data.get('acc_id')
    
    success,error = update_accomodation(connection,cursor,p_id,acc_id)
    
    if success:
        return jsonify({"message": "Accomodation updated"}), 201
    else:
        return jsonify({"error": error}), 500 

@app.route('/choose_food', methods=['POST'])
def choose_food():
    data = request.json
    p_id = data.get('p_id')
    food_id = data.get('food_id')
    
    success,error = update_food(connection,cursor,p_id,food_id)
    
    if success:
        return jsonify({"message": "Food Plan updated"}), 201
    else:
        return jsonify({"error": error}), 500 

def create_trigger1():
    try:
        cursor.execute("DROP TRIGGER IF EXISTS update_num_of_participants_trigger_accomodation ON participant")

        trigger_function = """
            CREATE OR REPLACE FUNCTION update_num_of_participants_accomodation()
            RETURNS TRIGGER AS
            $$
            BEGIN
                IF TG_OP = 'UPDATE' THEN
                    IF OLD.acc_id IS NOT NULL AND NEW.acc_id IS NOT NULL AND OLD.acc_id <> NEW.acc_id THEN
                        UPDATE accomodation
                        SET num_of_participants = num_of_participants - 1
                        WHERE acc_id = OLD.acc_id;

                        UPDATE accomodation
                        SET num_of_participants = num_of_participants + 1
                        WHERE acc_id = NEW.acc_id;
                        
                    ELSIF OLD.acc_id IS NULL AND NEW.acc_id IS NOT NULL THEN
                        UPDATE accomodation
                        SET num_of_participants = num_of_participants + 1
                        WHERE acc_id = NEW.acc_id;

                    ELSIF OLD.acc_id IS NOT NULL AND NEW.acc_id IS NULL THEN
                        UPDATE accomodation
                        SET num_of_participants = num_of_participants - 1
                        WHERE acc_id = OLD.acc_id;
                    END IF;   
                END IF;
                RETURN NEW;
            END;
            $$
            LANGUAGE plpgsql;
        """
        cursor.execute(trigger_function)

        trigger = """
            CREATE TRIGGER update_num_of_participants_trigger_accomodation
            AFTER UPDATE OF acc_id ON participant
            FOR EACH ROW
            EXECUTE FUNCTION update_num_of_participants_accomodation();
        """
        cursor.execute(trigger)

        connection.commit()
        print("Trigger created successfully")

    except Exception as e:
        print("Error creating trigger:", e)

def create_trigger2():
    try:
        cursor.execute("DROP TRIGGER IF EXISTS update_num_of_participants_trigger_food ON participant")

        trigger_function = """
            CREATE OR REPLACE FUNCTION update_num_of_participants_food()
            RETURNS TRIGGER AS
            $$
            BEGIN
                IF TG_OP = 'UPDATE' THEN
                    IF OLD.food_id IS NOT NULL AND NEW.food_id IS NOT NULL AND OLD.food_id <> NEW.food_id THEN
                        UPDATE food
                        SET num_of_participants = num_of_participants - 1
                        WHERE food_id = OLD.food_id;

                        UPDATE food
                        SET num_of_participants = num_of_participants + 1
                        WHERE food_id = NEW.food_id;
                        
                    ELSIF OLD.food_id IS NULL AND NEW.food_id IS NOT NULL THEN
                        UPDATE food
                        SET num_of_participants = num_of_participants + 1
                        WHERE food_id = NEW.food_id;

                    ELSIF OLD.food_id IS NOT NULL AND NEW.food_id IS NULL THEN
                        UPDATE food
                        SET num_of_participants = num_of_participants - 1
                        WHERE food_id = OLD.food_id;
                    END IF;   
                END IF;
                RETURN NEW;
            END;
            $$
            LANGUAGE plpgsql;
        """
        cursor.execute(trigger_function)

        trigger = """
            CREATE TRIGGER update_num_of_participants_trigger_food
            AFTER UPDATE OF food_id ON participant
            FOR EACH ROW
            EXECUTE FUNCTION update_num_of_participants_food();
        """
        cursor.execute(trigger)

        connection.commit()
        print("Trigger created successfully")

    except Exception as e:
        print("Error creating trigger:", e)

# Updates num_of_participants whenever acc_id for any participant is changed
create_trigger1()
# Updates num_of_participants whenever food_id for any participant is changed
create_trigger2()


if __name__ == '__main__':
    app.run(debug=True)
