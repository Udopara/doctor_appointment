import csv

class HospitalRecommender:
    CSV_FILE_HOSPITAL = "hospital.csv"
    CSV_FILE_APPOINTMENT = "appointment_data.csv"

    @classmethod
    def recommend_hospital(cls):
        # Display the contents of appointment_data.csv
        print("\nAvailable Appointments:")
        with open(cls.CSV_FILE_APPOINTMENT, mode='r') as appointment_file:
            appointment_reader = csv.DictReader(appointment_file)
            for appointment in appointment_reader:
                print(f"ID: {appointment['id']}, Purpose of visit: {appointment['purpose']}")
        
        appointment_id = input("Enter the ID of the appointment you want to check: ")
        found_appointment = None
        
        # Find the appointment by ID
        with open(cls.CSV_FILE_APPOINTMENT, mode='r') as appointment_file:
            appointment_reader = csv.DictReader(appointment_file)
            for appointment in appointment_reader:
                if appointment['id'] == appointment_id:
                    found_appointment = appointment
                    break
        
        if not found_appointment:
            print("Appointment ID not found.")
            return
        
        purpose = found_appointment['purpose']
        print(f"Checking recommendations for purpose: {purpose}")
        
        # Check against hospital data
        with open(cls.CSV_FILE_HOSPITAL, mode='r') as hospital_file:
            hospital_reader = csv.DictReader(hospital_file)
            found = False
            for row in hospital_reader:
                if row['organ'].lower() == purpose.lower():
                    print(f"\nRecommended hospital for '{purpose}' checkup is {row['hospital']}")
                    found = True
                    break

        if not found:
            print("\nWe can treat you for that purpose, but no specific hospital recommendation is available.")

# Example usage
# if __name__ == "__main__":
#     HospitalRecommender.recommend_hospital()
