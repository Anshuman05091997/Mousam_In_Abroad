from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email
from models import db, Contact, Appointment
from admin import admin, check_auth
# from sheets_helper import setup_google_sheets, add_contact_to_sheet, add_appointment_to_sheet
from chatbot import Chatbot
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mousam.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Initialize Google Sheets client
# try:
#     sheets_client = setup_google_sheets()
# except Exception as e:
#     print(f"Google Sheets setup failed: {e}")
#     sheets_client = None
sheets_client = None

# Initialize chatbot
chatbot = Chatbot()

# Register admin blueprint
app.register_blueprint(admin)

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

# Forms
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject')
    message = TextAreaField('Message', validators=[DataRequired()])

class AppointmentForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    country = StringField('Country')
    marks = StringField('Marks/Percentage')
    course = StringField('Course Interested In')
    intake = SelectField('Preferred Intake', choices=[
        ('winter', 'Winter Semester'),
        ('summer', 'Summer Semester')
    ])
    services = SelectMultipleField('Services Needed', choices=[
        ('university', 'University Guidance'),
        ('visa', 'Visa & APS Support'),
        ('insurance', 'Health Insurance'),
        ('blocked_account', 'Blocked Account'),
        ('accommodation', 'Accommodation'),
        ('pre_arrival', 'Pre/Post Arrival Help')
    ])
    concerns = TextAreaField('Your Biggest Concern')

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chatbot messages"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    if user_message:
        bot_response = chatbot.get_response(user_message)
        return jsonify({'response': bot_response})
    
    return jsonify({'response': 'Sorry, I didn\'t understand that. Could you please rephrase?'})

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Save to database
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact)  # type: ignore
        db.session.commit()  # type: ignore

        # Add to Google Sheets
        # if sheets_client:
        #     contact_data = {
        #         'name': form.name.data,
        #         'email': form.email.data,
        #         'subject': form.subject.data,
        #         'message': form.message.data
        #     }
        #     add_contact_to_sheet(sheets_client, contact_data)

        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        # Save to database
        appointment = Appointment(
            full_name=form.full_name.data,
            email=form.email.data,
            country=form.country.data,
            marks=form.marks.data,
            course=form.course.data,
            intake=form.intake.data,
            services=','.join(form.services.data) if form.services.data else '',
            concerns=form.concerns.data
        )
        db.session.add(appointment)  # type: ignore
        db.session.commit()  # type: ignore

        # Add to Google Sheets
        # if sheets_client:
        #     appointment_data = {
        #         'full_name': form.full_name.data,
        #         'email': form.email.data,
        #         'country': form.country.data,
        #         'marks': form.marks.data,
        #         'course': form.course.data,
        #         'intake': form.intake.data,
        #         'services': ', '.join(form.services.data) if form.services.data else 'None',
        #         'concerns': form.concerns.data
        #     }
        #     add_appointment_to_sheet(sheets_client, appointment_data)

        flash('Your appointment has been booked! We will contact you shortly.', 'success')
        return redirect(url_for('appointment'))
    return render_template('appointment.html', form=form)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 