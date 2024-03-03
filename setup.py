import psycopg2
from argparse import ArgumentParser

def establish_connection():
    #establishing the connection with the database and returning the connection object
    connection = psycopg2.connect(
        user = "postgres",
        password = "pass@1234",
        host = "localhost",
        database = "event_management"
        )
    return connection

def sample_data():
    try:
        connection = establish_connection()
        cursor = connection.cursor()
        if connection:
            query = "INSERT INTO student (roll_no,dept,name,phone_number,email,password) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (1, "CSE", "Aman", "1234567890", "hii@gmail.com", "123456"))
            cursor.execute(query, (2, "MAE", "Suman", "1234897890", "bye@gmail.com", "456789"))
            cursor.execute(query, (3, "ECE", "Raman", "9765409834", "hello@gmail.com", "789012"))

            query = "INSERT INTO organiser (o_id,email,password,name,phone_number,can_create) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (1, "org@gmail.com", "123456", "Suresh", "1234567890", 1))
            cursor.execute(query, (2, "org2@gmail.com", "456789", "Ramesh", "1234567890", 0))

            query = "INSERT INTO dbadmin (email,password) VALUES (%s, %s)"
            cursor.execute(query, ("admin@gmail.com","admin"))

            query = "INSERT INTO event (e_id,date_and_time,name,type_event,description,first,second,third,prize,venue,num_p) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (6, "2021-10-10 10:00:00", "KTJ", "Technical", "This is a technical event", None, None, None, 1000, "LHC", 0))
            cursor.execute(query, (7, "2021-10-11 10:00:00", "KTH", "Technical", "This is a technical event", None, None, None, 1000, "LBS", 0))
            cursor.execute(query, (8, "2021-10-12 10:00:00", "KTP", "Cultural", "This is a cultural event", None, None, None, 1000, "Pro", 0))

            connection.commit()
            cursor.close()
            connection.close()
            print("Sample data inserted successfully")

    except Exception as err:
        connection.rollback()
        print(f"Error: {err}")

def create_triggers():
        connection = establish_connection()
        cursor = connection.cursor()        
        if connection:
            cursor.execute("DROP TRIGGER IF EXISTS update_num_of_participants_trigger_accomodation ON participant")
            cursor.execute("DROP TRIGGER IF EXISTS update_num_of_participants_trigger_food ON participant")
            cursor.execute("DROP TRIGGER IF EXISTS update_winners_trigger ON event")
            cursor.execute("DROP TRIGGER IF EXISTS update_event_trigger ON event")
            cursor.execute("DROP TRIGGER IF EXISTS update_food_trigger ON food")
            cursor.execute("DROP TRIGGER IF EXISTS update_accomodation_trigger ON accomodation")
            cursor.execute("DROP TRIGGER IF EXISTS update_num_of_participants_trigger ON event_has_participant")

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

            trigger_function = """
                CREATE OR REPLACE FUNCTION update_winners()
                RETURNS TRIGGER AS
                $$
                BEGIN
                    IF TG_OP = 'UPDATE' THEN
                        INSERT INTO notifications (time_t, description)
                        VALUES (current_timestamp, 'Winnners for the event ' || NEW.name || ' are as follows: First: ' || NEW.first || ', Second: ' || NEW.second || ', Third: ' || NEW.third);
                    END IF;
                    RETURN NEW;
                END;
                $$
                LANGUAGE plpgsql;
            """
            cursor.execute(trigger_function)

            trigger = """
                CREATE TRIGGER update_winners_trigger
                AFTER UPDATE OF first, second, third ON event
                FOR EACH ROW
                EXECUTE FUNCTION update_winners();
            """
            cursor.execute(trigger)

            connection.commit()

            trigger_function = """
                CREATE OR REPLACE FUNCTION update_event()
                RETURNS TRIGGER AS
                $$
                BEGIN
                    IF TG_OP = 'UPDATE' THEN
                        INSERT INTO notifications (time_t, description)
                        VALUES (current_timestamp, 'Event ' || NEW.name || ' has been updated. New venue: ' || NEW.venue || ', New date and time: ' || NEW.date_and_time);
                    END IF;
                    RETURN NEW;
                END;
                $$
                LANGUAGE plpgsql;
            """
            cursor.execute(trigger_function)

            trigger = """
                CREATE TRIGGER update_event_trigger
                AFTER UPDATE OF venue, date_and_time ON event
                FOR EACH ROW
                EXECUTE FUNCTION update_event();
            """
            cursor.execute(trigger)

            connection.commit()

            trigger_function = """
                CREATE OR REPLACE FUNCTION update_food()
                RETURNS TRIGGER AS
                $$
                BEGIN
                    IF TG_OP = 'UPDATE' THEN
                        INSERT INTO notifications (time_t, description)
                        VALUES (current_timestamp, 'Food plan ' || NEW.food_type || ' has been updated. New price: ' || NEW.price);
                    END IF;
                    RETURN NEW;
                END;
                $$
                LANGUAGE plpgsql;
            """
            cursor.execute(trigger_function)

            trigger = """
                CREATE TRIGGER update_food_trigger
                AFTER UPDATE OF price ON food
                FOR EACH ROW
                EXECUTE FUNCTION update_food();
            """
            cursor.execute(trigger)

            connection.commit()

            trigger_function = """
                CREATE OR REPLACE FUNCTION update_accomodation()
                RETURNS TRIGGER AS
                $$
                BEGIN
                    IF TG_OP = 'UPDATE' THEN
                        INSERT INTO notifications (time_t, description)
                        VALUES (current_timestamp, 'Accomodation plan ' || NEW.name || ' has been updated. New price: ' || NEW.price);
                    END IF;
                    RETURN NEW;
                END;
                $$
                LANGUAGE plpgsql;
            """
            cursor.execute(trigger_function)

            trigger = """
                CREATE TRIGGER update_accomodation_trigger
                AFTER UPDATE OF price ON accomodation
                FOR EACH ROW
                EXECUTE FUNCTION update_accomodation();
            """
            cursor.execute(trigger)

            connection.commit()

            query = """
                CREATE OR REPLACE FUNCTION update_num_of_participants()
                RETURNS TRIGGER AS
                $$
                BEGIN
                    IF TG_OP = 'INSERT' THEN
                        UPDATE event
                        SET num_p = num_p + 1
                        WHERE e_id = NEW.e_id;
                    END IF;
                    RETURN NEW;
                END;
                $$
                LANGUAGE plpgsql;
            """

            cursor.execute(query)

            query = """
                CREATE TRIGGER update_num_of_participants_trigger
                AFTER INSERT ON event_has_participant
                FOR EACH ROW
                EXECUTE FUNCTION update_num_of_participants();
            """

            cursor.execute(query)
            connection.commit()

            print("Triggers created successfully")
            cursor.close()
            connection.close()

def main():
    try:
        connection = establish_connection()
        cursor = connection.cursor()        
        if connection:
            query = "drop table accomodation, food, participant, student, event, event_has_volunteer, event_has_tag, organiser, event_has_organiser, dbadmin, event_has_participant, notifications, tasks;"
            cursor.execute(query)
            
            query = """
                create table accomodation(
                    acc_id int primary key,
                    price int,
                    days int,
                    name varchar(50),
                    description text,
                    num_of_participants int
                );
            """
            cursor.execute(query)
            
            
            query = """
                create table food(
                    food_id int primary key,
                    name varchar(50),
                    type varchar(10),
                    price int,
                    days int,
                    description text,
                    num_of_participants int,
                    CONSTRAINT type_check CHECK (type IN ('Veg', 'NonVeg'))
                );
            """
            
            cursor.execute(query)
            
                    
            query = """
                create table participant(
                    p_id int primary key,
                    name varchar(50),
                    college_name varchar(50),
                    phone_number char(10),
                    email varchar(255),
                    password varchar(50),
                    acc_id int,
                    food_id int,
                    foreign key (acc_id) references accomodation(acc_id),
                    foreign key (food_id) references food(food_id)
                );
            """
            cursor.execute(query)
            
            
            query="""
                create table student(
                    roll_no int primary key,
                    dept varchar(50),
                    name varchar(50),
                    phone_number char(10),
                    email varchar(255),
                    password varchar(50)
                );
            """
            
            cursor.execute(query)
            
            query = """
                create table event(
                    e_id int primary key,
                    date_and_time timestamp,
                    name varchar(50),
                    type_event varchar(50),
                    description text,
                    first varchar(50),
                    second varchar(50),
                    third varchar(50),
                    prize int,
                    venue varchar(100),
                    num_p int
                );
            """
            
            cursor.execute(query)
            
            
            query = """
                create table event_has_volunteer(
                    e_id int references event(e_id), roll_no int references
                    student(roll_no), primary key (e_id,roll_no)
                );
            """
            
            cursor.execute(query)
            
            
            query = """
                create table event_has_tag(
                    e_id int references event(e_id),
                    tag varchar(50),
                    primary key (e_id,tag)
                );
            """
            
            cursor.execute(query)
            
            
            query = """
                create table organiser(
                    o_id int primary key,
                    email varchar(255),
                    password varchar(50),
                    name varchar(50),
                    phone_number char(10),
                    can_create int
                );
            """
            
            cursor.execute(query)
            
            
            
            query = """
                create table event_has_organiser(
                    e_id int references event(e_id), o_id int references
                    organiser(o_id), primary key (e_id,o_id)
                );
            """
            
            cursor.execute(query)
            
            
            query = """
                create table dbadmin(
                    email varchar(255) primary key,
                    password varchar(50)
                );
            """
            
            cursor.execute(query)
            
            
            query = """
                create table event_has_participant(
                    e_id int references event(e_id),
                    type varchar(50),
                    id int,
                    CONSTRAINT type_check CHECK (type IN ('Student', 'Participant')),
                    primary key (e_id,type,id)
                );
            """
            
            cursor.execute(query)
            
            
            query = """
                create table notifications(
                    time_t timestamp,
                    description text,
                    primary key(time_t,description)                    
                );
            """
            
            cursor.execute(query)
            
            
            query = """
                create table tasks(
                    task_id int primary key,
                    task_description text,
                    e_id int references event(e_id), roll_no int references
                    student(roll_no),
                    is_complete int
                );
            """

            
            cursor.execute(query)
            connection.commit()
            
            cursor.close()
            connection.close()
            print("Conection to database closed")
    except Exception as err:
        connection.rollback()
        print(f"Error: {err}")

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--create_triggers", action="store_true", help="Create triggers for the database")
    parser.add_argument("--sample_data", action="store_true", help="Insert sample data into the database")
    args = parser.parse_args()
    if args.create_triggers:
        create_triggers()
    elif args.sample_data:
        sample_data()
    else:
        main()