import csv

class HospitalRecommender:
    CSV_FILE = "hospital.csv"

    @classmethod
    def recommend_hospital(cls):
        organ = input("Enter the organ or body part you have an issue with: ").strip().lower()
        found = False

        # Open and read CSV
        with open(cls.CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['organ'].lower() == organ:
                    print(f"\nRecommended hospital for '{organ}': {row['hospital']}")
                    found = True
                    break

        if not found:
            print("\nSorry, no recommendation found for that organ/body part.")

# Example usage
if __name__ == "__main__":
    HospitalRecommender.recommend_hospital()

