from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, URL, Optional


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[InputRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)],
    )

    email = StringField(
        'E-mail',
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=50)],
    )

    image_url = StringField(
        '(Optional) Image URL',
        validators=[Optional(), URL(), Length(max=255)]
    )


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=50)],
    )


class UpdateUserForm(FlaskForm):
    """ Update user form """

    email = StringField(
        'E-mail',
        validators=[Email(), Length(max=50)], #TODO:// make required so they can't put an empty string
    )

    username = StringField(
        'Username',
        validators=[Length(max=30)], #TODO:// make required so they can't put an empty string
    )

    #TODO:// Optional validator in front, make sure defaults are working (route?)
    image_url = StringField(
        'Image URL (optional)',
        validators=[URL(), Length(max=255)]
    )
    #TODO:// Optional validator in front, make sure defaults are working (route?)
    header_image_url = StringField(
        'Image URL (optional)',
        validators=[URL(), Length(max=255)]
    )

    bio = TextAreaField(
        'Bio',
    )

    # not sure if this is working as intended
    password = PasswordField(
        'Password',
        validators=[Length(min=6, max=50)] #TODO:// make required
    )



class CSRFProtectForm(FlaskForm):
    """ Form just for CSRF Protection """