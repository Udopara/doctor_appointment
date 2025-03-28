import pandas as pd
from datetime import datetime
import getpass

date_format = '%d-%m-%Y'
time_format = '%H:%M'


user_emails_pwd = {
    'luvel@gmail.com' : "admin_luvel",
    'admin': 'admin'
}

# To get the doctor to log in
def prompt_for_credentials():
    while True:
        email = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")  # we use getpass to hide password input
        if email in user_emails_pwd and user_emails_pwd[email] == password:
            print("Login successful!")
            break
        else:
            print("Invalid email or password. Please try again or type 'quit' to exit.")
            if email.lower() == 'quit':
                exit()
    

def generate_ID():
    beginning = 'AP-'
    length = 5
    df = pd.read_csv('appointment_data.csv')
    df_ids = df['id'].map(lambda x: (int(x.split('-')[1]) if isinstance(x, str) else 0))[1:]
    if len(df_ids) == 0:
        return beginning + '1'.zfill(length)
    current_id = df_ids.max() 
    app_id = beginning + str(current_id + 1).zfill(length) #generate appointment ID
    return app_id



def get_date(prompt = "Enter the date of the appointment (dd-mm-yyyy) or 'enter' for today's date or 'q' to quit: "): 
    date_str = input(prompt).lower() #get date from user 
    if date_str == 'q':
        return date_str
    if date_str == '':
        return datetime.today().strftime(date_format) #return current date if user doesn't enter anything
    
    try:
        valid_date = datetime.strptime(date_str, date_format) #convert date string to datetime object
        return valid_date.strftime(date_format) #return formatted date string
    except ValueError: #if date is invalid
        print('Invalid date! Please enter date in dd-mm-yyyy format.')
        return get_date() #ask user for date again

def get_time(prompt = "Enter the new time(hh:mm) or 'q' to quit: "): #get time from user
    time_str = input(prompt).lower() #get time from user
    if time_str == 'q':
        return time_str
    try:
        valid_time = datetime.strptime(time_str, time_format) #convert time string to datetime object
        return valid_time.strftime(time_format) #return formatted time string
    except ValueError: #if time is invalid
        print('Invalid time! Please enter time in HH:MM format.')
        return get_time() #ask user for time again

def get_patient(prompt = "Enter the patient name  or 'q' to quit: "): #get patient name from user
    patient = input(prompt).lower() #get patient name from user
    if patient == '': #if patient name is empty
        print('Patient name cannot be empty!') #print error message
        return get_patient() #ask user for patient name again
    return patient
    
def get_purpose(prompt = "Enter the purpose of the appointment or 'q' to quit: "): #get purpose of appointment from user
    purpose = input(prompt).lower() #get purpose of appointment from user
    if purpose == '': #if purpose is empty
        print('Purpose cannot be empty!') #print error message
        return get_purpose() #ask user for purpose again
    return purpose #return valid purpose

def get_phone(prompt = "Enter the phone number or 'q' to quit: "): #get phone number from user
    phone = input(prompt).lower() #get phone number from user

    if phone == 'q':
        return phone

    if phone == '': #if phone number is empty
        print('Phone number cannot be empty!') #print error message
        return get_phone() #ask user for phone number again
    
    if not phone.isdigit(): #if phone number contains non-numeric characters
        print('Invalid phone number! Please enter a valid phone number.') #print error message
        return get_phone() #ask user for phone number again
    
    if len(phone) != 10: #if phone number is not 10 digits long
        print('Invalid phone number! Phone number must be 10 digits long.') #print error message
        return get_phone() #ask user for phone number again
    
    return phone #return valid phone number

def get_email(prompt = "Enter the email address or 'q' to quit: "): #get email from user
    email = input(prompt).lower() #get email address from user
    if email == 'q':
        return email
    if email == '': #if email is empty
        print('Email cannot be empty!') #print error message
        return get_email() #ask user for email again
    email_parts = email.split('@') #split email address into parts
    if len(email_parts) != 2: #if email address doesn't contain '@'
        print('Invalid email address! Please enter a valid email address.') #print error message
        return get_email() #ask user for email again
    return email #return valid email address

def get_new_date():
    while True:
        new_date = input("Enter the new date (dd-mm-yyyy) or press 'enter' to skip or 'q' to quit: ").strip()
        if new_date.lower() == 'q':  # If user enters 'q', return 'q'
            return 'q'
        if new_date == '':  # If user enters an empty string, return None
            return new_date
        try:
            # Try to convert the input to a datetime object
            return datetime.strptime(new_date, '%d-%m-%Y')
        except ValueError:
            print("Invalid date format. Please use dd-mm-yyyy.")

def get_new_phone(prompt="Enter the new phone number (10 digits) or press 'enter' to skip or 'q' to quit: "):
    while True:
        phone = input(prompt).strip().lower()  # Get input from the user
        if phone == 'q':  # If user enters 'q', return 'q'
            return 'q'
        if phone == '':  # If user enters an empty string, return ''
            return ''
        if not phone.isdigit():  # Check if the input contains only digits
            print("Invalid phone number! Please enter a valid 10-digit phone number.")
            continue
        if len(phone) != 10:  # Check if the phone number is exactly 10 digits long
            print("Invalid phone number! Phone number must be 10 digits long.")
            continue
        return phone  # Return the valid phone number


if __name__ == '__main__':   
    pass
