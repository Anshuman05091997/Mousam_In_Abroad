# Mousam In Abroad

A website for an education consultancy helping Indian students study in Germany.

## Features

- Contact form for inquiries
- Appointment booking system
- Multilingual chatbot (English, Hindi, German)
- Admin dashboard for managing submissions
- Responsive design with Tailwind CSS

## Tech Stack

- Backend: Flask (Python)
- Database: SQLite (Development) / PostgreSQL (Production)
- Frontend: HTML, Tailwind CSS, JavaScript
- Deployment: Render.com

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Visit http://localhost:5000

## Deployment Instructions

1. Create an account on [Render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add Environment Variables:
   - `SECRET_KEY`: [Generate a secure key]
   - `ADMIN_USERNAME`: Your admin username
   - `ADMIN_PASSWORD`: Your admin password

## Admin Access

Default credentials (change these in production):
- Username: admin
- Password: mousam123

## Contact

For support or inquiries:
- Email: mousaminabroad@gmail.com
- WhatsApp: +49 1575 9876543