#Helpers functions
from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(f):
    #Decorate or alter the functionality of login
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unathorized, Please login.', 'danger')
            return redirect(url_for('login'))
    return wrap

def collect_form_data(form):
    Parent_name,Student_name,Student_id,Contact = "","","",""
    #handling translation cases
    if session["Selected_language"] == 'English':

        if session["User_type"] == "Parent":
            Contact = "Unspecified"
            Parent_name = form.en_Parent_name.data
            if form.en_Student_id == None:
                Student_id = "Unspecified"
            else:
                Student_id = form.en_Student_id.data

        if session["User_type"] == "Student":
            Contact = "Unspecified"
            Parent_name = "Unspecified"
            if form.en_Student_id.data == None:
                Student_id = "Unspecified"
            else:
                Student_id = form.en_Student_id.data

        if session["User_type"] == "Visitor":
            Student_id = "Unspecified"
            Parent_name = form.en_Parent_name.data
            if form.en_Contact.data == None:
                Contact = "Unspecified"
            else:
                Contact = form.en_Contact.data

        Student_name = form.en_Student_name.data

    else: #Khmer form data

        if session["User_type"] == "Parent":
            Contact = "Unspecified"
            Parent_name = form.kh_Parent_name.data
            if form.kh_Student_id == None:
                Student_id = "Unspecified"
            else:
                Student_id = form.kh_Student_id.data

        if session["User_type"] == "Student":
            Contact = "Unspecified"
            Parent_name = "Unspecified"
            if form.kh_Student_id.data == None:
                Student_id = "Unspecified"
            else:
                Student_id = form.kh_Student_id.data

        if session["User_type"] == "Visitor":
            Student_id = "Unspecified"
            Parent_name = form.kh_Parent_name.data
            if form.kh_Contact.data == None:
                Contact = "Unspecified"
            else:
                Contact = form.kh_Contact.data

        Student_name = form.kh_Student_name.data

    return {'Parent_name':Parent_name, 'Student_name':Student_name, 'Student_id':Student_id, 'Contact':Contact}
