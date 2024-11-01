from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from .models import Event, Comment, Order, User
from .forms import EventForm, CommentForm, OrderForm
from datetime import datetime
from . import db
import os
from werkzeug.utils import secure_filename
# additional import:
from flask_login import login_required, current_user


# Create the event blueprint
event_bp = Blueprint('event', __name__, url_prefix='/events')

# route to display all events in the database
@event_bp.route('/show_all')
def show_all():
    events = db.session.scalars(db.select(Event).where(Event.status=='Open'))
    if not events:
        abort(404)
    return render_template('events/show_all.html', events=events)

# route to display all details of a selected event
@event_bp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    comments = db.session.scalars(db.select(Comment).where(Comment.event_id==id)).all()
    form = CommentForm()
    form2 = OrderForm() 
    if not event:
       abort(404)
    return render_template('events/show_id.html', event=event, comments=comments, form=form, form2=form2)


#route to create events - user must be logged in  
@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        # call the function that checks and returns image
        db_file_path = check_upload_file(form)
        event = Event(name=form.name.data,description=form.description.data, category=form.category.data,
        date=form.date.data,start_time=form.start_time.data, end_time=form.end_time.data, 
        venue=form.venue.data,image=db_file_path,numberOfTickets=form.numberOfTickets.data,
        price_per_ticket=form.price_per_ticket.data,status="Open", user_id=current_user.id)
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()
        flash('Successfully created new vibeverse event', 'success')
        return redirect(url_for('event.create'))
    return render_template('events/create_event.html', form=form)

def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/' + secure_filename(filename)
  # save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

#route to create comments on a selected event. User must be logged in to comment 
@event_bp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):
    form = CommentForm()
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, user_id=current_user.id, event=event)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully', 'success')
    return redirect(url_for('event.show', id=id))

#route to display all events created by the logged in user
@event_bp.route('/created_events', methods=['GET', 'POST'])
@login_required
def created_events():
    open_events = db.session.scalars(db.select(Event).where(Event.status=='Open', Event.user_id==current_user.id))
    not_open_events = db.session.scalars(db.select(Event).where(Event.status!='Open', Event.user_id==current_user.id))
    return render_template('events/created_events.html', open_events=open_events, not_open_events=not_open_events)


#route to edit an event that a logged in user has created
@event_bp.route('/created_events/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    form = EventForm()    
    if form.validate_on_submit():  
        db_file_path = check_upload_file(form)
        name=form.name.data
        description=form.description.data
        category=form.category.data
        date=form.date.data
        start_time=form.start_time.data
        end_time=form.end_time.data 
        venue=form.venue.data
        image=db_file_path
        numberOfTickets=form.numberOfTickets.data
        price_per_ticket=form.price_per_ticket.data
        status="Open"
        user_id=current_user.id

        event.name = name
        event.description = description
        event.category=category
        event.date = date
        event.start_time = start_time
        event.end_time = end_time
        event.venue = venue
        event.image = image
        event.numberOfTickets = numberOfTickets
        event.price_per_ticket = price_per_ticket
        event.status = status
        event.user_id = user_id

        db.session.commit()
        flash('Event edited successfully', 'success')
        return redirect(url_for('event.created_events'))
    return render_template('events/edit.html', event=event, form=form)


#route for when a user selects to cancel an event, will redirect to an 'are you sure' page
@event_bp.route('/created_events/<id>/cancel_request', methods=['GET', 'POST'])
@login_required
def cancel_request(id):
    event=db.session.scalar(db.select(Event).where(Event.id==id, Event.user_id==current_user.id))
    return render_template('events/cancel.html', event=event)


#function for changing the status to cancelled when a user wishes to cancel an event
@event_bp.route('/created_events/<id>/cancel', methods=['GET', 'POST'])
@login_required
def cancel(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id, Event.user_id==current_user.id))
    status="Cancelled"

    event.status = status
    db.session.commit()
    flash('Event cancelled successfully', 'success')
    return render_template('events/cancel.html', event=event)


#function for ordering tickets on a paticular event
@event_bp.route('/<id>/order', methods=['GET', 'POST'])  
@login_required
def order(id):
    form2 = OrderForm()
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form2.validate_on_submit():
        order = Order(order_date=datetime.now(), ticket_quantity=form2.ticket_quantity.data, price_per_ticket=event.price_per_ticket,
                      total_amount=form2.ticket_quantity.data*event.price_per_ticket, user_id=current_user.id, event_id=event.id)
        db.session.add(order)
        db.session.commit()
        flash('Order added successfully', 'success')
    return redirect(url_for('event.order_history'))

#route to view order history of a logged in user
@event_bp.route('order_history', methods=['GET', 'POST'])
@login_required
def order_history():
    orders = db.session.scalars(db.select(Order).where(Order.user_id==current_user.id))
    return render_template('histories/booking_history.html', orders=orders)

