#!/usr/bin/python3
from data_entry import get_date, get_time, get_patient, get_purpose, get_phone, get_email, prompt_for_credentials
import sqlite3
import re
from email.message import EmailMessage
import ssl
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

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
    

# Laura
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
                fetch_appointments(conn)
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

