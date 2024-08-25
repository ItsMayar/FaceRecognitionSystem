import tkinter as tk
import addstudents 
import tkinter.font as font

import Main
root = tk.Tk()
myFont = font.Font(size=10)
register_button = tk.Button(root, text="Register New Student",height= 5, width=30, command=addstudents.start)
register_button['font'] = myFont
    # Create a button to save the data
attendance_button = tk.Button(root, text="Take Attendance",height= 5, width=30, command=Main.start)
attendance_button['font'] = myFont
register_button.pack()
attendance_button.pack()
root.mainloop()