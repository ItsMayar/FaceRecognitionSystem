import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import csv

# Set up Firebase credentials and initialize the app
cred = credentials.Certificate('facerecognition-c0e1a-firebase-adminsdk-b7t4k-55aeb38888.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facerecognition-c0e1a-default-rtdb.firebaseio.com/'
})

# Define the path to the node in the Firebase Realtime Database
node_path = 'Students'

# Read the data from the specified node
ref = db.reference(node_path)
data = ref.get()

# Specify the path to save the CSV file
csv_file_path = 'data.csv'

# Extract the keys from the first item to use as CSV headers
keys = list(data.keys())

headers = list(data[keys[0]].keys()) + ['total_monthly_attendance', 'monthly_percentage']
print(keys)

# Create a dictionary to store the total monthly attendance for each class
class_attendance = {}

# Prompt the user to enter the total monthly attendance for each class
for key in keys:
    class_name = data[key]['class_name']
    total_monthly_attendance = int(input(f"Enter the total monthly attendance for class {class_name}: "))
    class_attendance[key] = total_monthly_attendance

# Write the data to the CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['id'] + headers)  # Write an empty cell followed by headers as the first row
    for key, values in data.items():
        # Get the total attendance
        total_attendance = values['total_attendance']
        
        # Get the total monthly attendance for the class
        total_monthly_attendance = class_attendance[key]
        
        # Calculate the monthly percentage
        monthly_percentage = (total_attendance / total_monthly_attendance) * 100

        # Append the total monthly attendance and monthly percentage to the row data
        row_data = [key] + list(values.values()) + [total_monthly_attendance, f"{monthly_percentage:.0f}%"]

        writer.writerow(row_data)

print("Data saved as CSV successfully.")
1