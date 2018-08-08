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
from flask import Flask, render_template, redirect, flash, url_for, request, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, SelectField, IntegerField, PasswordField, validators
from passlib.hash import sha256_crypt
from helpers import login_required, collect_form_data
from datetime import timedelta

#app is the name of the flask app
app = Flask(__name__)

#necessary for session to work
app.secret_key = "i7T7e@CkqVkuHT5Lo9PH9xeg"

#Configuring MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
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
        session["Selected_language"] = request.form["Selected_language"]
        #Show debug message
        flash('Selected ' + str(session["Selected_language"] + ' language'), "success")
        #rediect to the next page
        return redirect(url_for('select_user_type'))
    return render_template('enduser/select_language.html')


#End-User second page. Select user type from (parent/student/visitor)
@app.route('/select_user_type',methods=['GET','POST'])
def select_user_type():
    #if End-User selected a user type
    if request.method == 'POST':
        #Record User type
        session["user_type"] = request.form["User_type"]
        #Show debug message
        flash('Selected ' + str(session["user_type"] + ' Form'), "success")
        #Redirect to the next page
        return redirect(url_for('request_basic'))
    return render_template('enduser/select_user_type.html')


#End-User third page. Filling out the forms.
@app.route('/request_basic',methods=['GET','POST'])
def request_basic():
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
        session["Student_name"] = data["Student_name"]
        session["Parent_name"] = data["Parent_name"]
        #Request advance enqires user about request type
        return redirect(url_for('request_advance'))
    return render_template('enduser/request_basic.html',form=form)

#Enduser fourth page. Filling out the forms.
@app.route('/request_advance',methods=['GET','POST'])
def request_advance():
    #Make a request form class object and pass in request data from template to the object
    form = RequestAdvanceForm(request.form)
    #If End-User select a request_type
    if request.method == 'POST':

        if session["user_type"] == 'Student':
            request_list = [form.Student_Academic.data,form.Student_Accounting,form.Student_FrontDesk.data]
        elif session["user_type"] == 'Visitor':
            request_list = [form.Visitor_FrontDesk.data, form.Visitor_Accounting.data]
        elif session["user_type"] == 'Parent':
            request_list = [form.Parent_Academic.data,form.Parent_FrontDesk.data,form.Parent_Accounting.data]
        else:
            error = "Unable to recognize user type."
            render_template('enduser/select_language',error)

        for request in request_list:
            if request:
                #Get the request type
                request_type = request
                number += 1
        if number > 1:
            error = "Please Don't Select more than one Request Type!"
            return render_template('enduser/request_advance',error=error)




        #Connect to MySQL server and traverse the database with a dictionary cursor
        cur = mysql.connection.cursor()
        #if student
        if session["user_type"] == "Student":
            #Get Recent Student_name
            recent = cur.execute("SELECT * FROM total_queue WHERE Student_name=%s", [session['Student_name']])
        else:
            #Get parent name
            recent = cur.execute("SELECT * FROM total_queue WHERE Parent_name=%s", [session['Parent_name']])
        #Get that student number or current postion in the queue (its important for workspace to keep track of this queue position)
        number = cur.fetchone()["Number"]
        #Pop it off, since we no longer need it
        session.pop('Student_name',None)
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
        #Commit to Database
        mysql.connection.commit()
        #Close connection
        cur.close()
        #Flask message
        flash("Request Completed !", "success")
        #Return to index
        return redirect(url_for('select_language'))
    return render_template('enduser/request_advance.html',form=form)

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
                session['logged_in'] = True
                session['username'] = Username
                session['department'] = Department
                #flash message
                flash("You are now logged in !  (◠‿◠✿)", 'success')
                #redirect to workspace
                return redirect(url_for('workspace'))
            else:
                #flash error message
                error = 'Invalid Credentials. (◡︿◡✿)'
                #render login with error
                return render_template('admin/login.html',error=error)
            #close connection
            cur.close()
        else:
            #flash error user not found in database
            error = 'Username Not Found. ↁ_ↁ'
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
    #loading form class
    form = WorkspaceForm(request.form)
    #connect to database
    cur = mysql.connection.cursor()
    #Select all data from associated workspace
    results = cur.execute("""SELECT *
    FROM total_queue JOIN (request_types)
    ON (total_queue.Request_type = request_types.Request_type)
    WHERE request_types.Department = %s AND total_queue.Status != %s """, (session["department"], 'Completed'))
    #if admin presses reassign button
    if request.method == 'POST' and form.validate():
        #Get request_type from reassign form
        Reassign = form.Reassign.data
        #Select number from the total_queue table, fetch the one on top to reassign
        cur.execute("SELECT * FROM total_queue WHERE Status = %s",["In Progress"])
        #Fetch the number from the NUMBER column
        number = cur.fetchone()["Number"]
        #Update the request type which will display it to a different department
        cur.execute("UPDATE total_queue SET Request_type=%s WHERE Number=%s",([Reassign],[number]))
        #Select all from request types table where data in column matches with the request type
        data = cur.execute("SELECT * FROM request_types WHERE Request_type=%s", [Reassign])
        #Fetch the department related to the request type
        department = cur.fetchone()["Department"]
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
            else:
                #If its still in the same department then just update the time in
                cur.execute("UPDATE accounting_queue SET Time_in=NOW() WHERE Number=%s", [number])
        #flash debug message
        flash(number,"success")
        #Commit to database
        mysql.connection.commit()
        #flash message
        flash('Entry Reassigned! ', 'success')
        #return to workspace after reassign
        return redirect(url_for('workspace'))
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
    WHERE Status=%s""",["In Progress"])
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
    #Create dictionary cursor
    cur = mysql.connection.cursor()
    #Update total_queue Set Status to be In Progress
    cur.execute("UPDATE total_queue SET Status=%s WHERE Number=%s",("In Progress",[number] ))
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

#reassign form class
class WorkspaceForm(Form):
    Reassign = SelectField( '',
        choices = [(-1,'<Select Request Type>'),('Information','Information'), ('Enrollment','Enrollment'), ('Tuition Fee','Tuition Fee')]
    )

class RequestAdvanceForm(Form):
    Student_FrontDesk = SelectField('Front Desk:',
        choices = [(-1, '<Select Request Type>'),('Late Slip','Late Slip'),('Leave Early','Leave Early'),('Reenrollment','Reenrollment'),
        ('Lost and Found','Lost and Found'),('General Enquiry','General Enquiry')])
    Student_Academic = SelectField('Academics Department',
        choices = [(-1, '<Select Request Type>'),('Transcript/Report Card','Transcript/Report Card'),('Academic Paperwork','Academic Paperwork'),
        ('Enquiry','Enquiry')])
    Student_Accounting = SelectField('Accounting Department',
        choices = [(-1, '<Select Request Type>'),('Payment','Payment')])

    Parent_FrontDesk = SelectField('Front Desk',
        choices = [(-1, '<Select Request Type>'),('Reenrollment','Reenrollment'),('Appointment','Appointment'),('General Enquiry','General Enquiry'),('Leave','Leave'),
        ('Lost and Found','Lost and Found'),('General Enquiry','General Enquiry')])
    Parent_Academic = SelectField('Academics Department',
        choices = [(-1, '<Select Request Type>'),('Transcript/Report Card','Transcript/Report Card'),('Academic Paperwork','Academic Paperwork'),
        ('Enquiry','Enquiry')])
    Parent_Accounting = SelectField('Accounting Department',
        choices = [(-1, '<Select Request Type>'),('Payment','Payment'),('Finance Enquiry ','Finance Enquiry')])

    Visitor_FrontDesk = SelectField('Front Desk',
        choices = [(-1, '<Select Request Type>'),('Enrollment','Enrollment'),('Admission Appointment','Admission Appointment'),('General Enquiry','General Enquiry'),
        ('Job Interview','Job Interview'), ('Business Meeting','Business Meeting')])
    Visitor_Accounting = SelectField('Accounting Department',
        choices = [(-1, '<Select Request Type>'),('Collect Payment','Payment')])


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
    Department = SelectField( 'Select Department',
        choices = [(-1,'<Select Department>'),('Accounting','Accounting Department'), ('Front Desk','Front Desk'), ('IT','IT Department')]
    )

# if name of app is main
if __name__ == '__main__':
    app.run(host="0.0.0.0",port="80",debug = True)
