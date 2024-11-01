from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG','JPG','png','jpg'}

# Create new event
class EventForm(FlaskForm):
  name = StringField('Event Title', validators=[InputRequired()], render_kw={"class": "inputField"})
  description = TextAreaField('Description', validators = [InputRequired()], render_kw={"class": "inputField"})
  category = SelectField('Category', choices=[('Concert'), ('Festival'), ('POP'), ('R&B'), ('Country'), ('Alternative')], render_kw={"class": "inputField"})
  date = DateField('Date', validators = [InputRequired()], render_kw={"class": "inputField"})
  start_time = TimeField('Start time', validators = [InputRequired()], render_kw={"class": "inputField"})
  end_time = TimeField('End time', validators = [InputRequired()], render_kw={"class": "inputField"})
  venue = TextAreaField('Venue', validators = [InputRequired()], render_kw={"class": "inputField"})
  image = FileField('Event Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only PNG or JPG files allowed')], render_kw={"class": "inputField"})
  numberOfTickets = IntegerField('Number of Tickets', validators = [NumberRange(min=1)], render_kw={"class": "inputField"})
  price_per_ticket = IntegerField('Price per Ticket (AUD)', validators = [NumberRange(min=1)], render_kw={"class": "inputField"})
  submit = SubmitField("Post") 

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')],
                          render_kw={"class": "inputField"})
    password=PasswordField("Password", validators=[InputRequired('Enter user password')],
                           render_kw={"class": "inputField"})
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()],
                          render_kw={"class": "inputField"})
    email = StringField("Email Address", validators=[Email("Please enter a valid email")],
                        render_kw={"class": "inputField"})
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")],
                           render_kw={"class": "inputField"})
    confirm = PasswordField("Confirm Password", render_kw={"class": "inputField"})

    # submit button
    submit = SubmitField("Register")

# creates the form for the comments component
class CommentForm(FlaskForm):
    text = TextAreaField("Comment", validators=[InputRequired(), Length(max=400)])
    submit = SubmitField("Post Comment")
    

# forms for place order
class OrderForm(FlaskForm):
    ticket_quantity = IntegerField('Number of Tickets you wish to order', validators=[InputRequired()], render_kw={"class": "inputField"})
    submit = SubmitField("Place Order")

  