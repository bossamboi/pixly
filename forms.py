from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class EditImageForm(FlaskForm):
    """Form for editing an image."""

    sepia = BooleanField("Sepia")
    sketchify = BooleanField("Sketchify")
    frame = BooleanField("Frame")

    def validate(self, extra_validators=None):
        """Redefine validate method to require at least one selection"""
        if super().validate(extra_validators):

            if not (self.sepia.data or self.sketchify.data or self.frame.data):
                self.sepia.errors.append('Please pick at least one choice!')
                return False
            else:
                return True

        return False
