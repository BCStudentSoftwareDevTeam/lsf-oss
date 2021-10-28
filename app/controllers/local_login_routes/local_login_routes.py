from flask import request, flash, redirect, url_for, session, abort
from is_safe_url import is_safe_url
from app.controllers.local_login_routes import *
# import app.login_manager as login_manager
from flask_login import current_user, login_user, login_required, logout_user
from app import config
# from app import login_mgr
from app.models.user import User
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField, TextField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from app.login_manager import require_login

# NOTE: These classes work with Flask Login to generate the forms
class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password',
                            [validators.DataRequired(),
                            validators.EqualTo('confirm',
                            message='Passwords must match')]
                            )
    confirm = PasswordField('Repeat Password')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(RegistrationForm, self).validate()
        if not initial_validation:
            return False
        user = User.get_or_none(username=self.username.data)
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.get_or_none(email=self.email.data)
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True

class LoginForm(Form):
    email = TextField('email',
            validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            print("Failed initial validation:", initial_validation)
            return False
        user = User.get(email=self.email.data)
        if not user:
            print("unknown email: ", self.email.data)
            self.email.errors.append('Unknown email')
            return False
        if not user.verify_password(self.password.data):
            print("unknown password: ", self.password.data)
            self.password.errors.append('Invalid password')
            return False
        print('validation passed')
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
                    flash('Logged in successfully.')

                    next = request.args.get('next')
                    # if not is_safe_url(next):
                    #     return abort(400)

                return redirect(next or url_for('main.index'))
        else:
            print("User failed to log in successfully")
            form = LoginForm()
            return render_template("local_login/localLogin.html", form=form)


@local_login_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    currentUser = require_login()
    print(currentUser)
    if currentUser.isLaborAdmin:
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            # Insert the user
            newUser = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
            newUser.save()
            flash('Thanks for registering')
            return redirect(url_for('local_login.login'))
        return render_template('local_login/localRegister.html', form=form)
    return abort(403)


@local_login_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for("local_login.login"))
