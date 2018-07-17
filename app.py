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

#Enduser index page
@app.route('/')
def index_choose_language():
    return render_template('enduser/select_language.html')

#Enduser select user type page. (parent/student/visitor)
@app.route('/select_user_type', methods=['GET','POST'])
def select_user_type():
    if request.method == 'POST':
        Session['User_type'] = request.form['User_type']
        return redirect(url_for('request'))
    return render_template('enduser/select_user_type.html')

@app.route('/request',methods=['GET','POST'])
def request():
    #Making form an object of a class
    form = RequestForm(request.form)

    if request.method == 'POST':
        Fullname = form.Name.data
        Student_name = form.Email.data
        Student_id = form.Username.data

        #Create DictCursor
        cur = mysql.connection.cursor()

        cur.execute("""INSERT INTO queue(Fullname, Student_name, Student_id)
        VALUES(%s, %s, %s)""", (Fullname, Student_name, Student_id))

        #commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash("Request Completed !", "success")

        return redirect(url_for('select_language'))
    return render_template('enduser/request.html', form=form)



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

        flash("Registered as Admin !", "success")

        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        Username = request.form['Username']
        Password_Candidate = request.form['Password']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM admins WHERE Username=%s", [Username])

        if result > 0:
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

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out.', 'success')
    return redirect(url_for('login'))



@app.route('/workspace')
def workspace():
    return render_template('admin/workspace.html')

class RequestForm(Form):
    Fullname = StringField('Full Name',[
        validators.DataRequired(),
        validators.Length(min=1,max=100)])
    Student_name = StringField('Student Name',[
        validators.DataRequired(),
        validators.Length(min=1,max=100)])
    Student_id = IntegerField('Student ID',[
        validators.NumberRange(min=0, max=10)] )


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
    app.run()
