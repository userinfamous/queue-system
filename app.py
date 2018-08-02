#Author: Vuottek Un
#Project Title: Queue-System
#Description:
#   The upper parts are imports and declaration of the app
#   after that, comes all the features that we implement.
#   Then there are the classes, and at the bottom is the app.run() itself.

# NOTE:
# lower case session["text"] or cookies refer to the admin
# Upper case cookies refer to the end user

#Importing necessary dependencies for the project
from flask import Flask, render_template, redirect, flash, url_for, request, session, logging
from tempfile import mkdtemp
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

#Enduser first page (select language)
@app.route('/',methods=['GET','POST'])
def select_language():
    if request.method == 'POST':
        session["Selected_language"] = request.form["Selected_language"]
        flash('Selected ' + str(session["Selected_language"] + ' language'), "success")
        return redirect(url_for('select_user_type'))
    return render_template('enduser/select_language.html')

#Enduser second page. Select (parent/student/visitor)
@app.route('/select_user_type',methods=['GET','POST'])
def select_user_type():
    if request.method == 'POST':
        session["User_type"] = request.form["User_type"]
        flash('Selected ' + str(session["User_type"] + ' Form'), "success")
        return redirect(url_for('request_basic'))
    return render_template('enduser/select_user_type.html')


#Enduser third page. Filling out the forms.
@app.route('/request_basic',methods=['GET','POST'])
def request_basic():

    #Assimulat the classes proerties to be passed into template
    form = RequestForm(request.form)

    #If enduser press confirm
    if request.method == 'POST':
        #Loaded script from helpers to reduce messiness
        Data = collect_form_data(form)

        #Create a dictionary cursor
        cur = mysql.connection.cursor()

        #Check for duplicates
        check = cur.execute("SELECT * FROM total_queue WHERE Student_name=%s",[Data['Student_name']] )

        #If there is any
        if check > 0:
            #Flask message
            flash("Request Failed Duplicates Sent !", "danger")
            #Close connection
            cur.close()
            #Return, assume queue already exists (Assuming no two students with the same name happen to be in the sane queue)
            return redirect(url_for('select_language'))

        #Update the database
        cur.execute("""INSERT INTO total_queue(User_type,Parent_name, Student_name, Student_id, Contact)
        VALUES(%s, %s, %s, %s, %s)""", (session["User_type"], Data['Parent_name'], Data['Student_name'], Data['Student_id'],  Data['Contact']))

        #commit to DB
        mysql.connection.commit()

        #getting current number of queues
        results = cur.execute("SELECT * FROM total_queue")

        #Close connection
        cur.close()

        #get session student name for request type
        session["Student_name"] = Data["Student_name"]

        #Request advance enqires user about request type
        return redirect(url_for('request_advance'))

    return render_template('enduser/request_basic.html',form=form)

#Enduser fourth page. Filling out the forms.
@app.route('/request_advance',methods=['GET','POST'])
def request_advance():

    if request.method == 'POST':
        #Get the request type
        Request_type = request.form["Request_type"]

        #Create a dictionary cursor
        cur = mysql.connection.cursor()

        #get newest enduser number
        recent = cur.execute("SELECT * FROM total_queue WHERE Student_name=%s", [session['Student_name']])
        number = cur.fetchone()["Number"]

        cur.execute("UPDATE variables SET NUMBER=%s", [number] )

        #Execute SQL
        cur.execute("UPDATE total_queue SET Request_type=%s WHERE Student_name=%s",(Request_type,session["Student_name"]))

        #if there is the Request_type belongs to any of the department
        results = cur.execute("SELECT * FROM request_types WHERE Request_type=%s",[Request_type])
        department = cur.fetchone()["Department"]

        #update variables
        cur.execute("UPDATE variables SET DEPARTMENT=%s",[department])

        if department == 'Front Desk':
            cur.execute("INSERT INTO front_desk_queue(Number) VALUES(%s)",[number]) #record time in
        elif department == 'Accounting':
            cur.execute("INSERT INTO accounting_queue(Number) VALUES(%s)",[number])  #record time in

        #pop off, since we no longer need it
        session.pop('Student_name',None)

        #commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        #Flask message
        flash("Request Completed !", "success")

        #Return to index
        return redirect(url_for('select_language'))

    return render_template('enduser/request_advance.html')

#Admin Registeration page, can technically be accessed by anyone
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        Name = form.Name.data
        Email = form.Email.data
        Username = form.Username.data
        Password = sha256_crypt.encrypt(str(form.Password.data))
        Department = form.Department.data

        #Create DictCursor
        cur = mysql.connection.cursor()

        cur.execute("""INSERT INTO admins(Name, Email, Username, Password, Department)
        VALUES(%s, %s, %s, %s, %s)""", (Name, Email, Username, Password, Department))

        #commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        #Flash message
        flash("Registered as Admin !", "success")

        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form)

#admin login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        Username = request.form['Username']
        Password_Candidate = request.form['Password']

        cur = mysql.connection.cursor()

        results = cur.execute("SELECT * FROM admins WHERE Username=%s", [Username])

        if results > 0:
            data = cur.fetchone()
            Password = data['Password']
            Department = data['Department']

            if sha256_crypt.verify(Password_Candidate, Password):

                #Logged in
                session['logged_in'] = True
                session['username'] = Username
                session['department'] = Department

                flash("You are now logged in !  (◠‿◠✿)", 'success')
                return redirect(url_for('workspace'))
            else:
                error = 'Invalid Credentials. (◡︿◡✿)'
                return render_template('admin/login.html',error=error)

            cur.close()
        else:
            error = 'Username Not Found. ↁ_ↁ'
            return render_template('admin/login.html',error=error)

    return render_template('admin/login.html')

#admin logout
@app.route('/logout')
@login_required
def logout():
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

    #Select all data points from associated workspace
    results = cur.execute("""SELECT total_queue.Number, total_queue.User_type, total_queue.Request_type, total_queue.Parent_name, total_queue.Student_name, total_queue.Student_id, total_queue.Contact, total_queue.Status
    FROM total_queue JOIN (request_types)
    ON (total_queue.Request_type = request_types.Request_type)
    WHERE request_types.Department = %s AND total_queue.Status != %s """, (session["department"], 'Completed'))

    #Reassign
    if request.method == 'POST':
        #get variable
        Reassign = form.Reassign.data

        #fetch number
        cur.execute("SELECT NUMBER FROM variables")
        number = cur.fetchone()["NUMBER"]

        #Reassign
        cur.execute("UPDATE total_queue SET Request_type=%s WHERE Number=%s",([Reassign],[number]))

        #fetch new department
        data = cur.execute("SELECT * FROM request_types WHERE Request_type=%s", [Reassign])
        department = cur.fetchone()["Department"]

        #update department variable to new deparment
        cur.execute("UPDATE variables SET DEPARTMENT=%s",[department])

        #Inser number into database
        if department == "Front Desk":
            results = cur.execute("SELECT * FROM front_desk_queue WHERE Number=%s",[number])
            if results == 0:
                cur.execute("INSERT INTO front_desk_queue(Number) VALUES(%s)",[number])
                cur.execute("UPDATE accounting_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s", [number])
            else:
                cur.execute("UPDATE front_desk_queue SET Time_in=NOW() WHERE Number=%s", [number])
        elif department == "Accounting":
            results = cur.execute("SELECT * FROM accounting_queue WHERE Number=%s",[number])
            if results == 0:
                cur.execute("INSERT INTO accounting_queue(Number) VALUES(%s)",[number])
                cur.execute("UPDATE front_desk_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s", [number])
            else:
                cur.execute("UPDATE accounting_queue SET Time_in=NOW() WHERE Number=%s", [number])

        #flash message
        flash(number,"success")

        #commit to DB
        mysql.connection.commit()
        #flash message
        flash('Entry Reassigned! ', 'success')
        #return to dashboard
        return redirect(url_for('workspace'))

    #Fetch everything found
    queues = cur.fetchall()

    #if there is queue
    if results > 0:
        return render_template('admin/workspace.html',queues=queues,form=form)
    else:
        no_queue = " No Queue "
        return render_template('admin/workspace.html',no_queue=no_queue)

    #close the connection
    cur.close()

#admin call
@app.route('/entry_call/<string:number>', methods=['POST'])
@login_required
def entry_call(number):
    #Create dictionary cursor
    cur = mysql.connection.cursor()

    #Execute, delete and insert
    cur.execute("UPDATE total_queue SET Status=%s WHERE Number=%s",("In Progress",[number] ))

    #commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    #flash message
    flash('Entry Called! ', 'success')

    #return to dashboard
    return redirect(url_for('workspace'))

#admin store to archive
@app.route('/entry_complete/<string:number>', methods=['POST'])
@login_required
def entry_complete(number):
    #Create dictionary cursor
    cur = mysql.connection.cursor()

    #Execute, delete and insert
    cur.execute("UPDATE total_queue SET Status=%s WHERE Number=%s",('Completed',[number]))

    #check for deparment to include timestamp (going out) in
    if session["department"] == "Front Desk":
        cur.execute("UPDATE front_desk_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s",[number])
    elif session["department"] == "Accounting":
        cur.execute("UPDATE accounting_queue SET Time_out=NOW(), Time_diff=(Time_out - Time_in) WHERE Number=%s",[number])

    result1 = cur.execute("SELECT * FROM front_desk_queue WHERE Number=%s",[number])
    if result1 > 0:
        time1 = cur.fetchone()["Time_diff"]
    else:
        time1 = timedelta(0,0)
    result2= cur.execute("SELECT * FROM accounting_queue WHERE Number=%s",[number])
    if result2 > 0:
        time2 = cur.fetchone()["Time_diff"]
    else:
        time2 = timedelta(0,0)

    cur.execute("UPDATE total_queue SET Total_time = %s WHERE number=%s",([time1+time2],[number]))

    #commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    #flash message
    flash('Entry Completed! ', 'success')

    #return to dashboard
    return redirect(url_for('workspace'))


#request form class
class RequestForm(Form):
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


if __name__ == '__main__':
    app.run(debug = True)
