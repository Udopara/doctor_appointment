import pandas as pd
from datetime import datetime
from email.message import EmailMessage
import ssl
import smtplib
from main import CSV


email = 'p.opara@alustudent.com'
password = 'xbbz xpgd lxka hvpf'

def send_email():
    CSV.read_appointments()
    receiver_id = input("Enter the receiver's id: ")
    df = pd.read_csv('appointment_data.csv')
    receiver_email = df[df['id'] == receiver_id]['email'] #get receiver's email from appointment data
    receiver_name = str(df[df['id'] == receiver_id]['patient'].values[0])  # Convert to string
    date = str(df[df['id'] == receiver_id]['date'].values[0])
    time = str(df[df['id'] == receiver_id]['time'].values[0])

    subject = 'Appointment Reminder'
    body = f"""
    Dear {receiver_name},
    This is a reminder that you have an appointment scheduled for {date} at {time}.
    """

    em = EmailMessage()
    em['From'] = email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()


    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email, password)
        smtp.send_message(em)

if __name__ == '__main__':
    send_email()