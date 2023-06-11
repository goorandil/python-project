import configparser
import csv
import datetime
import subprocess
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import serial
import os
from datetime import datetime

class LeftFrame(tk.Frame):
    def __init__(self, parent, port, baud_rate, right_frame):
        super().__init__(parent)
           # Set the fixed width of the left frame
        self.pack_propagate(False)
        self.config(width=150)
        self.port = port
        self.baud_rate = baud_rate
        self.is_capturing = False
        self.right_frame = right_frame
        self.respondent_folder = "respondent"

        # Set the fontsize
        fontsize = 10

        # Create the connect button
        self.connect_button = tk.Button(self, text="Connect", command=self.connect_serial,font=("Arial", fontsize))
        self.connect_button.pack(pady=10)

        # Create the disconnect button
        self.disconnect_button = tk.Button(self, text="Disconnect", command=self.disconnect_serial,font=("Arial", fontsize), state=tk.DISABLED)
        self.disconnect_button.pack(pady=10)

      # Set initial button states
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)

        # Create the status label
        self.status_label = tk.Label(self, text="Not connected", wraplength=200,font=("Arial", fontsize))
        self.status_label.pack(pady=10)

         # Create a separator line
        separator2 = tk.Frame(self, bd=5, relief='sunken', height=10)
        separator2.pack(fill="x", pady=5, padx=5)
     
       # Serial object to hold the connection
        self.ser = None
        self.filename = ""  # Global variable for filename
        self.filename_label = ""  # Global variable for filename label

  
        # Create the start record button
        self.setting_button = tk.Button(self, text="Settings", command=self.open_text_editor,font=("Arial", fontsize))
        self.setting_button.pack(pady=10, anchor='center')
 
        # Display the filename as the title in the right frame
        self.filename_label = tk.Label(self, text=f"Filename: {self.filename}", font=("Arial", 10))
        self.filename_label.pack()

      
     # Create a separator line
        separator2 = tk.Frame(self, bd=5, relief='sunken', height=10)
        separator2.pack(fill="x", pady=5, padx=5)
   
     # Create the show CSV button
        show_plot_button = tk.Button(self, text="Show Plot", command=self.show_plot,font=("Arial", fontsize))
        show_plot_button.pack(pady=10)
 
 # Create the show CSV button
        show_csv_button = tk.Button(self, text="Show Data CSV", command=self.show_csv,font=("Arial", fontsize))
        show_csv_button.pack(pady=10)


     # Create a separator line
        separator2 = tk.Frame(self, bd=5, relief='sunken', height=10)
        separator2.pack(fill="x", pady=5, padx=5)
   
    
      # Create the start record button
        self.dataset_button = tk.Button(self, text="Show Dataset", command=self.show_dataset,font=("Arial", fontsize))
        self.dataset_button.pack(pady=10, anchor='center')
 
    # Create the start record button
        self.addlabel_button = tk.Button(self, text="Add Label", command=self.open_dataset_file,font=("Arial", fontsize))
        self.addlabel_button.pack(pady=10, anchor='center')
 
   # Create a separator line
        separator2 = tk.Frame(self, bd=5, relief='sunken', height=10)
        separator2.pack(fill="x", pady=5, padx=5)
   
        # Create the exit button
        exit_button = tk.Button(self, text="Exit", command=self.exit_app,font=("Arial", fontsize))
        exit_button.pack(pady=10)
  
    
    # Open a text editor or input field for editing configuration
    def open_text_editor(self):
          
        config_editor = tk.Toplevel(self)
        config_editor.title("Configuration Editor")
        config_editor.geometry("400x300")

  # Save button to update the config.ini file
        def save_config():
             # Use the nonlocal keyword to update the global filename variable
            config_content = config_text.get("1.0", tk.END)
            with open("config.ini", "w") as config_file:
                config_file.write(config_content)
            messagebox.showinfo("Success", "Configuration saved successfully.")
            config_editor.destroy()

        # Update the filename variable and label text
            self.filename = config.get("Serial", "filename")
            self.filename_label.config(text=f"Filename: {self.filename}")
            self.filename_label.pack()

        save_button = tk.Button(config_editor, text="Save", command=save_config)
        save_button.pack(side=tk.TOP)

 

    # Text widget for editing the configuration
        config_text = tk.Text(config_editor)
        config_text.pack(fill=tk.BOTH, expand=True)

    # Load the current configuration from the config.ini file
        config = configparser.ConfigParser()
        config.read("config.ini")
        # Get all sections in the config.ini file
        sections = config.sections()
     
    # Iterate through the sections and retrieve their content
        config_content = ""
        for section in sections:
            config_content += f"[{section}]\n"
            for option in config.options(section):
                value = config.get(section, option)
                config_content += f"{option} = {value}\n"

    # Insert the current configuration content into the text widget
            config_text.insert(tk.END, config_content)

  
    def open_dataset_file(self):
        folder_pathdata = "D:\python-project\dataset"  # Specify the folder path
      
        csv_file = folder_pathdata+ "\combined_group_sum_averages.csv"
        text_editor_cmd = ["notepad", csv_file]  # Replace "notepad" with your desired text editor program

        try:
            subprocess.run(text_editor_cmd)
        except FileNotFoundError:
            print(f"Unable to open file '{csv_file}' with the specified text editor.")

    
    def connect_serial(self):

        try:
            # Open the serial port
            self.ser = serial.Serial(self.port, self.baud_rate)
            self.status_label.config(text="Serial port connected.")
            print("Serial port connected.")
            self.is_capturing = True
            # Capture data here
              # Wait for 3 seconds
            self.master.after(3000, self.capture_data)

        except serial.SerialException:
            self.status_label.config(text="Failed to connect to the serial port.", wraplength=200)

    # Update button states
        self.connect_button.config(state=tk.DISABLED)
        self.disconnect_button.config(state=tk.NORMAL)
        self.right_frame.text_widget.pack(fill='both', expand=True)
        self.right_frame.csv_listbox.pack_forget()
        self.right_frame.treeview_frame.pack_forget()
        self.right_frame.dataset_frame.pack_forget()
        self.right_frame.plot_frame.pack_forget()
      

    
    def capture_data(self):
        if self.is_capturing:
            if self.ser and self.ser.is_open:
                # Read data from the serial port
                data = self.ser.readline().decode('utf-8').strip()
                if data:
                    # Append the received data to the text widget
                    print(data)
                    self.right_frame.text_widget.insert('end', data + '\n')
                    # Scroll the text widget to show the latest data
                    self.right_frame.text_widget.see('end')

                    # Create the respondent folder if it doesn't exist
                    if not os.path.exists(self.respondent_folder):
                        os.makedirs(self.respondent_folder)

                    # Extract specific columns from the data
                    columns = [7]  # Specify the column indices you want to save
                    data_columns = [int(data.split(',')[col]) / 100000 for col in columns]  # Divide by 10000

                    # Prepend timestamp to the extracted columns
                    #timestamp = datetime.now().strftime("%M:%S")
                    #timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #row_data = [timestamp] + data_columns

                    # Append the received data to the CSV file
                    csv_file_path = os.path.join(self.respondent_folder, f"{self.filename}.csv")
                    is_new_file = not os.path.exists(csv_file_path)  # Check if the file is new
                    
                     # Get the current number of rows in the CSV file
                    num_rows = 0
                    if not is_new_file:
                        with open(csv_file_path, "r") as csv_file:
                            reader = csv.reader(csv_file)
                            num_rows = sum(1 for _ in reader)
                    
                    with open(csv_file_path, "a", newline="") as csv_file:
                        writer = csv.writer(csv_file)
                        if is_new_file:  # Write the header if the file is new
                            writer.writerow(["Timestamp", "Data"])  # Replace with your actual header names
                        writer.writerow([num_rows, *data_columns])

            self.master.after(1, self.capture_data)


    def disconnect_serial(self):
        if self.ser:
            self.ser.close()
            self.ser = None
            self.status_label.config(text="Serial port disconnected.", wraplength=200)
            self.is_capturing=False
        
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.right_frame.text_widget.pack(fill='both', expand=True)
        self.right_frame.csv_listbox.pack_forget()
        self.right_frame.treeview_frame.pack_forget()
        self.right_frame.plot_frame.pack_forget()
        self.right_frame.dataset_frame.pack_forget()
      

    def exit_app(self):
        self.master.destroy()

   
    def show_csv(self):
        self.right_frame.treeview_frame.pack_forget()
      
        folder_path = "respondent"  # Specify the folder path
        csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]
        self.right_frame.update_csv_list(csv_files)
        
       
        self.right_frame.text_widget.pack_forget()
        self.right_frame.dataset_frame.pack_forget()
      

    def show_plot(self):
        self.right_frame.plot_frame.pack_forget()
            
        self.right_frame.update_plot_list()
        self.right_frame.text_widget.pack_forget()
        self.right_frame.treeview_frame.pack_forget()
        self.right_frame.dataset_frame.pack_forget()
      
    def show_dataset(self):
        folder_path = "respondent"  # Specify the folder path
        folder_pathdata = "dataset"  # Specify the folder path
        csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

        # List to store the group sum averages for each CSV file
        all_group_sum_averages = []

        # Iterate over each CSV file
        for file in csv_files:
            print(file)
            data_values = []

            # Read the "Data" column from the current CSV file and append to data_values
            with open(os.path.join(folder_path, file), "r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data_values.append(int(row["Data"]))

            # Divide the data_values into four groups
            group_size = 120
            groups = [data_values[i:i+group_size] for i in range(0, len(data_values), group_size)]

            # Calculate the sum average for each group
            group_sum_averages = [sum(group) / group_size for group in groups]

            print(group_sum_averages)
            all_group_sum_averages.append(group_sum_averages)

        # Save the all_group_sum_averages to a combined CSV file
        output_file = "combined_group_sum_averages.csv"

        with open(os.path.join(folder_pathdata, output_file), "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            # Write the header row
            writer.writerow(["Baseline","Soal","Membaca"])
            # Write the data rows
            writer.writerows(all_group_sum_averages)
 
        self.right_frame.update_dataset_list()
        self.right_frame.csv_listbox.pack_forget()
        self.right_frame.treeview_frame.pack_forget()
        self.right_frame.plot_frame.pack_forget()
        self.right_frame.text_widget.pack_forget()
        