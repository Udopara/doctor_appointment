import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_time, get_patient, get_purpose, get_phone, get_email, get_new_phone, get_new_date, generate_ID,  prompt_for_credentials
from recommendations import HospitalRecommender

class CSV:
    CSV_FILE = 'appointment_data.csv'
    COLUMNS = ['id','date', 'time', 'patient', 'purpose', 'phone', 'email']
    FORMAT = '%d-%m-%Y'
    @classmethod
    def initialize_csv(cls): #create csv file if it doesn't exist
        try: #try to read csv file
            pd.read_csv(cls.CSV_FILE) #check if file exists
        except FileNotFoundError: #if file doesn't exist
            df = pd.DataFrame(columns=cls.COLUMNS) #create new dataframe
            df.to_csv(cls.CSV_FILE, index=False) #save dataframe to csv file


    @classmethod
    def add_appointment(cls):
        functions = [get_date, get_time, get_patient, get_purpose, get_phone, get_email]  # List of functions to get input from the user
        fields = ['date', 'time', 'patient', 'purpose', 'phone', 'email']  # Corresponding fields in the dictionary

        # Generate appointment ID
        id = generate_ID()

        # Initialize a dictionary for the new appointment
        new_appointment = {'id': id}

        # Iterate through functions and fields
        for function, field in zip(functions, fields):
            result = function()  # Call the function to get the user input
            if result == 'q':  # If user enters 'q', return and exit
                return
            new_appointment[field] = result  # Assign the result to the corresponding field in the dictionary

        # Write the new appointment to the CSV file
        try:
            with open(cls.CSV_FILE, mode='a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
                writer.writerow(new_appointment)  # Write the new appointment to the CSV file

            print('Appointment added successfully!')
        except Exception as e:
            print(f"An error occurred while adding the appointment: {e}")
        
    @classmethod
    def read_appointments(cls):  # Read appointments from CSV file
        patient = input("Enter the patient name or press enter to skip or 'q' to quit: ")  # Get patient name from user
        if patient.lower() == 'q':  # If user enters 'q', return and exit
            return
        start_date = input("Enter the start date (dd-mm-yyyy) or press enter to skip or 'q' to quit: ")  # Get start date
        if start_date.lower() == 'q':  # If user enters 'q', return and exit
            return
        end_date = input("Enter the end date (dd-mm-yyyy) or press enter to skip or 'q' to quit: \n")  # Get end date
        if end_date.lower() == 'q':  # If user enters 'q', return and exit
            return
        
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
        print("Current appointments:")
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)  # Convert date column to datetime
        print(df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}), end='\n')
        id = input("Enter the ID of the appointment to delete or 'q' to quit: ")
        if id.lower() == 'q':  # If user enters 'q', return and exit
            return
        # Remove rows where row 'id' has value of the input ID
        df_filtered = df[df["id"] != id]
        df_filtered.to_csv(cls.CSV_FILE, index=False)


    @classmethod
    def update_appointment(cls): #update appointment from csv file
        df = pd.read_csv(cls.CSV_FILE)
        print("Current appointments:")
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)  # Convert date column to datetime
        print(df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}), end='\n')
        id  = input("Enter the ID of the appointment to update or 'q' to quit: ")
        if id.lower() == 'q':  # If user enters 'q', return and exit
            return
        #check if id exists in dataframe
        if id in df["id"].values:
            new_time = input("Enter the new time(hh:mm) or 'enter' to skip or 'q' to quit: ")
            if new_time.lower() == 'q':  # If user enters 'q', return and exit
                return
            
            new_name = input("Enter the new name or 'enter' to skip or 'q' to quit: ")
            if new_name.lower() == 'q':  # If user enters 'q', return and exit
                return
            
            new_date = get_new_date()
            if new_date.lower() == 'q':  # If user enters 'q', return and exit
                return
            
            
            new_purpose = input("Enter the new purpose or 'enter' to skip or 'q' to quit: ")
            if new_purpose.lower() == 'q':  # If user enters 'q', return and exit
                return
            
            new_phone_number = get_new_phone()
            if new_phone_number.lower() == 'q':  # If user enters 'q', return and exit
                return
            
            new_email = get_email("Enter the new email or 'enter' to skip or 'q' to quit: ")
            if new_email.lower() == 'q':  # If user enters 'q', return and exit
                return

            if new_time:
                df.loc[df["id"] == id, "time"] = new_time
                df.to_csv(cls.CSV_FILE, index=False)

            if new_name:
                df.loc[df["id"] == id, "name"] = new_name
                df.to_csv(cls.CSV_FILE, index=False)

            if new_date:
                df.loc[df["id"] ==id, "date"] = new_date
                df.to_csv(cls.CSV_FILE, index=False)

            if new_purpose:
                df.loc[df["id"] ==id, "purpose"] = new_purpose
                df.to_csv(cls.CSV_FILE,index=False)

            if new_phone_number:
                df.loc[df["id"] ==id,"phone_number"] = new_phone_number
                df.to_csv(cls.CSV_FILE, index=False)

            if new_email:
                df.loc[df["id"] ==id,"email"] = new_email
                df.to_csv(cls.CSV_FILE, index=False)
            
            print("Appointment updated successfully")

    
        
    @classmethod
    def recommend_appointment(cls): #recommend appointment from csv file
        df = pd.read_csv(cls.CSV_FILE)
        
        # Get user input
        organ = input("Enter the organ or body part you are having issues with or 'q' to quit: ").strip().lower()
        if organ == 'q':
            return
        
        # Search for the hospital recommendation
        recommendation = df[df["organ"] == organ]
        
        # Check if recommendation exists
        if not recommendation.empty:
            hospital = recommendation.iloc[0]["hospital"]
            print(f"\nRecommended hospital for '{organ}' issues: {hospital}")
        else:
            print("\nSorry, no recommendation available for that organ/body part.")




if __name__ == '__main__':
    print("Welcome to LUVEL Clinic!")
    prompt_for_credentials()
    CSV.initialize_csv()
    while True:
        print("\nPlease select an option:")
        print("1: Add an appointment")
        print("2: Read appointments")
        print("3: Update an appointment")
        print("4: Delete an appointment")
        print("5: Recommend a hospital")
        print("6: Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            CSV.add_appointment()
        elif choice == '2':
            CSV.read_appointments()
        elif choice == '3':
            CSV.update_appointment()
        elif choice == '4':
            CSV.delete_appointment()
        elif choice == '5':
            if pd.read_csv(CSV.CSV_FILE).empty:
                print("No available appointments to recommend hospitals for.")
            else:
                HospitalRecommender.recommend_hospital()
        elif choice == '6':
            print("Exiting Appointment Management Sysytem...")
            print("Saving current state to database...")
            print("...")
            print("Saved!! See you next time!")
            break
        else:
            print("Invalid choice. Please select a valid option.")