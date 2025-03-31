#!/usr/bin/python3
from data_entry import get_date, get_time, get_patient, get_purpose, get_phone, get_email, prompt_for_credentials
import sqlite3
import re
from email.message import EmailMessage
import ssl
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

def update_appointment(conn):
    # Show all appointments first
    show_query = "SELECT * FROM appointments"
    try:
        with conn:
            rows = conn.execute(show_query).fetchall()
            if not rows:
                print("\nNo appointments found.")
                return

            print("\nAppointments found:")
            for row in rows:
                id, date, time, patient, purpose, phone, email = row
                print(id, date, time, patient, purpose, phone, email, sep=' | ')
    
    except sqlite3.Error as e:
        print(f"Error fetching appointments: {e}")
        return

    # Get appointment ID from user
    while True:
        appointment_id = input("\nEnter the ID of the appointment to update or 'q' to quit: ").strip()

        if appointment_id.lower() == 'q':
            return

        if not appointment_id.isdigit():
            print("Invalid ID. Please enter a numeric ID.")
            continue

        appointment_id = int(appointment_id)

        # Check if the ID exists
        check_query = "SELECT * FROM appointments WHERE ID = ?"
        with conn:
            result = conn.execute(check_query, (appointment_id,)).fetchone()

        if not result:
            print(f"No appointment found with ID {appointment_id}. Please enter a valid ID.")
            continue
        
        break  # Valid ID found

    # Fields to update
    fields = {
        "Date": "date",
        "Time": "time",
        "Patient": "patient",
        "Purpose": "purpose",
        "Phone": "phone",
        "Email": "email"
    }

    updates = {}
    
    # Prompt user for new values
    for i, (label, field) in enumerate(fields.items(), start=1):
        new_value = input(f"Enter new {label} (press enter to keep current value '{result[i]}') or 'q' to quit: ").strip()
        if new_value == 'q':
            return
        if new_value:
            updates[field] = new_value

    if not updates:
        print("No changes made.")
        return

    # Construct SQL update query dynamically
    update_query = f"UPDATE appointments SET {', '.join(f'{key} = ?' for key in updates.keys())} WHERE ID = ?"
    update_values = list(updates.values()) + [appointment_id]

    try:
        with conn:
            conn.execute(update_query, update_values)
            conn.commit()
            print(f"Appointment with ID {appointment_id} updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating appointment: {e}")


def send_reminder_email(receiver_email, patient_name, app_date, app_time):
    # sender_email = 'p.opara@alustudent.com'
    # password = 'xbbz xpgd lxka hvpf'
    sender_email = 'luvel.remnder@gmail.com'
    password = 'jjka keni yshl hjkb'

    subject = 'LUVEL Clinic Appointment Reminder'
    body = f"""
    Dear {patient_name},
    This is a reminder that you have an appointment scheduled for {app_date} at {app_time}.
    """

    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(em)
        print(f"\nReminder to {patient_name} sent successfully.")
        print("Apologies for the interruption, \nPlease continue with the action you wanted to perform: ")
        # insert_appointment(get_connection())
        return