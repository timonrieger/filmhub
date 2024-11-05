from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange


class EditRatingForm(FlaskForm):
    rating = FloatField(label="Your Rating from 0 (worst) to 10 (best)", validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = StringField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")


class AddMovieForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Search Movie")


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = StringField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")


class RegistrationForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = StringField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Register")
