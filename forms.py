from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired


# WTForm for logging in existing users
class LoginForm(FlaskForm):
    matric_no = StringField("Matric Number", validators=[DataRequired()])
    pin = PasswordField("Pin", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")
    
# WTForm for voting for candidates
class VoteForm(FlaskForm):
    candidate_id = HiddenField("Candidate ID")
    submit = SubmitField("Vote")
