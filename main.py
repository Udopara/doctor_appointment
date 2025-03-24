import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_time, get_patient, get_purpose, get_phone, generate_ID

class CSV:
    CSV_FILE = 'appointment_data.csv'
    COLUMNS = ['id','date', 'time', 'patient', 'purpose', 'phone']
    FORMAT = '%d-%m-%Y'
    @classmethod
    def initialize_csv(cls): #create csv file if it doesn't exist
        try: #try to read csv file
            pd.read_csv(cls.CSV_FILE) #check if file exists
        except FileNotFoundError: #if file doesn't exist
            df = pd.DataFrame(columns=cls.COLUMNS) #create new dataframe
            df.to_csv(cls.CSV_FILE, index=False) #save dataframe to csv file


    @classmethod
    def add_appointment(cls, id, date, time, patient, purpose, phone): #add appointment to csv file
        new_appointment = {
            'id': id, 
            'date': date,
            'time': time,
            'patient': patient,
            'purpose': purpose,
            'phone': phone
        } #create new appointment dictionary

        with open(cls.CSV_FILE, mode='a', newline='') as csvfile: #open csv file in append mode, don't add new line character
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS) #create writer object
            writer.writerow(new_appointment) #write new appointment to csv file

        print('Appointment added successfully!')
        return True
    
    @classmethod
    def read_appointments(cls):  # Read appointments from CSV file
        patient = input("Enter the patient name or press enter to skip: ")  # Get patient name from user
        start_date = input("Enter the start date (dd-mm-yyyy) or press enter to skip: ")  # Get start date
        end_date = input("Enter the end date (dd-mm-yyyy) or press enter to skip: ")  # Get end date
        
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(cls.CSV_FILE)
        
        # Convert the 'date' column to datetime format for proper filtering
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        
        # Initialize a boolean mask to include all rows initially
        mask = pd.Series(True, index=df.index)
        
        # Convert user input dates to datetime if provided
        if start_date:
            try:
                start_date = datetime.strptime(start_date, cls.FORMAT)  # Convert start date to datetime
                mask &= df['date'] >= start_date  # Apply filter for start date
            except ValueError:
                print("Invalid start date format. Please use dd-mm-yyyy.")
                return
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, cls.FORMAT)  # Convert end date to datetime
                mask &= df['date'] <= end_date  # Apply filter for end date
            except ValueError:
                print("Invalid end date format. Please use dd-mm-yyyy.")
                return
        
        # Apply filter for patient name if provided
        if patient:
            mask &= df['patient'] == patient  # Filter by patient name
        
        # Filter DataFrame based on the mask
        filtered_df = df.loc[mask]
        
        # Check if any appointments were found
        if filtered_df.empty:
            print('No appointments found!')
        else:
            # Print appointments in a readable format
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}), end='\n')
            
            # Get total number of appointments found
            total_appointments = len(filtered_df)
            print(f"There {'is' if total_appointments == 1 else 'are'} {total_appointments} {'appointment' if total_appointments == 1 else 'appointments'} found.")

    @classmethod
    def delete_appointment(cls): #delete appointment from csv file
        df = pd.read_csv(cls.CSV_FILE) #read csv file
        id = input("Enter the ID of the appointment to delete: ")
        # Remove rows where row 'id' has value of the input ID
        df_filtered = df[df["id"] != id]
        df_filtered.to_csv(cls.CSV_FILE, index=False)


    @classmethod
    def update_appointment(cls): #update appointment from csv file
        df = pd.read_csv(cls.CSV_FILE)
        id  = input("Enter the ID of the appointment to update: ")
        #check if id exists in dataframe
        if id in df["id"].values:
            new_time = input("Enter the new time(hh:mm) or press 'Enter' to skip: ")
            new_name = input("Enter new name if applicable or press 'Enter' to skip: ")
            new_date = input("Enter the new date of appointment(dd-mm-yyyy) or press 'Enter' to skip: ")
            new_purpose = input("Enter the new purpose of appointment or press 'Enter' to skip: ")
            new_phone_number = input("Enter the new phone number of patient or press 'Enter' to skip: ")
            if new_time:
                df.loc[df["id"] == id, "time"] = new_time
                df.to_csv(cls.CSV_FILE, index=False)
                print ("Appointment updated successfully")
            if new_name:
                df.loc[df["id"] == id, "name"] = new_name
                df.to_csv(cls.CSV_FILE, index=False)
                print ("Appointment updated successfully")
            if new_date:
                df.loc[df["id"] ==id, "date"] = new_date
                df.to_csv(cls.CSV_FILE, index=False)
                print("Appointment updated successfully")
            if new_purpose:
                df.loc[df["id"] ==id, "purpose"] = new_purpose
                df.to_csv(cls.CSV_FILE,index=False)
                print("Appointment updated successfully")
                if new_phone_number:
                    df.loc[df["id"] ==id,"phone_number"] = new_phone_number
                    df.to_csv(cls.CSV_FILE, index=False)
                    print("Appointment updated successfully")

    
        
    @classmethod
    def recommend_appointment(cls): #recommend appointment from csv file
        df = pd.read_csv(cls.CSV_FILE)
        
        # Get user input
        organ = input("Enter the organ or body part you are having issues with: ").strip().lower()
        
        # Search for the hospital recommendation
        recommendation = df[df["organ"] == organ]
        
        # Check if recommendation exists
        if not recommendation.empty:
            hospital = recommendation.iloc[0]["hospital"]
            print(f"\nRecommended hospital for '{organ}' issues: {hospital}")
        else:
            print("\nSorry, no recommendation available for that organ/body part.")


def add():
    CSV.initialize_csv() #initialize csv file
    id = generate_ID() #generate appointment ID
    date = get_date("Enter the date of the appointment (dd-mm-yyyy) or enter for today's date: ", allow_default=True) #get date from user
    time = get_time('Enter the time of the appointment (hh:mm): ') #get time from user
    patient = get_patient() #get patient name from user
    purpose = get_purpose() #get purpose of appointment from user
    phone = get_phone() #get phone number from user
    CSV.add_appointment(id, date, time, patient, purpose, phone) #add appointment


add() #add appointment to csv file
CSV.read_appointments() #read appointments from csv file
CSV.update_appointment() # updates appointment
CSV.delete_appointment() #delete appointment from csv file
