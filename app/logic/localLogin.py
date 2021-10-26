from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField, TextField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from app.models.user import User

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
