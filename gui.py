import tkinter as tk
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import csv
import time


arduino_port = 'COM3'  #set the port for the Arduino
baud_rate = 9600  #set the baud rate
fileName ="sensor_data.csv"  #set the file name for the CSV file
samples = 10
print_labels = False


#create the main window
root = tk.Tk()
root.geometry("800x600")
root.attributes('-alpha', 0.9)  #set the window transparency to 80%
root.title("Greenhouse Control System")

# Create a figure for the graph
fig, ax = plt.subplots(figsize=(5, 3))

# Create a canvas for the figure and place it in the window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().config(width=400, height=200)  # Set the size of the canvas widget
canvas.get_tk_widget().place(relx=0.5, rely=0.2, anchor='center')

# Lists to store the sensor data
soil_moisture_data = 500
humidity_data = 50

# create a label for the time
time_label = tk.Label(root)
time_label.place(relx=0.95, rely=0.05, anchor='ne')  #place at the top right of the window

terminal = tk.Text(root, height=10)
terminal.place(relx=0.5, rely=0.9, anchor='s')  #place at the bottom of the window

#create labels for the sensor data
soil_moisture_label = tk.Label(root, text="Soil Moisture: ")
soil_moisture_label.place(relx=0.3, rely=0.5, anchor='center')  #place in the center of the window, slightly to the left

humidity_label = tk.Label(root, text="Humidity: ") #create a label for the humidity
humidity_label.place(relx=0.5, rely=0.5, anchor='center')  #place in the center of the window

co2_label = tk.Label(root, text="CO2 Level: ") #create a label for the CO2 level
co2_label.place(relx=0.7, rely=0.5, anchor='center')  #place in the center of the window, slightly to the right

pump_status_label = tk.Label(root, text="Pump Status: OFF")
pump_status_label.place(relx=0.3, rely=0.4, anchor='center')  #place above the soil moisture label

fan_status_label = tk.Label(root, text="Fan Status: OFF")
fan_status_label.place(relx=0.5, rely=0.4, anchor='center')  #place above the humidity label


#function to update the time
def update_time():
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    time_label.config(text=current_time)
    root.after(1000, update_time)  #schedule the function to run again after 1 second

#function to update the sensor data
def update_data():

        # Update the labels with the new data
    soil_moisture_label.config(text=f"Soil Moisture: {soil_moisture_data}%")
    humidity_label.config(text=f"Humidity: {humidity_data}%")
    co2_label.config(text=f"CO2 Level: N/A ppm")

    #update the pump and fan status labels
    if soil_moisture_data < 450:
        pump_status_label.config(text="Pump Status: ON")
    else:
        pump_status_label.config(text="Pump Status: OFF")

    if humidity_data > 80:
        fan_status_label.config(text="Fan Status: ON")
    else:
        fan_status_label.config(text="Fan Status: OFF")

    #if the soil moisture is less than 30%, display a message in the terminal
    if soil_moisture_data < 450:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        terminal.insert('end', f'{current_time}: The greenhouse is being watered.\n')
        terminal.see('end')  #scroll the terminal to the end

    #schedule the function to run again after 1 second (1000 milliseconds)
    root.after(1000, update_data)

ser = serial.Serial(arduino_port, baud_rate)  #create the serial object
print("Connected to Arduino port:", arduino_port)
file = open(fileName, 'a')  #open the CSV file
print("Created CSV file:", fileName)

line = 0

while line <= samples:
    if print_labels:
        if line==0:
            print("Printing column headers")
        else:
            print("Line " + str(line) + ": writing...")
    getData=str(ser.readline())
    data=getData[0:][:-2]
    print(data)

    file = open(fileName, 'a')
    file.write(data + "\n")
    line = line+1

print("Data collection complete!")

#start the time update function
update_time()
#start the data update function
update_data()

# Start the main loop
root.mainloop()
