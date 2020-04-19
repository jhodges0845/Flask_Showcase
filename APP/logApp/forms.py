from flask_wtf import FlaskForm
from APP.models import User, Log
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class LogForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=3, max=500)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField("Create")