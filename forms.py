from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, EmailField, RadioField
from wtforms.validators import DataRequired, Email, Length

class EditImageForm(FlaskForm):
    """Form for editing an image."""

    filter = RadioField(validators=[DataRequired()], choices=["B/W", "Sepia", "None"])

    # username = StringField('Username', validators=[DataRequired()])
    # email = EmailField('E-mail', validators=[DataRequired(), Email()])
    # image_url = StringField('Profile Img URL (opt.)')
    # header_image_url = StringField('Background Img URL (opt.)')
    # bio = TextAreaField('Bio', validators=[DataRequired()])
    # password = PasswordField('Current Password', validators=[DataRequired(),
    #                                                             Length(min=6)])