from datetime import datetime

date_format = '%d-%m-%Y'
time_format = '%H:%M'
current_id = 0

user_emails_pwd = {
    'johndoe@example.com': 'abc123'
}
    

def generate_ID():
    beginning = 'AP-'
    length = 5
    global current_id #use global variable
    current_id += 1
    app_id = beginning + str(current_id).zfill(length) #generate appointment ID
    return app_id



def get_date(prompt, allow_default = False): 
    date_str = input(prompt) #get date from user
    if allow_default and date_str == '':
        return datetime.today().strftime(date_format) #return current date if user doesn't enter anything
    
    try:
        valid_date = datetime.strptime(date_str, date_format) #convert date string to datetime object
        return valid_date.strftime(date_format) #return formatted date string
    except ValueError: #if date is invalid
        print('Invalid date! Please enter date in dd-mm-yyyy format.')
        return get_date(prompt, allow_default) #ask user for date again

def get_time(prompt): #get time from user
    time_str = input(prompt) #get time from user
    # if allow_default and time_str == '':
    #     return datetime.now().strftime(time_format) #return current time if user doesn't enter anything
    
    try:
        valid_time = datetime.strptime(time_str, time_format) #convert time string to datetime object
        return valid_time.strftime(time_format) #return formatted time string
    except ValueError: #if time is invalid
        print('Invalid time! Please enter time in HH:MM format.')
        return get_time(prompt) #ask user for time again

def get_patient(): #get patient name from user
    patient = input('Enter the patient name: ') #get patient name from user
    if patient == '': #if patient name is empty
        print('Patient name cannot be empty!') #print error message
        return get_patient() #ask user for patient name again
    return patient
    
def get_purpose(): #get purpose of appointment from user
    purpose = input('Enter the purpose of the appointment: ') #get purpose of appointment from user
    if purpose == '': #if purpose is empty
        print('Purpose cannot be empty!') #print error message
        return get_purpose() #ask user for purpose again
    return purpose #return valid purpose

def get_phone(): #get phone number from user
    phone = input("Enter the phone number: ") #get phone number from user

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

if __name__ == '__main__':
#     get_date("Enter the date of the appointment (dd-mm-yyyy) or enter for today's date: ", allow_default=True) #get date from user
#     get_time('Enter the time of the appointment (hh:mm): ') #get time from user
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID
    print(generate_ID()) #generate appointment ID