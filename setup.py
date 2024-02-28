import psycopg2

def establish_connection():
    #establishing the connection with the database and returning the connection object
    connection = psycopg2.connect(
        user = "postgres",
        password = "pass@1234",
        host = "localhost",
        database = "event_management"
        )
    return connection

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
                    num_of_participants int
                );
            """
            cursor.execute(query)
            
            
            query = """
                create table food(
                    food_id int primary key,
                    type varchar(10),
                    days int,
                    description text,
                    num_of_participant int,
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
                    foreign  key (food_id) references food(food_id)
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
                    description text,
                    first int,
                    second int,
                    third int,
                    venue varchar(100)
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
                    primary key (e_id)
                );
            """
            
            cursor.execute(query)
            
            
            query = """
                create table organiser(
                    o_id int primary key,
                    email varchar(255),
                    password varchar(50),
                    name varchar(50),
                    phone_number char(10)
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
                    roll_no int,
                    task_description text
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
    main()