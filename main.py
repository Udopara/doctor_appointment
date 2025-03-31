#!/usr/bin/python3
from data_entry import get_date, get_time, get_patient, get_purpose, get_phone, get_email, prompt_for_credentials
import sqlite3
import re
from email.message import EmailMessage
import ssl
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

def is_valid_date(date_str):
    """Check if the input follows the YYYY-MM-DD format using regex."""
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str))

def compare_dates(start_date, end_date):
    """Ensure end_date is not earlier than start_date."""
    return start_date <= end_date

def get_connection():
    try:
        conn = sqlite3.connect('luvel.db')
        print("Connected to SQLite successfully!")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None
    
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Date TEXT NOT NULL,
                Time TEXT NOT NULL,
                Patient TEXT NOT NULL,
                Purpose TEXT NOT NULL,
                Phone INTEGER NOT NULL,
                Email TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Table created successfully!")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def insert_appointment(conn):
    functions = [get_date, get_time, get_patient, get_purpose, get_phone, get_email]  # List of functions to get input from the user
    fields = ['date', 'time', 'patient', 'purpose', 'phone', 'email']  # Corresponding fields in the dictionary


    # Initialize a dictionary for the new appointment
    new_appointment = {}

    # Iterate through functions and fields
    for function, field in zip(functions, fields):
        result = function()  # Call the function to get the user input
        if result == 'q':  # If user enters 'q', return and exit
            return
        new_appointment[field] = result  # Assign the result to the corresponding field in the dictionary
    query = """
INSERT INTO appointments(date, time, patient, purpose, phone, email) VALUES (?, ?, ?, ?, ?, ?)
"""
    try:
        with conn:
            conn.execute(query, (new_appointment[fields[0]], new_appointment[fields[1]], new_appointment[fields[2]], new_appointment[fields[3]], new_appointment[fields[4]], new_appointment[fields[5]]))
            print("Appointment sucessfully added")
    except Exception as e:
        print('error is', e)

def fetch_appointments(conn):
    patient = input("Enter the patient name or press enter to skip or 'q' to quit: ").strip()
    if patient.lower() == 'q':
        return

    while True:
        start_date = input("Enter the start date (yyyy-mm-dd) or press enter to skip or 'q' to quit: ").strip()
        if start_date.lower() == 'q':
            return
        if start_date == "" or is_valid_date(start_date):
            break
        print("Invalid date format. Please enter a valid date in YYYY-MM-DD format.")

    while True:
        end_date = input("Enter the end date (yyyy-mm-dd) or press enter to skip or 'q' to quit: ").strip()
        if end_date.lower() == 'q':
            return
        if end_date == "" or is_valid_date(end_date):
            if start_date and end_date and not compare_dates(start_date, end_date):
                print("End date cannot be earlier than start date. Please enter a valid date range.")
                continue
            break
        print("Invalid date format. Please enter a valid date in YYYY-MM-DD format.")

    conditions = []
    params = []

    if start_date:
        conditions.append("Date >= ?")
        params.append(start_date)

    if end_date:
        conditions.append("Date <= ?")
        params.append(end_date)

    if patient:
        conditions.append("Patient LIKE ?")
        params.append(f"%{patient}%")  # Allows partial match

    query = "SELECT * FROM appointments"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    try:
        with conn:
            rows = conn.execute(query, params).fetchall()
            if rows:
                print("\nAppointments found:")
                return rows
            else:
                print("\nNo appointments match the criteria.")
                return None
        
    except sqlite3.Error as e:
        print(f"Error fetching appointments: {e}")

    # If no filters were applied, fetch all appointments
    if not start_date and not end_date and not patient:
        print("\nNo filters applied. Showing all appointments:")
        try:
            with conn:
                rows = conn.execute("SELECT * FROM appointments").fetchall()
                if rows:
                    print("\nAppointments found:")
                    return rows
                else:
                    print("\nNo appointments found.")
        except sqlite3.Error as e:
            print(f"Error fetching all appointments: {e}")

def delete_appointment(conn):
    show_query = "SELECT * FROM appointments"
    try:
        with conn:
            rows = conn.execute(show_query).fetchall()
            if rows:
                print("\nAppointments found:")
                for row in rows:
                    id, date, time, patient, purpose, phone, email = row
                    print(id, date, time, patient, purpose, phone, email, sep='|')
            else:
                print("\nNo appointments")
                return
        
    except sqlite3.Error as e:
        print(f"Error fetching appointments: {e}")

    while True:
        id = input("Enter the ID of the appointment to delete or 'q' to quit: ").strip()

        if id.lower() == 'q':  # Allow user to quit
            return

        if not id.isdigit():  # Ensure it's a valid integer
            print("Invalid ID. Please enter a numeric ID.")
            continue

        id = int(id)

        # Check if the ID exists
        check_query = "SELECT 1 FROM appointments WHERE ID = ?"
        with conn:
            result = conn.execute(check_query, (id,)).fetchone()

        if not result:
            print(f"No appointment found with ID {id}. Please enter a valid ID.")
            continue
        
        break  # Valid ID found

    query = "DELETE FROM appointments WHERE ID = ?"

    try:
        with conn:
            conn.execute(query, (id,))
            conn.commit()
            print(f"Appointment with ID {id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting appointment: {e}")


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


def schedule_reminders(conn, scheduler):
    with conn:
        query = "SELECT ID, Date, Time, Email, Patient FROM appointments"
        appointments = conn.execute(query).fetchall()

    for appointment in appointments:
        app_id, app_date, app_time, email, patient = appointment
        appointment_datetime = datetime.strptime(f"{app_date} {app_time}", "%Y-%m-%d %H:%M")
        reminder_time = appointment_datetime - timedelta(minutes=1) # time for email to send

        if reminder_time > datetime.now():
            scheduler.add_job(send_reminder_email, 'date', run_date=reminder_time, args=[email, patient, app_date, app_time])
            print(f"Reminder scheduled for {patient} at {reminder_time}")


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
    
def send_reminder(conn):
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
        appointment_id = input("\nEnter the ID of the appointment or 'q' to quit: ").strip()

        if appointment_id.lower() == 'q':
            return

        if not appointment_id.isdigit():
            print("Invalid ID. Please enter a numeric ID.")
            continue

        appointment_id = int(appointment_id)
        break

    try:
        with conn:  

            # SQL query to fetch the email, date, time, patient for the given appointment ID
            query = "SELECT email, date, time, patient FROM appointments WHERE ID = ?"

            # Execute the query
            result = conn.execute(query, (appointment_id,)).fetchone()

            # If result is None, it means no record was found
            if result:
                receiver_email, app_date, app_time, patient_name = result  
    
    except sqlite3.Error as e:
        print(f"Error: {e}")

    sender_email = 'luvel.remnder@gmail.com'
    password = 'jjka keni yshl hjkb'

    subject = 'LUVEL Clinic Appointment Reminder'
    body = f"""
    Dear {patient_name},
    This is a reminder that you have an appointment scheduled for {app_date} at {app_time}.
    """

    print("Sending reminder, please wait...")
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()


    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(em)
        print(f"Reminder to {patient_name} sent sucessfully.")
    


def main():
    print("Welcome to LUVEL Clinic!")
    prompt_for_credentials()
    conn = get_connection()

    scheduler = BackgroundScheduler()
    scheduler.start()

    try:
        create_table(conn)
        schedule_reminders(conn, scheduler)  # Schedule reminders at startup

        while True:
            print("\nPlease select an option:")
            print("1: Add an appointment")
            print("2: Read appointments")
            print("3: Update an appointment")
            print("4: Delete an appointment")
            print("5: Send appointment manually to a patient")
            print("6: Exit")

            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                insert_appointment(conn)
                schedule_reminders(conn, scheduler)  # Reschedule reminders after adding new appointments
            elif choice == '2':
                appointments = fetch_appointments(conn)
                if appointments: 
                    for appointment in appointments:
                        id, date, time, patient, purpose, phone, email = appointment
                        print(id, date, time, patient, purpose, phone, email, sep=' | ')
            elif choice == '3':
                update_appointment(conn)
                schedule_reminders(conn, scheduler)  # Reschedule in case of time change
            elif choice == '4':
                delete_appointment(conn)
                schedule_reminders(conn, scheduler)  # Reschedule after deletion
            elif choice == '5':
                send_reminder(conn)
            elif choice == '6':
                print("Exiting Appointment Management System...")
                scheduler.shutdown()
                break
            else:
                print("Invalid choice. Please select a valid option.")

    finally:
        conn.close()

if __name__ == "__main__":
    main()

