#Author: Vuottek Un
#Project Title: Queue-System
#Description:
#   The upper parts are imports and declaration of the app
#   after that, comes all the features that we implement.
#   Then there's the classes, and at the bottom is the app.run() itself.

#Importing necessary dependencies for the project
from flask import Flask, render_template, redirect, flash, url_for, request, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, SelectField, IntegerField, PasswordField, validators
from passlib.hash import sha256_crypt
from helpers import login_required, collect_form_data

import pusher

pusher_client = pusher.Pusher(
  app_id='565012',
  key='eefbd3472aabb2b3fc60',
  secret='847a073500e5464a47f9',
  cluster='ap1',
  ssl=True
)

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
        return redirect(url_for('request_info'))
    return render_template('enduser/select_user_type.html')


#Enduser third page. Filling out the forms.
@app.route('/request_info',methods=['GET','POST'])
def request_info():

    form = RequestForm(request.form)
    if request.method == 'POST':
        #Loaded script from helpers to reduce messiness
        Data = collect_form_data(form)

        #Create a dictionary cursor
        cur = mysql.connection.cursor()

        #Check for duplicates
        check = cur.execute("SELECT * FROM queue WHERE Student_name=%s",[Data['Student_name']] )

        if check > 0:
            #Flask message
            flash("Request Failed Duplicates Sent !", "danger")
            #Close connection
            cur.close()
            
            return redirect(url_for('select_language'))

        #Update the database
        cur.execute("""INSERT INTO queue(User_type,Parent_name, Student_name, Student_id, Contact)
        VALUES(%s, %s, %s, %s, %s)""", (session["User_type"], Data['Parent_name'], Data['Student_name'], Data['Student_id'],  Data['Contact']))

        results = cur.execute("SELECT * FROM queue")

        #commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        #Flask message
        flash("Request Completed !", "success")

        #clearning 'undefine' out of real time interface
        pusher_client.trigger('queue-channel', 'queue-event', {
            'Number': results,
            'User_type': session['User_type'],
            'Parent_name': Data['Parent_name'],
            'Student_name': Data['Student_name'],
            'Student_id': Data['Student_id'],
            'Contact': Data['Contact'],
            'Request_type': '',
            'Status': ''
        })

        return redirect(url_for('select_language'))

    return render_template('enduser/request_info.html',form=form)

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

            if sha256_crypt.verify(Password_Candidate, Password):
                #Logged in
                session['logged_in'] = True
                session['username'] = Username

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
@app.route('/workspace')
@login_required
def workspace():

    cur = mysql.connection.cursor()
    results = cur.execute("SELECT * FROM queue")
    queues = cur.fetchall()

    if results > 0:
        return render_template('admin/workspace.html',queues=queues)
    else:
        no_queue = " No Queue "
        return render_template('admin/workspace.html',no_queue=no_queue)
    cur.close()

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
        choices = [(-1,'<Select Department>'),('Accounting Department','Accounting Department'), ('Front Desk','Front Desk'), ('IT Department','IT Department')]
    )

if __name__ == '__main__':
    app.run(debug = True)
