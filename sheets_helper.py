import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def setup_google_sheets():
    """Setup Google Sheets connection"""
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # You'll need to create a service account and download the JSON key file
    # For now, we'll use a placeholder
    credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(credentials)
    return client

def add_contact_to_sheet(client, contact_data):
    """Add contact form submission to Google Sheet"""
    try:
        # Replace 'Contact Form Submissions' with your actual sheet name
        sheet = client.open('Mousam In Abroad - Contact Form').sheet1
        
        # Add data to sheet
        row = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            contact_data['name'],
            contact_data['email'],
            contact_data['subject'],
            contact_data['message']
        ]
        sheet.append_row(row)
        return True
    except Exception as e:
        print(f"Error adding to Google Sheets: {e}")
        return False

def add_appointment_to_sheet(client, appointment_data):
    """Add appointment booking to Google Sheet"""
    try:
        # Replace 'Appointment Bookings' with your actual sheet name
        sheet = client.open('Mousam In Abroad - Appointments').sheet1
        
        # Add data to sheet
        row = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            appointment_data['full_name'],
            appointment_data['email'],
            appointment_data['country'],
            appointment_data['marks'],
            appointment_data['course'],
            appointment_data['intake'],
            appointment_data['services'],
            appointment_data['concerns']
        ]
        sheet.append_row(row)
        return True
    except Exception as e:
        print(f"Error adding to Google Sheets: {e}")
        return False 