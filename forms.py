from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class EditImageForm(FlaskForm):
    """Form for editing an image."""

    # filter = RadioField("Filter", validators=[DataRequired()], choices=["B/W", "Sepia", "None"])
    # filter = SelectField("Editing Options", validators=[DataRequired()], choices=["Sepia", "Sketchify", "Frame"])
    sepia = BooleanField("Sepia")
    sketchify = BooleanField("Sketchify")
    frame = BooleanField("Frame")

    def validate(self, extra_validators=None):
        if super().validate(extra_validators):

            # your logic here e.g.
            if not (self.sepia.data or self.sketchify.data or self.frame.data):
                self.sepia.errors.append('Please pick at least one choice!')
                return False
            else:
                return True

        return False
    # username = StringField('Username', validators=[DataRequired()])
    # email = EmailField('E-mail', validators=[DataRequired(), Email()])
    # image_url = StringField('Profile Img URL (opt.)')
    # header_image_url = StringField('Background Img URL (opt.)')
    # bio = TextAreaField('Bio', validators=[DataRequired()])
    # password = PasswordField('Current Password', validators=[DataRequired(),
    #                                                             Length(min=6)])