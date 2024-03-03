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
        self.name=""
        # print("user",user,email)
        if(user.get("utype")!="Anonymous"):
            self.authenticated=True
            data=user["data"]
            self.id = data.get("email",None)
            self.department=data.get("dept",None)
            self.phone_number=data.get("phone_number",None)
            self.email=data.get("email",None)
            if user["utype"]=="Student":
                self.roll_no=data.get("roll_no",None)
                self.college_name="IITKGP"
                self.name=data.get("name",None)

            if user["utype"]=="Participant":
                self.p_id=data.get("p_id",None)
                self.food_id=data.get("food_id",None)
                self.acc_id=data.get("acc_id",None)
                self.college_name=data.get("college_name",None)
                self.name=data.get("name",None)

            if user["utype"]=="Organiser":

                self.name=data.get("name",None)
                self.o_id=data.get("o_id",None)
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
            success,reg=fetch_reg_events_of_student(connection,cursor,self.roll_no)
            return len(reg)
        if self.utype=="participant":
            success,reg=fetch_reg_events_of_participant(connection,cursor,self.p_id)
            return len(reg)
        if self.utype=="organiser":
            success,reg=fetch_reg_events_of_organiser(connection,cursor,self.o_id)
            return len(reg)

    @property       
    def num_completed_tasks(self):
        if self.utype=="student":
            success,reg=fetch_completed_tasks_of_student(connection,cursor,self.roll_no)
            return len(reg)
        if self.utype=="participant":
            return 0
        if self.utype=="organiser":
            return 0

    @property       
    def num_allotted_tasks(self):
        if self.utype=="student":
            success,reg=fetch_alloted_tasks_of_student(connection,cursor,self.roll_no)
            return len(reg)
        if self.utype=="participant":
            return 0
        if self.utype=="organiser":
            return 0
    @property       
    def tasks(self):
        if self.utype=="student":
            success,reg=fetch_alloted_tasks_of_student(connection,cursor,self.roll_no)
            # Convert to list of dictionaries
            tasks_list=[]
            for task in reg:
                tasks_list.append({"id":task[2],"description":task[0],"is_complete":task[1],"event":{"name":task[3],"type":task[4]}})
            print("List of tasks ",tasks_list)
            return tasks_list
        if self.utype=="participant":
            return []
        if self.utype=="organiser":
            return []
    @property
    def num_volunteers(self):
        if self.utype=="student":
            success,reg=fetch_events_volunteered_by_student(connection,cursor,self.roll_no)
            return len(reg)
        if self.utype=="participant":
            return 0
        if self.utype=="organiser":
            return 0
    
        
    @property
    def events_registered(self):
        events_list=[]
        if self.utype=="student":
            success,reg=fetch_reg_events_of_student(connection,cursor,self.roll_no)
            # Convert to list of dictionaries
            events_list=[]
            for event in reg:
                dt_object = datetime.fromisoformat(str(event[1]))
                date = dt_object.date()
                time = dt_object.time()
                # print("Hello from here ")
                event_dict = {
                    "e_id": event[0],
                    "date": str(date),
                    "time":str(time),
                    "name": event[2],
                    "type_event": event[3],
                    "description": event[4],
                    "first": event[5],
                    "second": event[6],
                    "third": event[7],
                    "prize": event[8],
                    "venue": event[9],
                    "num_p": event[10]
                }
                success,org = fetch_organiser_of_event(connection,cursor,event[0])
                # success,org = fetch_organiser_of_event(connection,cursor,event[0])
                print("Hehe ",org[0],org[1])
                event_dict["organiser"]={"name":org[0],"phone":org[1]}
                events_list.append(event_dict)
        if self.utype=="participant":
            success,reg=fetch_reg_events_of_participant(connection,cursor,self.p_id)
            # Convert to list of dictionaries
            events_list=[]
            for event in reg:
                dt_object = datetime.fromisoformat(str(event[1]))
                date = dt_object.date()
                time = dt_object.time()
                event_dict = {
                    "e_id": event[0],
                    "date": str(date),
                    "time":str(time),
                    "name": event[2],
                    "type_event": event[3],
                    "description": event[4],
                    "first": event[5],
                    "second": event[6],
                    "third": event[7],
                    "prize": event[8],
                    "venue": event[9],
                    "num_p": event[10]
                }
                success,org = fetch_organiser_of_event(connection,cursor,event[0])
                # success,org = fetch_organiser_of_event(connection,cursor,event[0])
                print("Hehe ",org[0],org[1])
                event_dict["organiser"]={"name":org[0],"phone":org[1]}
                events_list.append(event_dict)
        if self.utype=="organiser":
            success,reg=fetch_reg_events_of_organiser(connection,cursor,self.o_id)
            # Convert to list of dictionaries
            events_list=[]
            for event in reg:
                dt_object = datetime.fromisoformat(str(event[1]))
                date = dt_object.date()
                time = dt_object.time()
                event_dict = {
                    "e_id": event[0],
                    "date": str(date),
                    "time":str(time),
                    "name": event[2],
                    "type_event": event[3],
                    "description": event[4],
                    "first": event[5],
                    "second": event[6],
                    "third": event[7],
                    "prize": event[8],
                    "venue": event[9],
                    "num_p": event[10]
                }
                success,org = fetch_organiser_of_event(connection,cursor,event[0])
                # success,org = fetch_organiser_of_event(connection,cursor,event[0])
                print("Hehe ",org[0],org[1])
                event_dict["organiser"]={"name":org[0],"phone":org[1]}
                events_list.append(event_dict)
        return events_list
    @property
    def events_volunteered(self):
        if self.utype=="student":
            success,reg=fetch_events_volunteered_by_student(connection,cursor,self.roll_no)
            # Convert to list of dictionaries
            events_list=[]
            for event in reg:
                dt_object = datetime.fromisoformat(str(event[1]))
                date = dt_object.date()
                time = dt_object.time()
                event_dict = {
                    "e_id": event[0],
                    "date": str(date),
                    "time":str(time),
                    "name": event[2],
                    "type_event": event[3],
                    "description": event[4],
                    "first": event[5],
                    "second": event[6],
                    "third": event[7],
                    "prize": event[8],
                    "venue": event[9],
                    "num_p": event[10]
                }
                events_list.append(event_dict)
            
            return events_list
        if self.utype=="participant":
            return []
        if self.utype=="organiser":
            return []
        else:
            return []
    @property
    def num_events_organised(self):
        if self.utype=="student":
            return 0
        if self.utype=="participant":
            return 0
        if self.utype=="organiser":
            success,reg=fetch_events_organised_by_organiser(connection,cursor,self.o_id)
            return len(reg)
        return 0
        
    @property
    def events_organised(self):
        if self.utype=="student":
            return []
        if self.utype=="participant":
            return []
        if self.utype=="organiser":
            success,reg=fetch_events_organised_by_organiser(connection,cursor,self.o_id)
            # Convert to list of dictionaries
            events_list=[]
            for event in reg:
                dt_object = datetime.fromisoformat(str(event[1]))
                date = dt_object.date()
                time = dt_object.time()
                event_dict = {
                    "e_id": event[0],
                    "date": str(date),
                    "time":str(time),
                    "name": event[2],
                    "type_event": event[3],
                    "description": event[4],
                    "first": event[5],
                    "second": event[6],
                    "third": event[7],
                    "prize": event[8],
                    "venue": event[9],
                    "num_p": event[10]
                }
                events_list.append(event_dict)
            return events_list
        return 0
        
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
        success2,tags = fetch_all_tags_of_event(connection,cursor,event_data[0])
        date = dt_object.date()
        time = dt_object.time()
        tags_list=[]
        for tag in tags:
            tags_list.append(tag[0])
        print(tags_list,"tags")
        is_registered=False
        is_volunteered=False
        if(current_user.is_authenticated):
            for item in current_user.events_registered:
                print(item)
                if(item["e_id"]==event_data[0]):
                    is_registered=True
                    break
            for item in current_user.events_volunteered:
                if(item["e_id"]==event_data[0]):
                    is_volunteered=True
                    break
            
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
            "num_p": event_data[10],
            "tags":tags_list,
            "is_registered":is_registered,
            "is_volunteered":is_volunteered,
        }
        
        events_list.append(event_dict)
    return render_template('events.html', name='events',events=events_list,user=current_user)
@app_views.route('/add-event', methods=['GET','POST'])
def addEvent(): 
    if not current_user.is_authenticated:
        return redirect(url_for("app_views.loginUser"))
    elif current_user.utype=="participant":
        return redirect(url_for("app_views.dashboard"))
    elif current_user.utype=="student":
        return redirect(url_for("app_views.dashboard"))  
    elif current_user.utype=="admin":
            return redirect(url_for("app_views.dashboard"))     
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
        try:
            print(current_user.is_authenticated)
            if current_user.utype=="organiser":
                success, error = insert_event(connection,cursor,date+" "+time,name,type,description,prize,venue,current_user.o_id,tags.split(","),num_p)
                print(success,error)
                if success:
                    return redirect(url_for('app_views.dashboard'))
            
        except Exception as e:
                print(str(e))
                return redirect(url_for("app_views.loginUser"))
    
    return render_template('addEvent.html', name='events')

@app_views.route('/event/<int:id>',methods=['GET'])
def eventDetails(id):
    # print("Hi ")
    success, rows = fetch_event_details(connection,cursor,id)
    success2,tags = fetch_all_tags_of_event(connection,cursor,id)
    success,accomodations = fetch_all_acc_plans(connection,cursor)
    accomodations_list=[]
    for accomodation in accomodations:
        accomodations_list.append({"title":accomodation[3],"price":accomodation[1],"desc":accomodation[4],"days":accomodation[2],"id":accomodation[0]})
    
    all_participants = get_participants_of_event(connection,cursor,id)
    
    print(all_participants)
    dt_object = datetime.fromisoformat(str(rows[0][1]))
    
    date = dt_object.date()
    time = dt_object.time()
    
    tags_list=[]
    for tag in tags:
        tags_list.append(tag[0])
    is_registered=False
    is_volunteered=False
    if(current_user.is_authenticated):
        for item in current_user.events_registered:
            if(item["e_id"]==rows[0][0]):
                is_registered=True
                break
        for item in current_user.events_volunteered:
            if(item["e_id"]==rows[0][0]):
                is_volunteered=True
                break
    is_organiser=False
    success3,details = fetch_all_organisers_of_event(connection,cursor,id)
    for item in details:
        if(item[0]==current_user.email):
            is_organiser=True
            break
    org_detail=details[0]
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
        'num_p': rows[0][10],
        "is_registered":is_registered,
        "is_volunteered":is_volunteered,
        "is_organiser":is_organiser
    }
    if current_user.utype=="student":
        roll_no=current_user.roll_no
        
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
    else:
        task_list=[]
        count_allotted=0
        count_completed=0
    print("participants",all_participants)
    organiser={"name":org_detail[1],"role":"Events Head","email":org_detail[0],"phone":org_detail[2],"bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}    
    return render_template('eventDetails.html', name='events',user=current_user,event=event_dict,organiser=organiser,num_tasks_allotted=count_allotted,num_tasks_completed=count_completed,tasks=task_list,accomodations=accomodations_list,participants=all_participants)

@app_views.route('/event/<int:id>/volunteers')
def getVolunteers(id):
    
    # volunteers=[
    #     {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
    #     {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
    #     {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
    #     {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
    #     {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
    #     {"name":"name 1","email":"email","phone":92321312312,"roll_no":213,"department":"CSE","num_tasks_allotted":20,"num_tasks_completed":10},
    #     ]

    success,rows = fetch_volunteers_of_event(connection,cursor,id)

    volunteers_list = []
    for volunteer in rows:
        user = User(volunteer[4])
        num_tasks_allotted = user.num_allotted_tasks
        num_tasks_completed = user.num_completed_tasks
        volunteer_dict = {
            "roll_no": volunteer[0],
            "name": volunteer[1],
            "department": volunteer[2],
            "phone": volunteer[3],
            "email": volunteer[4],
            "num_tasks_allotted": num_tasks_allotted,
            "num_tasks_completed": num_tasks_completed
        }
        volunteers_list.append(volunteer_dict)
    organiser={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('volunteers.html',volunteers=volunteers_list,eventid=id)

@app_views.route('/profile')
def getProfile():
    if not current_user.is_authenticated:
        return redirect(url_for("app_views.loginUser"))
    return render_template('profile.html',user=current_user)

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
    try:
        # pass
        # if current_user.is_authenticated:
        return render_template('signup.html')   
        #     return redirect(url_for("app_views.dashboard"))
    except Exception as e:
            print(str(e))
            return render_template('signup.html',error=str(e))   
        

     


@app_views.route('/login',methods=["POST","GET"])
def loginUser():
    from Event_Management import load_user
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            ftype = request.form['ftype']
            print("cur",current_user)
            # Check if the username and password match
            user_dict=check_user_type(connection,cursor,email)
            utype=user_dict["utype"]
            print(user_dict)
            if utype=="Anonymous":
                return redirect(url_for("app_views.registerUser"))
            elif utype=="Participant":
                success, row = check_participant_login(connection,cursor,email,password)       
            elif utype=="Student":
                success, row = check_student_login(connection,cursor,email,password)          
            elif utype=="Organiser":
                success, row = check_organiser_login(connection,cursor,email,password)
            elif utype=="Admin":
                success, row = check_admin_login(connection,cursor,email,password)
            
                
            if success:
                print("here")
                user = load_user(user_dict["data"]["email"])
                print("here",user)
                login_user(user)
                return redirect(url_for("app_views.dashboard"))


            else:
                print("login error")
                # Authentication failed, render the login form with an error message
                return render_template('login.html', error='Invalid username or password')
    except Exception as e:
            print(str(e))
            return render_template('login.html', error=str(e))

    return render_template('login.html',events=[])

# @app_views.route('/login/participant', methods=['POST'])
# def loginParticipant():
#     from Event_Management import load_user
#     try:
#         if request.method == 'POST':
#             email = request.form['email']
#             password = request.form['password']
#             print("cur",current_user)
#             # Check if the username and password match
#             user_dict=check_user_type(email)
#             utype=user_dict["utype"]
#             if utype!="Participant":
#                 return redirect(url_for("loginUser"))
#             success, row = check_participant_login(connection,cursor,email,password)
#             if success:
#                 user_dict={"name":"name","id":row[0],"utype":"participant"}
#                 user = load_user(user_dict["data"]["p_id"])
#                 # login_user(user)
#                 # user={"user":row,"is_active":True}
#                 # print(type(row),row,user)
#                 login_user(user_dict["data"])
#                 return redirect(url_for("app_views.dashboardParticipant"))

#             else:
#                 # Authentication failed, render the login form with an error message
#                 return render_template('login.html', error='Invalid username or password')
#     except Exception as e:
#             print(str(e))
#             return render_template('login.html', error=str(e))

         
# @app_views.route('/login/student', methods=['POST'])
# def loginStudent():
#     if request.method == 'POST':
#         username = request.form['email']
#         password = request.form['password']
        
#         # Check if the username and password match
#         if True:
#             return jsonify({'success':True,'user':{},'utype':'Participant'})

#         success, row = check_student_login(connection,cursor,username,password)
#         if success:
#             # Authentication successful, redirect to a protected page
#             return redirect(url_for('app_views.dashboardStudent'))
#         else:
#             # Authentication failed, render the login form with an error message
#             return render_template('login.html', error='Invalid username or password')
    
# @app_views.route('/login/organiser', methods=['POST'])
# def loginOrganiser():
#     if request.method == 'POST':
#         username = request.form['email']
#         password = request.form['password']

#         print(request.form)

#         success, row = check_organiser_login(connection,cursor,username,password)
        
#         # Check if the username and password match
#         if success:
#             # Authentication successful, redirect to a protected page
#             return redirect(url_for('app_views.dashboardOrganiser'))
#         else:
#             # Authentication failed, render the login form with an error message
#             return render_template('login.html', error='Invalid username or password')
    
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
        # phone_number = 9876543210
        phone_number = info.get('phone_number')
        can_create = 1
        success, error = insert_organiser(connection,cursor,email,password,name,phone_number,can_create)

        if success:
        # Registration successful, redirect to login page
            return redirect(url_for('app_views.loginUser'))
    
    # If GET request, render the registration form
    return render_template('signup.html', error=None)   

 
    
@app_views.route('/register/student', methods=['POST'])
def registerStudent():
    try:
            
        if request.method == 'POST':
            from Event_Management import load_user

            email = request.form['email']
            password = request.form['password']
            # Check if the username already exists
            # user_dict=check_user_type(connection,cursor,email)
            # utype=user_dict["utype"]

            # if utype!="Anonymous":
            #         return redirect(url_for("app_views.dashboard"))

            print("data from form: ",request.form)
            info = request.form
            name = info.get('name')
            email = info.get('email')
            dept = info.get('department')
            roll_no = info.get('rollno')
            phone_number = info.get('phone')
            password = info.get('password')

            success, error = insert_student(connection,cursor,roll_no,dept,name,phone_number,email,password)
            print(success,error,"in register")
            # Registration successful, redirect to login page
            if success:
                return redirect(url_for('app_views.loginUser'))
    except Exception as e:
        print(str(e))
        return render_template('signup.html', error=str(e))   
           
        
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
        print(success,error,"signup")
        if success:
            
            return redirect(url_for('app_views.loginUser'))
    
    # If GET request, render the registration form
    return render_template('signup.html', error=error)


@app_views.route('/add_accomodation', methods=['POST'])
def addAccomodation():
    if request.method == 'POST':

        info = request.form
        print(info)

        name = info.get('name')
        price = info.get('price')
        days = info.get('days')
        desc = info.get('desc')
        price = int(price)
        days = int(days)

        print(name,price,days,desc)
        success, error = insert_accomodation(connection,cursor,price,days,name,desc)
        if success:
            return redirect(url_for('app_views.facilities'))
        else:
            return redirect(url_for('app_views.dashboard'))
        

@app_views.route('/subcribe_accomodation', methods=['POST'])
def subscribeAccomodation():
    if request.method == 'POST':
        print(request.form)
        info = request.form

        if current_user.utype=="participant":
            p_id = current_user.p_id
            acc_id = info.get('acco-1')

            success, error = subscribe_accomodation(connection,cursor,p_id,acc_id)
            if success:
                return redirect(url_for('app_views.dashboard'))
            else:
                return redirect(url_for('app_views.dashboard'))
        else:
            return redirect(url_for('app_views.dashboard'))

@app_views.route('/subcribe_food', methods=['POST'])
def subscribeFood():
    if request.method == 'POST':
        info = request.form
        # print(info)
        print(current_user.utype)
        if current_user.utype=="participant":
            p_id = current_user.p_id
            food_id = info.get('food-1')

            print(p_id,food_id)
            success, error = subscribe_food(connection,cursor,p_id,food_id)
            if success:
                return redirect(url_for('app_views.dashboard'))
            else:
                return redirect(url_for('app_views.dashboard'))
        else:
            return redirect(url_for('app_views.dashboard'))
 
@app_views.route('/add_food', methods=['POST'])
def addFood():
    if request.method == 'POST':
        info = request.form
        print("Info printed from here ",info)
        name = info.get('name')
        days = info.get('days')
        price = info.get('price')
        desc = info.get('desc')
        type = info.get('table-1-main')
        if type == "on":
            type = "Veg"
        else:
            type = "NonVeg"
        price = int(price)
        days = int(days)
        success, error = insert_food(connection,cursor,type,price,days,name,desc)
        print("Success from here ",success)
        if success:
            return redirect(url_for('app_views.facilities'))
        else:
            return redirect(url_for('app_views.dashboard'))
 
@app_views.route('/add-organiser')
def AddOrganiser():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('add-organiser.html',events=[])

@app_views.route('/facilities')
def facilities():
    # fetch acco , food
    accomodation_list = get_all_accomodation(connection,cursor)
    food_list = get_all_food(connection,cursor)
    
    print(food_list)
    # profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('logistics_admin.html',events=[],accomodation=accomodation_list,food=food_list)

@app_views.route('/plans')
def plans():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    # accomodations=[
    #     {"title":"Basic","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
    #     {"title":"Premium","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
    #     {"title":"Standard","price":40,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
    #     {"title":"Economy","price":10,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
    #                ]
    # food=[
    #     {"title":"Basic","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
    #     {"title":"Premium","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
    #     {"title":"Standard","price":40,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
    #     {"title":"Economy","price":10,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
    #                ]
    facilities=[
        {"title":"Bus Service","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
        {"title":"Toto Booking","price":20,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
        {"title":"Campus Tour","price":40,"desc":"dsjchdsjfhdsss adsa dasd sad asd as sad sad "},
                   ]

    success,accomodations = fetch_all_acc_plans(connection,cursor)
    success,food = fetch_all_food_plans(connection,cursor)


    # Convert to list of dictionaries
    accomodations_list=[]
    for accomodation in accomodations:
        accomodations_list.append({"title":accomodation[3],"price":accomodation[1],"desc":accomodation[4],"days":accomodation[2],"id":accomodation[0]})

    print(accomodations_list)

    food_list=[]
    for f in food:
        food_list.append({"title":f[6],"price":f[5],"desc":f[3],"days":f[2],"id":f[0]})

    print(food_list)
    

    return render_template('plancards.html',accomodations=accomodations_list,food=food_list,facilities=facilities)

@app_views.route('/update-winners/<int:e_id>', methods=['POST'])
def updateWinners(e_id):
    if request.method == 'POST':
        info = request.form
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
    cursor.execute("""
        SELECT e_id,date_and_time,name,type_event,description,first,second,third,prize,venue,num_p
        FROM event
        ORDER BY date_and_time DESC
        LIMIT 5
    """)
    
    events_data = cursor.fetchall()
    
    events_list = []
    for event_data in events_data:
        event_dict = {
            "e_id": event_data[0],
            "date_and_time": str(event_data[1]),
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
    
    cursor.execute("""
        SELECT time_t, description
        FROM notifications
        ORDER BY time_t DESC
        LIMIT 5
    """)
    
    # Fetch all rows from the result set
    notifications = cursor.fetchall()
    
    
    
    notifications_list = []
    for notification_data in notifications:
        notification_dict = {
            "timestamp": str(notification_data[0]),
            "description": notification_data[1]
        }
        notifications_list.append(notification_dict)
    
    organiser_list = []
    cursor.execute("""
        SELECT o_id, name, email, phone_number
        FROM organiser
    """)
    organisers = cursor.fetchall()
    for organiser in organisers:
        organiser_dict = {
            "id": organiser[0],
            "name": organiser[1],
            "email": organiser[2],
            "phone": organiser[3]
        }
        organiser_list.append(organiser_dict)

    student_list = []
    cursor.execute("""
        SELECT roll_no, name, email, phone_number
        FROM student
    """)
    students = cursor.fetchall()
    for student in students:
        student_dict = {
            "id": student[0],
            "name": student[1],
            "email": student[2],
            "phone": student[3]
        }
        student_list.append(student_dict)

    participant_list = []
    cursor.execute("""
        SELECT p_id, name, email, phone_number
        FROM participant
    """)
    participants = cursor.fetchall()
    for participant in participants:
        participant_dict = {
            "id": participant[0],
            "name": participant[1],
            "email": participant[2],
            "phone": participant[3]
        }
        participant_list.append(participant_dict)

    
    print("Student list ",student_list)
    print("Organiser list ",organiser_list)
    print("Participant list ",participant_list)

    
    print("List of events ",events_list)
    try:
        
        print(current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for("app_views.loginUser"))
        elif current_user.utype=="participant":
            return render_template('dashboard_participant.html',user=current_user,trending_events=events_list,notifications=notifications_list)
        elif current_user.utype=="student":
            # print("from here ",current_user.tasks)
            return render_template('dashboard_student.html',user=current_user,trending_events=events_list,notifications=notifications_list)
        elif current_user.utype=="organiser":
            # volunteers=
            total_reg=sum([item["num_p"] for item in current_user.events_organised])
            print("events:",current_user.events_organised)
            
            return render_template('dashboard_organiser.html',user=current_user,total_reg=total_reg,trending_events=events_list,notifications=notifications_list)
        elif current_user.utype=="admin":
            return render_template('dashboard_admin.html',user=current_user,trending_events=events_list,notifications=notifications_list,organisers=organiser_list,students=student_list,participants=participant_list)
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
    # profile={"name":"Smarak K.","phone":9323232323,"bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}

    return render_template('schedule.html',events=current_user.events_registered)


@app_views.route('/add_task/<int:e_id>', methods=['GET','POST'])
def addTask(e_id):
    
    if request.method == 'POST':

        if current_user.utype=="organiser":
            roll_no = int(request.form['student_id'])
            
            description = request.form['desc']
            success, error = insert_task(connection,cursor,roll_no,description,e_id)
            if success:
                return redirect(request.url)
            else:
                return redirect(url_for('app_views.dashboard'))
        else:
            return redirect(url_for('app_views.dashboard'))

    # return redirect(url_for('app_views.getVolunteers'))
        
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
    try:
        print(current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for("app_views.loginUser"))
        elif current_user.utype=="participant":
            participant_id = current_user.p_id
            participant_type="Participant"
            success,error=register_participant(connection,cursor,e_id, participant_id, participant_type)
            if success:
                return jsonify({"message": "Registered successfully"}), 201
            else:
                return jsonify({"error": error}), 500 
        elif current_user.utype=="student":
            participant_id = current_user.roll_no
            participant_type="Student"
            success,error=register_participant(connection,cursor,e_id, participant_id, participant_type)
            if success:
                return jsonify({"message": "Registered successfully"}), 201
            else:
                return jsonify({"error": error}), 500 
        elif current_user.utype=="organiser":
            return redirect(url_for("app_views.dashboard"))
        elif current_user.utype=="admin":
            return redirect(url_for("app_views.dashboard"))
    except Exception as e:
            print(str(e))
            return redirect(url_for("app_views.loginUser"))
    
@app_views.route('/do_task/<int:task_id>', methods=['POST'])
def do_task(task_id):
    info = request.form
    success, error = complete_task(connection,cursor,task_id)
    if success:
        return jsonify({"message": "Task completed successfully"}), 201
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

@app_views.route('/delete_user', methods=['POST'])
def delete_user():
    info = request.json
    utype = info.get('utype')
    id = info.get('id')
    success, error = delete_from_db(connection,cursor,utype,id)
    if success:
        return redirect(request.url)
    else:
        return redirect(url_for('app_views.dashboard'))
