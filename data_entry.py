import pandas as pd
from datetime import datetime
import getpass

date_format = '%Y-%m-%d'
time_format = '%H:%M'


user_emails_pwd = {
    'luvel.remnder@gmail.com' : "admin_luvel",
    'admin': 'admin'
}

def get_date(prompt = "Enter the date of the appointment (yyyy-mm-dd) or 'enter' for today's date or 'q' to quit: "): 
    date_str = input(prompt).lower() #get date from user 
    if date_str == 'q':
        return date_str
    if date_str == '':
        return datetime.today().strftime(date_format) #return current date if user doesn't enter anything
    
    try:
        valid_date = datetime.strptime(date_str, date_format) #convert date string to datetime object
        return valid_date.strftime(date_format) #return formatted date string
    except ValueError: #if date is invalid
        print('Invalid date! Please enter date in yyyy-mm-dd format.')
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