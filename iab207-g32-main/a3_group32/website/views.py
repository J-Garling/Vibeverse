from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = db.session.scalars(db.select(Event).where(Event.status=='Open')) 
    return render_template('index.html', events=events)

@main_bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(Event.description.like(query)))
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))
    
# Route to filter events by category
@main_bp.route('/filter', methods=['GET'])
def filter_events():
    # Get the selected category from the dropdown
    category = request.args.get('categorySelect')
    #If a category is selected, filter the events
    if category:
       events = Event.query.filter_by(category=category).all()  # Assuming category is part of Event model
       return render_template('index.html', events=events)
    else:
       events = Event.query.all()  # Otherwise, show all events
    # Render the index page with filtered or all events
    return redirect(url_for('main.index'))