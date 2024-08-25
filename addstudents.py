import tkinter as tk
from tkinter import PhotoImage, messagebox
import cv2
import dlib
from PIL import Image, ImageTk
import numpy as np
import encodegenerator
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage
import os
cred = credentials.Certificate("facerecognition-c0e1a-firebase-adminsdk-b7t4k-55aeb38888.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognition-c0e1a-default-rtdb.firebaseio.com/",
    'storageBucket':"facerecognition-c0e1a.appspot.com"
})

ref = db.reference('Students')

def delete_data():

    id = id_entry.get()
    if id =='':
        messagebox.showinfo("warning", "id is empty!")
    folderPath = 'Images'
    ref.child(id).delete()
    fileName = f'{folderPath}/{id}.png'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.delete()
    os.remove(fileName)
    encodegenerator.process()



def save_data():
    # Get the data from the entry boxes
    id = id_entry.get()
    name = name_entry.get()
    major = major_entry.get()
    starting_year = starting_year_entry.get()
    total_attendance = total_attendance_entry.get()
    class_name = class_name_entry.get()
    study_year = study_year_entry.get()

    # Create a dictionary to store the data
    data = {
        id:{
        "name": name,
        "major": major,
        "starting_year": int(starting_year),
        "total_attendance": int(total_attendance),
        "class_name": class_name,
        "year": int(study_year),
        "last_attendance_time": "2023-01-01 00:00:00"
        }
    }
    print(data)
    for key, value in data.items():
        ref.child(key).set(value)

    messagebox.showinfo("Success", "Data saved successfully!")
    

    # Save the data to a file
    

    # Display a message


# Create a canvas to display the image


# Create a video capture object


# Start a loop to capture frames from the webcam
def take_image():
    cap = cv2.VideoCapture(0)

# Create a face detector
    detector = dlib.get_frontal_face_detector()

    # Create a predictor
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    while True:
        # Capture a frame
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('gray',gray)
        # Detect faces in the frame
        faces = detector(gray)

        # If there are any faces detected
        if len(faces) > 0:
            # Find the largest face in the frame
            face = max(faces, key=lambda face: face.area())
            
            print(face)
            face_image = frame[face.top()-40:face.bottom()+40,face.left()-40:face.right()+40]

            # Resize the face image to 216x216
            resized_face_image = cv2.resize(face_image, (216, 216))
            cv2.imshow('cropped',resized_face_image)

            # Save the face image
            cv2.imwrite("Images/{id}.png".format(id=id_entry.get()), resized_face_image)

            # Display the face image on the canvas
            cap.release()
            if cv2.waitKey(0) == 27:
                cv2.destroyAllWindows()
            encodegenerator.process()
            return
        

        
        



# Destroy the Tkinter window
def start() :
    # Close the video capture object
    root = tk.Tk()

    # Create a label for the ID
    id_label = tk.Label(root, text="ID")
    global id_entry, name_entry, major_entry, starting_year_entry, total_attendance_entry, class_name_entry, starting_year_entry, study_year_entry
    # Create an entry box for the ID
    id_entry = tk.Entry(root)

    # Create a label for the name
    name_label = tk.Label(root, text="Name")

    # Create an entry box for the name
    name_entry = tk.Entry(root)

    # Create a label for the major
    major_label = tk.Label(root, text="Major")

    # Create an entry box for the major
    major_entry = tk.Entry(root)

    # Create a label for the starting year
    starting_year_label = tk.Label(root, text="Starting Year")

    # Create an entry box for the starting year
    starting_year_entry = tk.Entry(root)

    # Create a label for the total attendance
    total_attendance_label = tk.Label(root, text="Total Attendance")

    # Create an entry box for the total attendance
    total_attendance_entry = tk.Entry(root)

    # Create a label for class name
    class_name_label = tk.Label(root, text="Class Name")

    # Create an entry box for class name
    class_name_entry = tk.Entry(root)

    # Create a label for the study year
    study_year_label = tk.Label(root, text="Study Year")

    # Create an entry box for the study year
    study_year_entry = tk.Entry(root)



    canvas = tk.Canvas(root, width=216, height=1)
    image_button = tk.Button(root, text="Take image", command=take_image)

    # Create a button to save the data
    save_button = tk.Button(root, text="Save", command=save_data)
    delete_button = tk.Button(root, text="Delete", command=delete_data)

    id_label.pack()    
    id_entry.pack()
    name_label.pack()
    name_entry.pack()
    major_label.pack()
    major_entry.pack()
    starting_year_label.pack()
    starting_year_entry.pack()
    total_attendance_label.pack()
    total_attendance_entry.pack()
    class_name_label.pack()
    class_name_entry.pack()
    study_year_label.pack()
    study_year_entry.pack()
    canvas.pack()
    image_button.pack()
    save_button.pack()
    delete_button.pack()  
    
    root.mainloop()
