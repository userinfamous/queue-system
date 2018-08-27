#Author: Vuottek Un
#Project Title: Queue-System
#Description:
#   The upper parts are imports and declaration of the app
#   after that, comes all the features that we implement.
#   Then there are the classes, and at the bottom is the app.run() itself.

# NOTE:
# lower case session["text"] or cookies refer to the admin
# Upper case cookies refer to the end user
# MySQL cursor allows us to traverse and manipulate the database, it is also dictionary based
# Each department has got their own table (i.e accounting_queue and front_desk_queue) It's for recording time in and time out in the respective deparment

#Importing necessary dependencies for the project
from flask import Flask, render_template, redirect, flash, url_for, request, session, logging, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, SelectField, IntegerField, PasswordField, validators, SubmitField
from wtforms_components.fields import SelectField
from passlib.hash import sha256_crypt
from helpers import login_required, collect_form_data
from datetime import timedelta
from json import dumps

#app is the name of the flask app
app = Flask(__name__)

#necessary for session to work
app.secret_key = "i7T7e@CkqVkuHT5Lo9PH9xeg"

#Configuring MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'CIACampus@2'
app.config['MYSQL_DB'] = 'users'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Initialize MySQL
mysql = MySQL(app)

#End-User first page (select language)
@app.route('/',methods=['GET','POST'])
def select_language():
    #if End-User selected a language
    if request.method == 'POST':
        #Record Language
        session["selected_language"] = request.form["Selected_language"]
        #rediect to the next page
        return redirect(url_for('select_user_type'))
    return render_template('enduser/select_language.html')


#End-User second page. Select user type from (parent/student/visitor)
@app.route('/select_user_type',methods=['GET','POST'])
def select_user_type():
    #Check for sessions for it to work properly
    if "selected_language" not in session:
        flash("You do not have the necessary data to pass through.","danger")
        return redirect(url_for('select_language'))

    #if End-User selected a user type
    if request.method == 'POST':
        #Record User type
        session["user_type"] = request.form["User_type"]
        #Show debug message
        #Redirect to the next page
        return redirect(url_for('request_basic'))
    return render_template('enduser/select_user_type.html')


#End-User third page. Filling out the forms.
@app.route('/request_basic',methods=['GET','POST'])
def request_basic():
    #Check for sessions for it to work properly
    cookies = ["selected_language","user_type"]
    for cookie in cookies:
        if cookie not in session:
            flash("You do not have the necessary data to pass through.","danger")
            return redirect(url_for('select_language'))

    #Make a request form class object and pass in request data from template to the object
    form = RequestBasicForm(request.form)
    #If enduser presses confirm to submit the form
    if request.method == 'POST':
        #Pass form into a function that handles translation from data receieved
        data = collect_form_data(form)
        #Connect to MySQL server and traverse the database with a dictionary cursor
        cur = mysql.connection.cursor()
        #Update the database
        cur.execute("""INSERT INTO total_queue(user_type,Parent_name, Student_name, Student_id, Contact)
        VALUES(%s, %s, %s, %s, %s)""", (session["user_type"], data['Parent_name'], data['Student_name'], data['Student_id'],  data['Contact']))
        #Commit to the database
        mysql.connection.commit()
        #Close connection to server
        cur.close()
        #Record student name
        session["student_name"] = data["Student_name"]
        session["parent_name"] = data["Parent_name"]
        #Request advance enqires user about request type
        return redirect(url_for('request_advance'))
    return render_template('enduser/request_basic.html',form=form)

#Enduser fourth page. Filling out the forms.
@app.route('/request_advance',methods=['GET','POST'])
def request_advance():
    #Check for sessions for it to work properly
    cookies = ["user_type","selected_language","parent_name","student_name"]
    for cookie in cookies:
        if cookie not in session:
            flash("You do not have the necessary data to pass through.","danger")
            return redirect(url_for('select_language'))
    #Make a request form class object and pass in request data from template to the object
    form = RequestAdvanceForm(request.form)
    #If End-User select a request_type
    if request.method == 'POST' and request.form.get("Back"):
        cur = mysql.connection.cursor()
        if session["user_type"] == 'Student':
            cur.execute("DELETE FROM total_queue WHERE Student_name=%s LIMIT 1",[session["student_name"]])
        elif session["user_type"] == 'Parent' or session["user_type"] == 'Visitor':
            cur.execute("DELETE FROM total_queue WHERE Parent_name=%s LIMIT 1",[session["parent_name"]])
        mysql.connection.commit()
        cur.close()

        #Pop it off, since we no longer need it
        session.pop('student_name',None)
        session.pop('parent_name',None)

        #Entry Deleted
        flash("Entry deleted from the database.","success")

        return redirect(url_for('request_basic'))

    elif request.method == 'POST' and request.form.get("Confirm"):

        cur = mysql.connection.cursor()
        cur.execute("UPDATE check_changes SET counting = counting + 1 WHERE id=1")
        cur.close()

        if session["selected_language"] == 'English':
            if session["user_type"] == "Parent":
                request_type = form.en_Parent.data
            elif session["user_type"] == "Student":
                request_type = form.en_Student.data
            elif session["user_type"] == "Visitor":
                request_type = form.en_Visitor.data
        elif session["selected_language"] == 'Khmer':
            if session["user_type"] == "Parent":
                request_type = form.kh_Parent.data
            elif session["user_type"] == "Student":
                request_type = form.kh_Student.data
            elif session["user_type"] == "Visitor":
                request_type = form.kh_Visitor.data

        #Connect to MySQL server and traverse the database with a dictionary cursor
        cur = mysql.connection.cursor()
        #check for recent entries formed by request basic in the database
        recent = cur.execute("SELECT * FROM total_queue WHERE Status=%s AND Request_type='' AND Student_name=%s ORDER BY Number ASC", (["Waiting"],session["student_name"]))
        #Get that student number or current postion in the queue
        number = cur.fetchone()["Number"]
        #Update total_queue, the Request_type using current queue position
        cur.execute("UPDATE total_queue SET Request_type=%s WHERE Number=%s",([request_type],[number]))
        #Select all from request_types table where the Request_type is equal to the current request_type
        results = cur.execute("SELECT * FROM request_types WHERE Request_type=%s",[request_type])
        #Get department under that request type
        department = cur.fetchone()["Department"]
        #Do a check for whichever department and insert into that department's table (each department has got their own table to check for time and time out)
        if department == 'Front Desk':
            cur.execute("INSERT INTO front_desk_queue(Number) VALUES(%s)",[number]) #record time in
        elif department == 'Accounting':
            cur.execute("INSERT INTO accounting_queue(Number) VALUES(%s)",[number])  #record time in
        elif department == "Academic":
            cur.execute("INSERT INTO academic_queue(Number) VALUES(%s)",[number])  #record time in

        #Commit to Database
        mysql.connection.commit()
        #Close connection
        cur.close()
        #Flask message
        flash("Request Completed !", "success")

        #Pop it off, since we no longer need it
        session.pop('student_name',None)
        session.pop('parent_name',None)

        #Return to index
        return redirect(url_for('select_language'))
    return render_template('enduser/request_advance.html',form=form)

@app.route('/checker',methods=['GET','POST'])
@login_required
def checker():
    return render_template('admin/checker.php')

#Admin Registeration page, can technically be accessed by anyone
@app.route('/register',methods=['GET','POST'])
def register():
    #Make a register form class object and pass in request data from template to the object
    form = RegisterForm(request.form)
    #if admin pressed submit and everything is validated
    if request.method == 'POST' and form.validate():
        #Get data from form if that is the case
        Name = form.Name.data
        Email = form.Email.data
        Username = form.Username.data
        Password = sha256_crypt.encrypt(str(form.Password.data))
        Department = form.Department.data
        #Create DictCursor
        cur = mysql.connection.cursor()
        #Insert into admins table
        cur.execute("""INSERT INTO admins(Name, Email, Username, Password, Department)
        VALUES(%s, %s, %s, %s, %s)""", (Name, Email, Username, Password, Department))
        #Commit to database
        mysql.connection.commit()
        #Close connection
        cur.close()
        #Flash message
        flash("Registered as Admin !", "success")
        #Redirect to login after registerred
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form)

#Admin login
@app.route('/login', methods=['GET','POST'])
def login():
    #if admin presses submits
    if request.method == 'POST':
        #Get username and password
        Username = request.form['Username']
        Password_Candidate = request.form['Password']
        #Connect to MySQL server
        cur = mysql.connection.cursor()
        #Get all entries from admins through username
        results = cur.execute("SELECT * FROM admins WHERE Username=%s", [Username])
        #if there is an entry of match
        if results > 0:
            #fetch the first one that closest to the query
            data = cur.fetchone()
            #scrape data from entry
            Password = data['Password']
            Department = data['Department']
            #check for password from the entry
            if sha256_crypt.verify(Password_Candidate, Password):
                #if the password match, then log the user in
                session["logged_in"] = True
                session["username"] = Username
                session["department"] = Department
                #flash message
                flash("You are now logged in !", 'success')
                #redirect to workspace
                return redirect(url_for('workspace'))
            else:
                #flash error message
                error = 'Invalid Credentials.'
                #render login with error
                return render_template('admin/login.html',error=error)
            #close connection
            cur.close()
        else:
            #flash error user not found in database
            error = 'Username Not Found.'
            #render login with error
            return render_template('admin/login.html',error=error)
    return render_template('admin/login.html')

#admin logout
@app.route('/logout')
@login_required
def logout():
    #clear everything from session
    session.clear()
    flash('You are now logged out.', 'success')
    return redirect(url_for('login'))

#admin workspace
@app.route('/workspace', methods=['GET','POST'])
@login_required
def workspace():
    #check in case missing cookie
    if "department" not in session:
        flash("You do not have the necessary data to pass through.","danger")
        return redirect(url_for('login'))

    #loading form class
    form = WorkspaceForm(request.form)

    #connect to database
    cur = mysql.connection.cursor()
    #Select all data from associated workspace
    results = cur.execute("""SELECT *
    FROM total_queue JOIN (request_types)
    ON (total_queue.Request_type = request_types.Request_type)
    WHERE request_types.Department = %s AND total_queue.Status != %s
    ORDER BY Number ASC""", (session["department"], ["Completed"])) #!= accounts for waiting numbers too
    #if admin presses reassign button
    if request.method == 'POST':
        #Get request_type from reassign form
        reassign = form.en_Assign.data
        #Select all in progress
        results = cur.execute("SELECT * FROM total_queue WHERE Status=%s",["In Progress"])
        #Select number from the total_queue table, fetch the one on top to reassign
        query = cur.fetchone()
        number = query["Number"]
        current = query["Request_type"]
        #Update the request type which will display it to a different department
        cur.execute("UPDATE total_queue SET Request_type=%s WHERE Number=%s",([reassign],[number]))
        #Select all from request types table where data in column matches with the request type
        data = cur.execute("SELECT * FROM request_types WHERE Request_type=%s", [reassign])
        #Fetch the department related to the request type
        department = cur.fetchone()["Department"]
        #Don't allow same department to reassign
        if current == reassign:
            flash("Can't reassign to the same request type!","danger")
            return redirect(url_for('workspace'))

        #Check for department the reassign data is related to
        if department == "Front Desk":
            #Select all from front_desk_queue table where there's a number
            results = cur.execute("SELECT * FROM front_desk_queue WHERE Number=%s",[number])
            #if there isn't an entry yet
            if results == 0:
                #Then create one
                cur.execute("INSERT INTO front_desk_queue(Number) VALUES(%s)",[number])
                #While cutting short the time out for the other department
                cur.execute("UPDATE accounting_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s", [number])
                cur.execute("UPDATE academic_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s", [number])
            else:
                #If its still in the same department then just update the time in
                cur.execute("UPDATE front_desk_queue SET Time_in=NOW() WHERE Number=%s", [number])
        #Check for department the reassign data is related to
        elif department == "Accounting":
            #Select all from accounting_queue table where there's a number
            results = cur.execute("SELECT * FROM accounting_queue WHERE Number=%s",[number])
            #if there isn't an entry yet
            if results == 0:
                #Then create one
                cur.execute("INSERT INTO accounting_queue(Number) VALUES(%s)",[number])
                #While cutting short the time out for the other department
                cur.execute("UPDATE front_desk_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s", [number])
                cur.execute("UPDATE academic_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s", [number])
            else:
                #If its still in the same department then just update the time in
                cur.execute("UPDATE accounting_queue SET Time_in=NOW() WHERE Number=%s", [number])
        #Check for department the reassign data is related to
        elif department == "Academic":
                #Select all from accounting_queue table where there's a number
                results = cur.execute("SELECT * FROM academic_queue WHERE Number=%s",[number])
                #if there isn't an entry yet
                if results == 0:
                    #Then create one
                    cur.execute("INSERT INTO academic_queue(Number) VALUES(%s)",[number])
                    #While cutting short the time out for the other department
                    cur.execute("UPDATE front_desk_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s", [number])
                    cur.execute("UPDATE accounting_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s", [number])
                else:
                    #If its still in the same department then just update the time in
                    cur.execute("UPDATE academic_queue SET Time_in=NOW() WHERE Number=%s", [number])

        #Commit to database
        mysql.connection.commit()
        #flash message
        flash('Entry Reassigned! ', 'success')
        redirec(url_for('workspace'))

    #Fetch everything found, the reason why its after POST reassign is to update the changes we make
    queues = cur.fetchall()

    #If there's something to display then display
    if results > 0:
        return render_template('admin/workspace.html',queues=queues,form=form)
    #Say that there is nothing to display
    else:
        no_queue = " No Queue "
        return render_template('admin/workspace.html',no_queue=no_queue)
    #close the connection
    cur.close()

#Display number
@app.route('/display' ,methods=['GET','POST'])
def display():
    #Create dictionary cursor
    cur = mysql.connection.cursor()
    #Select number in-progress
    results = cur.execute("""SELECT *
    FROM total_queue JOIN (request_types)
    ON (total_queue.Request_type = request_types.Request_type)
    WHERE Status=%s """,["In Progress"])
    #fetch all
    queues = cur.fetchall()
    #Close connection
    cur.close()
    #display
    return render_template("enduser/display.html",queues=queues)

#Admin calling queue, there's string number because it takes the argument of number from <string:number>
@app.route('/entry_call/<string:number>', methods=['POST'])
@login_required
def entry_call(number):
    for char in session["username"]:
        if char.isnumeric():
            counter_number = char
    #Create dictionary cursor
    cur = mysql.connection.cursor()
    #Update total_queue Set Status to be In Progress
    cur.execute("UPDATE total_queue SET Status=%s, Counter_number=%s WHERE Number=%s",("In Progress",[counter_number],[number]))
    #Commit to database
    mysql.connection.commit()
    #Close connection
    cur.close()
    #flash message
    flash('Entry Called! ', 'success')
    #return to workspace
    return redirect(url_for('workspace'))

#Admin completes a queue
@app.route('/entry_complete/<string:number>', methods=['POST'])
@login_required
def entry_complete(number):
    #Create dictionary cursor
    cur = mysql.connection.cursor()
    #Execute, delete and insert
    cur.execute("UPDATE total_queue SET Status=%s WHERE Number=%s",('Completed',[number]))
    #Check for deparment to include timestamp (going out) in
    if session["department"] == "Front Desk":
        cur.execute("UPDATE front_desk_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s",[number])
    elif session["department"] == "Accounting":
        cur.execute("UPDATE accounting_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s",[number])
    #Select all from front_desk_queue table where number is same (which is only one since its primary)
    result1 = cur.execute("SELECT * FROM front_desk_queue WHERE Number=%s",[number])
    #If there is one
    if result1 > 0:
        #Fetch the time difference
        time1 = cur.fetchone()["Time_diff"]
    else:
        #If there isn't, let it be 0
        time1 = timedelta(0,0)
    #Select all from accounting_queue table where number is same (which is only one since its primary)
    result2= cur.execute("SELECT * FROM accounting_queue WHERE Number=%s",[number])
    #If there is one
    if result2 > 0:
        #Fetch the time difference
        time2 = cur.fetchone()["Time_diff"]
    else:
        #If there isn't, let it be 0
        time2 = timedelta(0,0)
    #Update
    cur.execute("UPDATE total_queue SET Total_time = %s WHERE number=%s",([time1+time2],[number]))
    #commit to Database
    mysql.connection.commit()
    #Close connection
    cur.close()
    #flash debug message
    flash('Entry Completed! ', 'success')
    #return to dashboard
    return redirect(url_for('workspace'))

#request form class
class RequestBasicForm(Form):
    en_Parent_name = StringField('Full Name',[
        validators.DataRequired(),
        validators.Length(min=1,max=100)])
    en_Student_name = StringField('Student Name',[
        validators.DataRequired(),
        validators.Length(min=1,max=100)])
    en_Student_id = StringField('Student ID',[
        validators.NumberRange(min=0, max=10)] ) #interger field to trigger number pad
    en_Contact = StringField('Contact',[
        validators.NumberRange(min=0, max=20)] ) #interger field to trigger number pad

    kh_Parent_name = StringField('ឈ្មោះ​ពេញ',[
        validators.DataRequired(),
        validators.Length(min=1,max=100)])
    kh_Student_name = StringField('ឈ្មោះ​របស់​និស្សិត',[
        validators.DataRequired(),
        validators.Length(min=1,max=100)])
    kh_Student_id = StringField('លេខសំគាល់​សិស្ស',[
        validators.Length(min=0, max=10)] ) #interger field to trigger number pad
    kh_Contact = StringField('លេខទូរសព្ទ',[
        validators.Length(min=0, max=20)] ) #interger field to trigger number pad

class RequestAdvanceForm(Form):
    en_Parent = SelectField('',[validators.DataRequired()],
        choices = [('','<Select Request Type>'),
        #Academic
        ('Academic Section', (
            ('Academic Enquiry','Academic Enquiry/Other'),
            ('Academic Paperwork','Academic Paperwork'),
            ('Transcript/Report Card','Transcript/Report Card')
        )),
        #Accounitng
        ('Accounting Section', (
            ('Finance Enquiry','Finance Enquiry/Other'),
            ('Payment','Payment'),
            ('Tuition Fee','Tuition Fee')
        )),
        #Front Desk
        ('Front Desk Section', (
            ('General Enquiry','General Enquiry/Other'),
            ('Enrollment','Enrollment'),
            ('Reenrollment','Reenrollment'),
            ('Bus Service','Bus Service'),
            ('Appointment','Appointment')
        )),
        ]
    )
    kh_Parent = SelectField('',[validators.DataRequired()],
        choices = [('','<ជ្រើសរើសលក្ខណៈនៃការស្នើសុំ>'),
        #Academic
        ('ផ្នែកសិក្សា', (
            ('Academic Enquiry','សំណួរអំពីផ្នែកការសិក្'),
            ('Academic Paperwork','ឯកសារសិក្'),
            ('Transcript/Report Card','របាយការណ៍កាតរបស់សិស្ស')
        )),
        #Accounitng
        ('ផ្នែកគណនេយ្យ', (
            ('Finance Enquiry','សំណួរអំពីហិរញ្ញវត្ថុ'),
            ('Payment','បង់ថ្លៃផ្សេងៗ'),
            ('Tuition Fee','បង់ថ្លៃ​សិក្សា')
        )),
        #Front Desk
        ('ផ្នែកការិយាល័យទទួលភ្ញៀវ', (
            ('General Enquiry','ការសាកសួរជាទូទៅ'),
            ('Enrollment','ចុះឈ្មោះចូលរៀនលើកដំបូង'),
            ('Reenrollment','ចុះឈ្មោះចូលរៀនសារ​ជា​ថ្មី'),
            ('Bus Service','សេវាកម្មឡានក្រុង'),
            ('Appointment','ការណាត់ជួប')
        )),
        ]
    )

    en_Student = SelectField('',[validators.DataRequired()],
        choices = [('','<Select Request Type>'),
        #Academic
        ('Academic Section', (
            ('Academic Enquiry','Academic Enquiry/Other'),
            ('Academic Paperwork','Academic Paperwork'),
            ('Transcript/Report Card','Transcript/Report Card')
        )),
        #Accounitng
        ('Accounting Section', (
            ('Finance Enquiry','Finance Enquiry/Other'),
            ('Payment','Payment'),
            ('Tuition Fee','Tuition Fee')
        )),
        #Front Desk
        ('Front Desk Section', (
            ('General Enquiry','General Enquiry/Other'),
            ('Late Slip','Late Slip'),
            ('Leave Early','Leave Early'),
            ('Bus Service','Bus Service'),
            ('Lost and Found','Lost and Found'),
            ('Appointment','Appointment'),
        ))
        ]
    )

    kh_Student = SelectField('',[validators.DataRequired()],
        choices = [('','ជ្រើសរើសលក្ខណៈនៃការស្នើសុំ'),
        #Academic
        ('ផ្នែកសិក្សា', (
            ('Academic Enquiry','សំណួរអំពីផ្នែកការសិក្សា'),
            ('Academic Paperwork','ឯកសារសិក្សា'),
            ('Transcript/Report Card','របាយការណ៍កាតរបស់សិស្ស')
        )),
        #Accounitng
        ('ផ្នែកគណនេយ្យ', (
            ('Finance Enquiry','សំណួរអំពីហិរញ្ញវត្ថុ'),
            ('Payment','បង់ថ្លៃផ្សេងៗ'),
            ('Tuition Fee','បង់ថ្លៃ​សិក្សា')
        )),
        #Front Desk
        ('ផ្នែកការិយាល័យទទួលភ្ញៀវ', (
            ('General Enquiry','ការសាកសួរជាទូទៅ'),
            ('Late Slip','ក្រដាសយឺតសម្រាប់មកយឺត'),
            ('Leave Early','ចាកចេញមុនម៉ោង'),
            ('Bus Service','សេវាកម្មឡានក្រុង'),
            ('Lost and Found','បាត់បង់អ្វីមួយ'),
            ('Appointment','ការណាត់ជួប'),
        ))
        ]
    )
    en_Visitor = SelectField('',[validators.DataRequired()],
        choices = [('','<Select Request Type>'),
        #Academic
        ('Academic Section', (
            ('Academic Enquiry','Academic Enquiry/Other'),
            ('Academic Paperwork','Academic Paperwork'),
            ('Transcript/Report Card','Transcript/Report Card')
        )),
        #Accounitng
        ('Accounting Section', (
            ('Finance Enquiry','Finance Enquiry/Other'),
            ('Payment','Payment'),
            ('Tuition Fee','Tuition Fee')
        )),
        #Front Desk
        ('Front Desk Section', (
            ('General Enquiry','General Enquiry/Other'),
            ('Enrollment','Enrollment'),
            ('Reenrollment','Reenrollment'),
            ('Bus Service','Bus Service'),
            ('Appointment','Appointment'),
            ('Business Meeting','Business Meeting'),
            ('Job Interview','Job Interview')
        ))
        ]
    )
    kh_Visitor = SelectField('',[validators.DataRequired()],
        choices = [('','ជ្រើសរើសលក្ខណៈនៃការស្នើសុំ'),
        #Academic
        ('ផ្នែកសិក្សា', (
            ('Academic Enquiry','សំណួរអំពីផ្នែកការសិក្សា'),
            ('Academic Paperwork','ឯកសារសិក្សា'),
            ('Transcript/Report Card','របាយការណ៍កាតរបស់សិស្ស')
        )),
        #Accounitng
        ('ផ្នែកគណនេយ្យ', (
            ('Finance Enquiry','សំណួរអំពីហិរញ្ញវត្ថុ'),
            ('Payment','បង់ថ្លៃផ្សេងៗ'),
            ('Tuition Fee','បង់ថ្លៃ​សិក្សា')
        )),
        #Front Desk
        ('ផ្នែកការិយាល័យទទួលភ្ញៀវ', (
            ('General Enquiry','ការសាកសួរជាទូទៅ'),
            ('Enrollment','ចុះឈ្មោះចូលរៀនលើកដំបូង'),
            ('Reenrollment','ចុះឈ្មោះចូលរៀនសារ​ជា​ថ្មី'),
            ('Bus Service','សេវាកម្មឡានក្រុង'),
            ('Appointment','ការណាត់ជួប'),
            ('Business Meeting','មានកិច្ចប្រជុំ'),
            ('Job Interview','សំភាសន៍ការងារ')
        ))
        ]
    )
#reassign form class
class WorkspaceForm(Form):
    en_Assign = SelectField('',[validators.DataRequired()],
        choices = [('','<Select Request Type>'),
        #Academic
        ('Academic Section', (
            ('Academic Enquiry','Academic Enquiry/Other'),
            ('Academic Paperwork','Academic Paperwork'),
            ('Transcript/Report Card','Transcript/Report Card')
        )),
        #Accounitng
        ('Accounting Section', (
            ('Finance Enquiry','Finance Enquiry/Other'),
            ('Payment','Payment'),
            ('Tuition Fee','Tuition Fee')
        )),
        #Front Desk
        ('Front Desk Section', (
            ('General Enquiry','General Enquiry/Other'),
            ('Enrollment','Enrollment'),
            ('Reenrollment','Reenrollment'),
            ('Late Slip','Late Slip'),
            ('Leave Early','Leave Early'),
            ('Bus Service','Bus Service'),
            ('Lost and Found','Lost and Found'),
            ('Appointment','Appointment'),
            ('Business Meeting','Business Meeting'),
            ('Job Interview','Job Interview')
        ))
        ]
    )

    kh_Assign = SelectField( '',[validators.DataRequired()],
        choices = [('','ជ្រើសរើសលក្ខណៈនៃការស្នើសុំ'),
        #Academic
        ('ផ្នែកសិក្សា', (
            ('Academic Enquiry','សំណួរអំពីផ្នែកការសិក្សា'),
            ('Academic Paperwork','ឯកសារសិក្សា'),
            ('Transcript/Report Card','របាយការណ៍កាតរបស់សិស្ស')
        )),
        #Accounitng
        ('ផ្នែកគណនេយ្យ', (
            ('Finance Enquiry','សំណួរអំពីហិរញ្ញវត្ថុ'),
            ('Payment','បង់ថ្លៃផ្សេងៗ'),
            ('Tuition Fee','បង់ថ្លៃ​សិក្សា')
        )),
        #Front Desk
        ('ផ្នែកការិយាល័យទទួលភ្ញៀវ', (
            ('General Enquiry','ការសាកសួរជាទូទៅ'),
            ('Enrollment','ចុះឈ្មោះចូលរៀនលើកដំបូង'),
            ('Reenrollment','ចុះឈ្មោះចូលរៀនសារ​ជា​ថ្មី'),
            ('Late Slip','ក្រដាសយឺតសម្រាប់មកយឺត'),
            ('Leave Early','ចាកចេញមុនម៉ោង'),
            ('Bus Service','សេវាកម្មឡានក្រុង'),
            ('Lost and Found','បាត់បង់អ្វីមួយ'),
            ('Appointment','ការណាត់ជួប'),
            ('Business Meeting','មានកិច្ចប្រជុំ'),
            ('Job Interview','សំភាសន៍ការងារ')
        ))
        ]
    )

#register form class
class RegisterForm(Form):
    Name = StringField('Full Name', [
        validators.DataRequired(),
        validators.Length(min=1,max=100)])
    Username = StringField('Username', [
        validators.DataRequired(),
        validators.Length(min=4,max=50)])
    Email = StringField("Email", [
        validators.DataRequired(),
        validators.Length(min=6,max=50)])
    Password = PasswordField("Password", [
        validators.DataRequired(),
        validators.EqualTo('Confirm', message="Passwords Don't Match.")
    ])
    Confirm = PasswordField('Confirm Password', [
        validators.DataRequired(),
    ])
    Department = SelectField( 'Select Department',[validators.DataRequired()],
        choices = [('','<Select Department>'),('Accounting','Accounting Department'), ('Front Desk','Front Desk'), ('Academic','Academic Department')]
    )

# if name of app is main
if __name__ == '__main__':
    app.run(host="0.0.0.0",port="88",debug = True)
