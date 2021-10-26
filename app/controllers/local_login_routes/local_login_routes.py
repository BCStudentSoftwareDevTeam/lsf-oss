from flask import request, flash, redirect, url_for
from is_safe_url import is_safe_url
from app.controllers.local_login_routes import *
# import app.login_manager as login_manager
from flask_login import current_user, login_user, login_required
from app.logic.localLogin import RegistrationForm, LoginForm
from app import config
from app.models.user import User

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
                    print("User logged in successfully: ", user.username)
                    login_user(user)

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
def register():
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


@local_login_bp.route('/logout', methods=['GET'])
def logout():
    return redirect(login_manager.logout())
