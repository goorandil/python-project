import tkinter as tk
from left_frame import LeftFrame
from right_frame import RightFrame
from configparser import ConfigParser

# Read the config file
config = ConfigParser()
config.read('config.ini')

# Retrieve the USB port and baud rate from the config file
port = config.get('Serial', 'port')
baud_rate = config.getint('Serial', 'baudrate')
filename = config.get('Serial', 'filename')

# Create the main window
window = tk.Tk()

 
# Maximize the window
window.state('zoomed')
window.title("Brainwave Monitoring Software")


# Create the right frame
right_frame = RightFrame(window)
right_frame.grid(row=0, column=1, sticky="nsew")

# Create the left frame
left_frame = LeftFrame(window,port, baud_rate,right_frame)
left_frame.grid(row=0, column=0, sticky="ns")

# Configure the grid to expand the right column when the window is resized
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# Start the GUI event loop
window.mainloop()
# Create the main window
root = tk.Tk()

# Create the right frame
right_frame = RightFrame(root)

# Create the left frame and pass the right frame as an argument
left_frame = LeftFrame(root, port, baud_rate, right_frame)

# Rest of the code...

# Start the main event loop
root.mainloop()