drop table accomodation, food, participant, student, event, event_has_volunteer, event_has_tag, organiser, event_has_organiser, dbadmin, event_has_participant, notifications, tasks;

create table accomodation(
    acc_id int primary key,
    price int,
    days int,
    name varchar(50),
    num_of_participants int
);

create table food(
    food_id int primary key,
    type varchar(10),
    days int,
    description text,
    num_of_participant int,
    CONSTRAINT type_check CHECK (type IN ('Veg', 'NonVeg'))
);

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

create table student(
    roll_no int primary key,
    dept varchar(50),
    name varchar(50),
    phone_number char(10),
    email varchar(255),
    password varchar(50)
);

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

create table event_has_volunteer(
    e_id int references event(e_id), roll_no int references
    student(roll_no), primary key (e_id,roll_no)
);

create table event_has_tag(
    e_id int references event(e_id),
    tag varchar(50),
    primary key (e_id)
);

create table organiser(
    o_id int primary key,
    email varchar(255),
    password varchar(50),
    name varchar(50),
    phone_number char(10)
);

create table event_has_organiser(
    e_id int references event(e_id), o_id int references
    organiser(o_id), primary key (e_id,o_id)
);

create table dbadmin(
    email varchar(255) primary key,
    password varchar(50)
);

create table event_has_participant(
    e_id int references event(e_id),
    type varchar(50),
    id int,
    CONSTRAINT type_check CHECK (type IN ('Student', 'Participant')),
    primary key (e_id,type,id)
);

create table notifications(
    time_t timestamp,
    description text,
    primary key(time_t,description)                    
);

create table tasks(
    roll_no int,
    task_description text
);