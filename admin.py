from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models import db, Contact, Appointment
from datetime import datetime
from functools import wraps

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Simple authentication
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "mousam123"  # Change this to a secure password

def check_auth(username, password):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if check_auth(username, password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('admin/login.html')

@admin.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))

@admin.route('/dashboard')
@login_required
def dashboard():
    # Get all submissions
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
    
    return render_template('admin/dashboard.html', 
                         contacts=contacts, 
                         appointments=appointments)

@admin.route('/contacts')
@login_required
def contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

@admin.route('/appointments')
@login_required
def appointments():
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
    return render_template('admin/appointments.html', appointments=appointments) 