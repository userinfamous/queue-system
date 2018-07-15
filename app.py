from flask import Flask, render_template, redirect, flash, url_for, request, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, SelectField, IntegerField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = "i7T7e@CkqVkuHT5Lo9PH9xeg"
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'users'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index_choose_language():
    return render_template('enduser/select_language.html')

@app.route('/select_user_type')
def select_user_type():
    return render_template('enduser/select_user_type.html')

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

        flash("Admin Registered!", "success")

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
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Credentials. (◡︿◡✿)'
                return render_template('admin/login.html',error=error)

            cur.close()
        else:
            error = 'Username Not Found. ↁ_ↁ'
            return render_template('admin/login.html',error=error)

    return render_template('admin/login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

class RequestForm(Form):
    Parent_name = StringField('Full Name', [validators.Length(min=1,max=100)])
    Student_name = StringField('Full Name', [validators.Length(min=1,max=100)])
    Student_id = IntegerField('Student ID', [validators.NumberRange(min=0, max=10)] )

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
        choices = [(-1,'<Select Department>'),('acc_dp','Accounting Department'), ('fd_dp','Front Desk'), ('it_dp','IT Department')]
    )

if __name__ == '__main__':
    app.run()
