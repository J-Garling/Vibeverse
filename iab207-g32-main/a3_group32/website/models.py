from . import db
from datetime import datetime
from flask_login import UserMixin

# User class represents a user in the system, storing user information
# such as user's name, email, and hashed password. The User class is linked to 
# the Comment and Order classes, representing the user's comments and orders.
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  
    comments = db.relationship('Comment', backref='user')
    orders = db.relationship('Order', backref='user')

    def __repr__(self):
        return f"User: {self.name}"


# Event class represents an event in the system, storing information such as
# event's name, description, date, time, venue, and an image. It also 
# tracks comments and orders related to the event.
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(400))
    numberOfTickets = db.Column(db.Integer, nullable=False)  
    price_per_ticket = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Open")
    category = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='event')
    orders = db.relationship('Order', backref='event')

    def __repr__(self):
        return f"Event: {self.name} at {self.venue}"


# Comment class represents user comments on events, each comment is linked to
# both a user and an event, capturing who made the comment and which event it is 
# associated with. It stores the comment text and the timestamp of when the comment was made.
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text} by User {self.user_id} on Event {self.event_id}"


# Order class represents a users ticket order for an event,the number of tickets, the total cost of the order,
# and the relationships to both the user who made the order and the event for which
# the tickets were purchased.
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    ticket_quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    price_per_ticket = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Order: {self.id} for Event {self.event_id} by User {self.user_id}, Total: {self.total_amount}"