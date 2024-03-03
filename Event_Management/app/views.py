from . import *
# from .__init__ import connection,cursor
from flask import jsonify
from Event_Management.database import *
from datetime import datetime
from flask_login import login_user,UserMixin, logout_user, login_required,current_user
app_views = Blueprint('app_views', __name__)
# User class
class User(UserMixin):
    def __init__(self, email):
        # fetch user
        user=check_user_type(connection,cursor,email)
        print("user",user,email)
        if(user.get("utype")!="Anonymous"):
            self.authenticated=True
            data=user["data"]
            self.id = data.get("email",None)
            self.name=data.get("name",None)
            self.dept=data.get("dept",None)
            self.phone_number=data.get("phone_number",None)
            self.email=data.get("email",None)
            if user["utype"]=="Student":
                self.roll_no=data.get("roll_no",None)
                self.college_name="IITKGP"
            if user["utype"]=="Participant":
                self.p_id=data.get("p_id",None)
                self.food_id=data.get("food_id",None)
                self.acc_id=data.get("acc_id",None)
                self.college_name=data.get("college_name",None)
            if user["utype"]=="Organiser":
                self.p_id=data.get("o_id",None)
                self.is_admin=data.get("can_create",None)
            self.utype=str(user["utype"]).lower()
        else:
            self.authenticated=False
            self.utype=str(user["utype"]).lower()
    @property       
    def is_authenticated(self):
        return self.authenticated
    @property       
    def num_registered(self):
        if self.utype=="student":
            success,reg=fetch_reg_events_of_student(self.roll_no)
            return len(reg)
        if self.utype=="participant":
            success,reg=fetch_reg_events_of_participant(self.p_id)
            return len(reg)
        # if self.utype=="organiser":
        #     fetch_reg_events_of_participant(self.p_id)
    @property       
    def num_completed_tasks(self):
        pass
    @property       
    def num_allotted_tasks(self):
        pass
    @property       
    def num_volunteered(self):
        pass
        
    def __str__(self):
        return self.name+"_"+self.utype




@app_views.route('/')
def index():
    return render_template('test.html', name='orld')
@app_views.route('/events')
def getEvents():
    # events=[
    #     {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
    #     {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
    #     {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
    #     {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
    #     {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
    #     {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        
    #     ]
    success,rows = fetch_all_events(connection,cursor)
    
    
    events_list = []
    for event_data in rows:
        dt_object = datetime.fromisoformat(str(event_data[1]))
        
        date = dt_object.date()
        time = dt_object.time()
        
        event_dict = {
            "e_id": event_data[0],
            "date": str(date),
            "time":str(time),
            "name": event_data[2],
            "type_event": event_data[3],
            "description": event_data[4],
            "first": event_data[5],
            "second": event_data[6],
            "third": event_data[7],
            "prize": event_data[8],
            "venue": event_data[9],
            "num_p": event_data[10]
        }
        events_list.append(event_dict)
    return render_template('events.html', name='events',events=events_list)
@app_views.route('/add-event', methods=['GET','POST'])
def addEvent():
    if request.method == 'POST':
        
        info = request.form
        name = info.get('name')
        date = info.get('date')
        time = info.get('time')
        description = info.get('description')
        tags = info.get('tags')
        venue = info.get('venue')
        prize = info.get('prize')
        type = info.get('type')
        num_p = 0
        success, error = insert_event(connection,cursor,date+" "+time,name,type,description,prize,venue,1,tags.split(","),num_p)
        # Check if the username already exists
        if success:
            return redirect(url_for('app_views.dashboardAdmin'))
    return render_template('addEvent.html', name='events')

@app_views.route('/event/<int:id>',methods=['GET'])
def eventDetails(id):
    # print("Hi ")
    success, rows = fetch_event_details(connection,cursor,id)
    success2,tags = fetch_all_tags_of_event(connection,cursor,id)
    
    dt_object = datetime.fromisoformat(str(rows[0][1]))
    
    date = dt_object.date()
    time = dt_object.time()
    
    tags_list=[]
    for tag in tags:
        tags_list.append(tag[0])
    
    event_dict = {
        'id': rows[0][0],
        'time': str(time),
        'date':str(date),
        'title': rows[0][2],
        'type': rows[0][3],
        'desc': rows[0][4],
        'first': rows[0][5],
        'second': rows[0][6],
        'third': rows[0][7],
        'prize': rows[0][8],
        'venue': rows[0][9],
        'tags' : tags_list,
        'num_p': rows[0][10]
    }
    
    roll_no=2130015
    
    count_allotted_query = """
        SELECT COUNT(*) FROM tasks
        WHERE roll_no = %s;
    """

    count_completed_query = """
        SELECT COUNT(*) FROM tasks
        WHERE roll_no = %s AND is_complete = 1;
    """

    cursor.execute(count_allotted_query, (roll_no,))
    count_allotted = cursor.fetchone()[0]  

    cursor.execute(count_completed_query, (roll_no,))
    count_completed = cursor.fetchone()[0]
    
    query = """
        SELECT task_description, is_complete
        FROM tasks
        WHERE roll_no = %s AND e_id = %s;
    """

    cursor.execute(query, (roll_no, id))
    tasks = cursor.fetchall()


    task_list = [{'description': task[0], 'is_complete': bool(task[1])} for task in tasks]
    
    success3,details = fetch_all_organisers_of_event(connection,cursor,id)

    organiser={"name":details[1],"role":"Events Head","email":details[0],"phone":details[2],"bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}    
    return render_template('eventDetails.html', name='events',event=event_dict,organiser=organiser,num_tasks_allotted=count_allotted,num_tasks_completed=count_completed,tasks=task_list)

@app_views.route('/event/<int:id>/volunteers')
def getVolunteers(id):
    
    volunteers=[
        {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
        {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
        {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
        {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
        {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
        {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
        ]
    organiser={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('volunteers.html',volunteers=volunteers,eventid=id)

@app_views.route('/profile')
def getProfile():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('profile.html',events=[])

@app_views.route('/organiser-events')
def getOrganiserEvents():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('organiser-events.html',events=[])

@app_views.route('/edit-profile')
def EditProfile():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('edit-profile.html',events=[])

@app_views.route('/register')
def registerUser():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('signup.html',events=[])


@app_views.route('/login',methods=["POST","GET"])
def loginUser():
    from Event_Management import load_user
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            print("cur",current_user)
            # Check if the username and password match
            user_dict=check_user_type(connection,cursor,email)
            utype=user_dict["utype"]
            if utype=="Anonymous":
                return redirect(url_for("signup"))
            elif utype=="Participant":
                success, row = check_participant_login(connection,cursor,email,password)       
            elif utype=="Student":
                success, row = check_student_login(connection,cursor,email,password)          
            elif utype=="Organiser":
                success, row = check_organiser_login(connection,cursor,email,password)
            # elif utype=="Admin":
                # success, row = check_admin_login(connection,cursor,email,password)
            
                
            if success:
                print("here")
                user = load_user(user_dict["data"]["email"])
                print("here",user)
 
                login_user(user)
                return redirect(url_for("app_views.dashboard"))


            else:
                # Authentication failed, render the login form with an error message
                return render_template('login.html', error='Invalid username or password')
    except Exception as e:
            print(str(e))
            return render_template('login.html', error=str(e))

    return render_template('login.html',events=[])

@app_views.route('/login/participant', methods=['POST'])
def loginParticipant():
    from Event_Management import load_user
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            print("cur",current_user)
            # Check if the username and password match
            user_dict=check_user_type(email)
            utype=user_dict["utype"]
            if utype!="Participant":
                return redirect(url_for("loginUser"))
            success, row = check_participant_login(connection,cursor,email,password)
            if success:
                user_dict={"name":"name","id":row[0],"utype":"participant"}
                user = load_user(user_dict["data"]["p_id"])
                # login_user(user)
                # user={"user":row,"is_active":True}
                # print(type(row),row,user)
                login_user(user_dict["data"])
                return redirect(url_for("app_views.dashboardParticipant"))

            else:
                # Authentication failed, render the login form with an error message
                return render_template('login.html', error='Invalid username or password')
    except Exception as e:
            print(str(e))
            return render_template('login.html', error=str(e))

         
@app_views.route('/login/student', methods=['POST'])
def loginStudent():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        
        # Check if the username and password match
        if True:
            return jsonify({'success':True,'user':{},'utype':'Participant'})

        success, row = check_student_login(connection,cursor,username,password)
        if success:
            # Authentication successful, redirect to a protected page
            return redirect(url_for('app_views.dashboardStudent'))
        else:
            # Authentication failed, render the login form with an error message
            return render_template('login.html', error='Invalid username or password')
    
@app_views.route('/login/organiser', methods=['POST'])
def loginOrganiser():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        print(request.form)

        success, row = check_organiser_login(connection,cursor,username,password)
        
        # Check if the username and password match
        if success:
            # Authentication successful, redirect to a protected page
            return redirect(url_for('app_views.dashboardOrganiser'))
        else:
            # Authentication failed, render the login form with an error message
            return render_template('login.html', error='Invalid username or password')
    
@app_views.route('/register/organiser', methods=['POST'])
def registerOrganiser():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        
        # Check if the username already exists
        user_exist=False
        if user_exist:
            return render_template('signup.html', error='Username already exists')
        
        # If username doesn't exist, add the user to the database
        info = request.form
        email = info.get('email')
        password = info.get('password')
        name = info.get('name')
        # TODO : Add phone number to the form
        phone_number = 9876543210
        can_create = 0
        success, error = insert_organiser(connection,cursor,email,password,name,phone_number,can_create)

        if success:
        # Registration successful, redirect to login page
            return redirect(url_for('app_views.loginUser'))
    
    # If GET request, render the registration form
    return render_template('signup.html', error=None)   

 
    
@app_views.route('/register/student', methods=['POST'])
def registerStudent():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        
        # Check if the username already exists
        user_exist=False
        if user_exist:
            return render_template('signup.html', error='User already exists')
        
        # If username doesn't exist, add the user to the database

        print(request.form)
        info = request.form
        name = info.get('name')
        email = info.get('email')
        dept = info.get('department')
        roll_no = info.get('rollno')
        phone_number = info.get('phone')
        password = info.get('password')

        success, error = insert_student(connection,cursor,roll_no,dept,name,phone_number,email,password)

        # Registration successful, redirect to login page
        if success:
            return redirect(url_for('app_views.loginUser'))
        
    
    # If GET request, render the registration form
    return render_template('signup.html', error=None)   

 
    
@app_views.route('/register/participant', methods=['POST'])
def registerParticipant():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check if the username already exists
        user_exist=False
        if user_exist:
            return render_template('signup.html', error='User already exists')
            # If username doesn't exist, add the user to the database
        info=request.form
        print(info)
        name = info.get('name')
        college_name = info.get('college_name')
        phone_number = info.get('phone')
        email = info.get('email')
        password = info.get('password')
        
        success, error = insert_participant(connection,cursor,name, college_name, phone_number, email, password)
        # Registration successful, redirect to login page
        print(success,error)
        if success:
            return redirect(url_for('app_views.loginUser'))
    
    # If GET request, render the registration form
    return render_template('signup.html', error=error)   

 
@app_views.route('/add-organiser')
def AddOrganiser():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('add-organiser.html',events=[])

@app_views.route('/facilities')
def facilities():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('logistics_admin.html',events=[])

@app_views.route('/plans')
def plans():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    accomodations=[
        {"title":"Basic","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
        {"title":"Premium","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
        {"title":"Standard","price":40,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
        {"title":"Economy","price":10,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
                   ]
    food=[
        {"title":"Basic","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
        {"title":"Premium","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
        {"title":"Standard","price":40,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
        {"title":"Economy","price":10,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
                   ]
    facilities=[
        {"title":"Bus Service","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
        {"title":"Toto Booking","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
        {"title":"Campus Tour","price":40,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
                   ]
    return render_template('plancards.html',accomodations=accomodations,food=food,facilities=facilities)

@app_views.route('/update-winners', methods=['POST'])
def updateWinners():
    if request.method == 'POST':
        # print(request.json)
        # TODO : Request.form
        info = request.json
        e_id = info.get('e_id')
        first = info.get('first')
        second = info.get('second')
        third = info.get('third')
        success, error = update_event_results(connection,cursor,e_id,first,second,third)
        if success:
            return jsonify({"message": "Winners updated successfully"}), 201
        else:
            return jsonify({"error": error}), 500
        


# Dashboards--------------------------
@app_views.route('/dashboard',methods=["POST","GET"])
def dashboard():
    try:
        print(current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for("app_views.loginUser"))
        elif current_user.utype=="participant":
            return render_template('dashboard_participant.html',user=current_user)
        elif current_user.utype=="student":
            return render_template('dashboard_student.html',user=current_user)
        elif current_user.utype=="organiser":
            return render_template('dashboard_organiser.html',user=current_user)
        elif current_user.utype=="admin":
            return render_template('dashboard_admin.html',user=current_user)
    except Exception as e:
            print(str(e))
            return redirect(url_for("app_views.loginUser"))
        

@app_views.route('/dashboard/student')
def dashboardStudent():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('dashboard_student.html',user=profile)

@app_views.route('/dashboard/organiser')
def dashboardOrganiser():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('dashboard_organiser.html',user=profile)

@app_views.route('/dashboard/participant')
def dashboardParticipant():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('dashboard_participant.html',user=profile)

@app_views.route('/dashboard/admin')
def dashboardAdmin():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('dashboard_admin.html',events=[])

@app_views.route('/dashboard/events')
def participantEvents():
    profile={"name":"Smarak K.","phone":9323232323,"bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    events=[
        {"title":"Event 1","organiser":profile,"venue":"Kalidas Audi","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","organiser":profile,"venue":"Kalidas Audi","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","organiser":profile,"venue":"Kalidas Audi","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","organiser":profile,"venue":"Kalidas Audi","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","organiser":profile,"venue":"Kalidas Audi","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","organiser":profile,"venue":"Kalidas Audi","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        
        ]
    return render_template('schedule.html',events=events)


@app_views.route('/add_task/<int:e_id>', methods=['GET','POST'])
def addTask(e_id):
    if request.method == 'POST':
        # Check if the username already exists
        return redirect(url_for('app_views.getVolunteers'))
    return redirect(url_for('app_views.getVolunteers'))
@app_views.route('/create_event_volunteer', methods=['POST'])

def create_event_volunteer():
    info = request.json
    print(request.json)
    e_id = info.get('e_id')
    try:
        print(current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for("app_views.loginUser"))
        elif current_user.utype=="participant":
            return redirect(url_for("app_views.dashboard"))
        elif current_user.utype=="student":
            success, error = insert_volunteer(connection,cursor,e_id,current_user.roll_no)
            if success:
                return jsonify({"message": "Volunteer added successfully"}), 201
            else:
                return jsonify({"error": error}), 500
        elif current_user.utype=="organiser":
            return redirect(url_for("app_views.dashboard"))
        elif current_user.utype=="admin":
            return redirect(url_for("app_views.dashboard"))
    except Exception as e:
            print(str(e))
            return redirect(url_for("app_views.loginUser"))

    
@app_views.route('/create_task_for_volunteer', methods=['POST'])
def create_task_for_volunteer():
    info = request.json
    roll_no = info.get('roll_no')
    description = info.get('description')

    success, error = insert_task(connection,cursor,roll_no,description)
    if success:
        return jsonify({"message": "Task added successfully"}), 201
    else:
        return jsonify({"error": error}), 500

@app_views.route('/register_for_event', methods=['POST'])
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

@app_views.route('/filter_event', methods=['POST'])
def filter_event():
    info = request.json
    tags = info.get('tags')

    events_data = fetch_event_for_filter(connection,cursor,tags)

    events_list = []
    for event_data in events_data:
        dt_object = datetime.fromisoformat(str(event_data[1]))
        
        date = dt_object.date()
        time = dt_object.time()
        event_dict = {
            "e_id": event_data[0],
            "date": str(date),
            "time":str(time),
            "name": event_data[2],
            "type_event": event_data[3],
            "description": event_data[4],
            "first": event_data[5],
            "second": event_data[6],
            "third": event_data[7],
            "prize": event_data[8],
            "venue": event_data[9],
            "num_p": event_data[10]
        }
        events_list.append(event_dict)

    return events_list
