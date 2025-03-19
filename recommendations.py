mport pandas as pd

class HospitalRecommender:
    CSV_FILE = "hospitals.csv"  # CSV file with organ and hospital data

    @classmethod
    def recommend_hospital(cls):
        # Read the CSV file
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

