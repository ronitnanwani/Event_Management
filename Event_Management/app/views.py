from . import *
from .__init__ import connection,cursor

from Event_Management.database import *

app_views = Blueprint('app_views', __name__)

@app_views.route('/')
def index():
    return render_template('test.html', name='orld')
@app_views.route('/events')
def getEvents():
    events=[
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        
        ]
    return render_template('events.html', name='events',events=events)
@app_views.route('/add-event')
def addEvent():
    events=[
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        
        ]
    
    info = request.form
    print(info)
    return render_template('addEvent.html', name='events',events=events)

@app_views.route('/event/<int:id>')
def eventDetails(id):
    
    events=[
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        
        ]
    organiser={"name":"Smarak K.","role":"Events Head","email":"adjahs@g.co","phone":92309123912,"bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    user={"name":"Smarak K.","num_tasks_allotted":50,"num_tasks_completed":20}
    
    return render_template('eventDetails.html', name='events',event=events[0],organiser=organiser,user=user)

@app_views.route('/volunteers')
def getVolunteers():
    
    events=[
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        {"title":"Event 1","num_p":200,"desc":"this is the event description.this is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event descriptionthis is the event description","tags":["hello","tags1","tag2"]},
        
        ]
    organiser={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('volunteers.html')

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


@app_views.route('/login')
def loginUser():
    profile={"name":"Smarak K.","bio":"asdhfgdsajnsadmnasd dsajd as dadas das"}
    return render_template('login.html',events=[])

@app_views.route('/login/participant', methods=['POST'])
def loginParticipant():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        
        # Check if the username and password match
        success, row = check_participant_login(connection,cursor,username,password)
        if success:
            # Authentication successful, redirect to a protected page
            return redirect(url_for('app_views.dashboardParticipant'))
        else:
            # Authentication failed, render the login form with an error message
            return render_template('login.html', error='Invalid username or password')
    
@app_views.route('/login/student', methods=['POST'])
def loginStudent():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        
        # Check if the username and password match

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

# Dashboards--------------------------
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

