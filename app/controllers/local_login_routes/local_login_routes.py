from flask import request, flash, redirect, url_for, session, abort
from peewee import fn
from is_safe_url import is_safe_url
from app.controllers.local_login_routes import *
# import app.login_manager as login_manager
from flask_login import current_user, login_user, login_required, logout_user
from app import config
# from app import login_mgr
from app.models.user import User
from app.models.supervisor import Supervisor
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField, TextField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from app.login_manager import require_login

# NOTE: These classes work with Flask Login to generate the forms
class RegistrationForm(Form):
    supervisors = TextAreaField('Supervisors',
                                [validators.Length(max=2500)],
                                description = "Paste in supervisors, one per line",
                                render_kw = {"placeholder": "Paste in supervisors, one per line. See below for format and examples:",
                                             "class": "form-control col-md-6",
                                             "style": "height: 10em"
                                          },
                                )
    students = TextAreaField('Students',
                             [validators.Length(max=2500)],
                             description = "Paste in students, one per line",
                             render_kw = {"placeholder": "Paste in students, one per line.  See below for format and examples:",
                                          "class": "form-control col-md-6",
                                          "style": "height: 10em"
                                        },
                             )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def validateSupervisors(self, supervisorData):
        # users = supervisorData.split("\r\n")
        for user in supervisorData:
            user = user.split(",")
            # id = user[0]
            # username = user[1]
            # email = user[2]
            if user[0] == "":
                print("Skipping blank line")
            else:
                if len(user) != 3:
                    flash("Invalid format, see examples below", "danger")
                    return False
                userCheck = User.get_or_none(supervisor = user[0])
                if userCheck:
                    flash("Supervisor ID already registered: {}".format(userCheck.supervisor), "danger")
                    return False
                userCheck = User.get_or_none(username=user[1])
                if userCheck:
                    # TODO Handle supervisor becoming a student also
                    flash("Username already registered: {}".format(userCheck.username), "danger")
                    return False
                userCheck = User.get_or_none(email=user[2])
                if userCheck:
                    flash("Email already registered: {}".format(userCheck.email), "danger")
                    return False
        return True

    def validateStudents(self, studentData):
        # users = studentData.split("\r\n")
        for user in studentData:
            user = user.split(",")
            # id = user[0]
            # username = user[1]
            # email = user[2]
            if len(user) != 3:
                flash("Invalid format, see examples below", "danger")
                return False
            userCheck = User.get_or_none(student = user[0])
            if userCheck:
                flash("Student ID already registered: {}".format(userCheck.student), "danger")
                return False
            userCheck = User.get_or_none(username=user[1])
            if userCheck:
                # TODO Handle student becoming a supervisor also
                flash("Username already registered: {}".format(userCheck.username), "danger")
                return False
            userCheck = User.get_or_none(email=user[2])
            if userCheck:
                flash("Email already registered: {}".format(userCheck.email), "danger")
                return False
        return True

    def validate(self):
        # TODO Validate each entry to ensure they aren't in the DB
        initial_validation = super(RegistrationForm, self).validate()
        if not initial_validation:
            print("Failed initial validation in RegistrationForm")
            return False
        # print(self.supervisors.data.split("\r\n")[0])
        if self.supervisors.data != '' and self.students.data != '':
            flash("Both fields are empty, doing nothing", "danger")
            return False
        if self.supervisors.data != '':
            # Restructure the data into a list of entries to add
            self.supervisors.data = self.supervisors.data.split("\r\n")   # ['bnum1, id1, email1', 'bnum2, id2, email2']
            while "" in self.supervisors.data:
                self.supervisors.data.remove("")
            if self.validateSupervisors(self.supervisors.data):
                print("Supervisor field valid")
            else:
                return False
        if self.students.data != '':
            # Restructure the data into a list of entries to add
            self.students.data = self.students.data.split("\r\n")   # ['bnum1, id1, email1', 'bnum2, id2, email2']
            while "" in self.students.data:
                self.students.data.remove("")
            if self.validateStudents(self.students.data):
                print("Students field valid")
                # TODO Flash no supervisors?
            else:
                return False
        return True

@local_login_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    currentUser = require_login()
    # print(currentUser)
    if currentUser.isLaborAdmin:
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            # Insert the Supervisors
            count = 0
            for supervisor in form.supervisors.data:
                supervisor = supervisor.split(",")
                newSupervisor, created = Supervisor.get_or_create(ID = supervisor[0],
                                        EMAIL = supervisor[2]
                                        )
                newUser = User(email = newSupervisor.EMAIL,
                        username = supervisor[1],
                        supervisor = newSupervisor.ID)
                newUser.save()
                count += 1

            flash('Thanks for registering {0} user(s)'.format(count), "success")
            return redirect(url_for('local_login.register'))
        return render_template('local_login/localRegister.html', form=form, currentUser = currentUser)
    return abort(403)


################################################################################
class LoginForm(Form):
    email = TextField('E-mail',
                      render_kw = {"placeholder": "Enter your email address:",
                                 "class": "form-control col-md-6"
                              },
                              validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password',
                             render_kw = {"placeholder": "Enter your password:",
                                         "class": "form-control col-md-6"
                                      },
                             validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            print("Failed initial validation:", initial_validation)
            return False
        user = User.get_or_none(email=self.email.data)
        if not user:
            print("Unknown email: ", self.email.data)
            self.email.errors.append('Unknown email')
            return False
        if not user.verify_password(self.password.data):
            print("Unknown password: ", self.password.data)
            self.password.errors.append('Invalid password')
            return False
        print('Validation passed')
        return True


################################################################################
class RegisterFirstTimeForm(Form):
    firstName = TextField('First Name',
                          render_kw = {"placeholder": "Enter your first name:",
                                 "class": "form-control col-md-6"},
                          validators = [DataRequired(), Length(1, 64)])
    lastName = TextField('Last Name',
                          render_kw = {"placeholder": "Enter your last name:",
                                 "class": "form-control col-md-6"},
                          validators = [DataRequired(), Length(1, 64)])
    username = TextField('Username',
                         render_kw = {"placeholder": "Enter your username:",
                                 "class": "form-control col-md-6"},
                         validators = [DataRequired(), Length(1, 64)])
    email = TextField('E-mail',
                      render_kw = {"placeholder": "Enter your email address:",
                                 "class": "form-control col-md-6"},
                      validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password',
                             render_kw = {"placeholder": "Enter your password:",
                                 "class": "form-control col-md-6"},
                             validators=[DataRequired()])
    submit = SubmitField('Register the First Administrator',
                         render_kw = {"class": "btn btn-success",
                                      "type": "submit"})

    def __init__(self, *args, **kwargs):
       super(RegisterFirstTimeForm, self).__init__(*args, **kwargs)

    def validate(self):
       initial_validation = super(RegisterFirstTimeForm, self).validate()
       if not initial_validation:
           print("Failed initial validation:", initial_validation)
           return False
       return True


@local_login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if config["USE_SHIBBOLETH"] == 0: # local login
        if request.method == "POST":
            form = LoginForm(request.form)
            if form.validate():
                print("form validated")
                # Login and validate the user.
                # user should be an instance of your `User` class
                user = User.get(email=form.email.data)
                if user is not None and user.verify_password(form.password.data):
                    login_user(user)
                    session['username'] = user.username
                    print("User logged in successfully: ", user.username)
                    flash('Logged in successfully.', "success")

                    next = request.args.get('next')
                    # if not is_safe_url(next):
                    #     return abort(400)

                return redirect(next or url_for('main.index'))
            else:
                flash("User failed to log in successfully", "danger")
                form = LoginForm()
                return render_template("local_login/localLogin.html", form=form)
        else:
            # No current logged in user
            users_exist = False
            if User.select(fn.COUNT(User.isLaborAdmin)).where(User.isLaborAdmin == 1).scalar() > 0:
                print("We got an admin!")
                form = LoginForm()
                users_exist = True
                return render_template("local_login/localLogin.html", form=form, users_exist = users_exist)
            else:
                print("No admins exist yet")
                return redirect(url_for('local_login.localRegisterFirstUser'))


@local_login_bp.route('/localRegisterFirstUser', methods=['GET', 'POST'])
def localRegisterFirstUser():
    if config["USE_SHIBBOLETH"] == 0: # local login
        if request.method == "POST":
            form = RegisterFirstTimeForm(request.form)
            if form.validate():
                print("First time registering form validated")
                newSupervisor, created = Supervisor.get_or_create(ID = form.username.data,
                                        EMAIL = form.email.data,
                                        FIRST_NAME = form.firstName.data,
                                        LAST_NAME = form.lastName.data
                                        )
                newUser = User(email = newSupervisor.EMAIL,
                        username = form.username.data,
                        supervisor = newSupervisor.ID,
                        isLaborAdmin = 1)
                newUser.password = form.password.data
                newUser.save()
            flash("New Administrator created successfully! Please log in now.", "success")
            return redirect(url_for("local_login.login"))
        if User.select(fn.COUNT(User.isLaborAdmin)).where(User.isLaborAdmin == 1).scalar() > 0:
            print("We got an admin!")
            return redirect(url_for("local_login.login"))
        else:
            form = RegisterFirstTimeForm()
            return render_template("local_login/localRegisterFirstUser.html", form = form)
    flash("Ah crap", "danger")
    return (abort(500))


@local_login_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for("local_login.login"))
