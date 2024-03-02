import psycopg2

def establish_connection():
    #establishing the connection with the database and returning the connection object
    connection = psycopg2.connect(
        user = "21CS30043",
        password = "21CS30043",
        host = "10.5.18.71",
        database = "21CS30043"
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

    except Exception as err:
        connection.rollback()
        print(f"Error: {err}")

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
                    type varchar(10),
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
                    first int,
                    second int,
                    third int,
                    prize int,
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
                    task_description text,
                    e_id int references event(e_id), roll_no int references
                    student(roll_no), primary key (e_id,roll_no,task_description),
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
    main()