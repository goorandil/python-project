import configparser
import csv
import datetime
import subprocess
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import joblib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import serial
import os
from datetime import datetime

class LeftFrame(tk.Frame):
    def __init__(self, parent, port, baud_rate, right_frame,capturecolumn):
        super().__init__(parent)
        self.pack_propagate(False)
        self.config(width=150)
        self.port = port
        self.baud_rate = baud_rate
        self.capturecolumn = capturecolumn
        self.is_capturing = False
        self.right_frame = right_frame
        self.respondent_folder = "respondent"
        self.respondent_folderrawdata = "rawdata"

        # Set the fontsize
        fontsize = 10

        """ start 
            all menu button
            left side
        """
        # Serial object to hold the connection
        self.ser = None
        self.filename = ""  # Global variable for filename
        self.filename_label = ""  # Global variable for filename label

        # Create the start record button
        self.setting_button = tk.Button(self, text="Settings", command=self.open_text_editor,font=("Arial", fontsize))
        self.setting_button.pack()
 
        # Display the filename as the title in the right frame
        self.filename_label = tk.Label(self, text=f"Filename: {self.filename}", font=("Arial", 10))
        self.filename_label.pack()

        # Create a separator line
        separator2 = tk.Frame(self, bd=3, relief='sunken', height=5)
        separator2.pack(fill="x", pady=3, padx=3)

        # Create the connect button
        self.connect_button = tk.Button(self, text="Connect/Record", command=self.connect_serial,font=("Arial", fontsize))
        self.connect_button.pack(pady=3)

        # Create the disconnect button
        self.disconnect_button = tk.Button(self, text="Disconnect/Stop", command=self.disconnect_serial,font=("Arial", fontsize), state=tk.DISABLED)
        self.disconnect_button.pack(pady=3)

        # Set initial button states
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)

        # Create the status label
        self.status_label = tk.Label(self, text="Not connected", wraplength=200,font=("Arial", fontsize))
        self.status_label.pack(pady=3)

        # Create a separator line
        separator2 = tk.Frame(self, bd=3, relief='sunken', height=5)
        separator2.pack(fill="x", pady=3, padx=3)

        # Create the show CSV button
        show_plot_button = tk.Button(self, text="Show Plot", command=self.show_plot,font=("Arial", fontsize))
        show_plot_button.pack(pady=3)
 
        # Create the show CSV button
        show_csv_button = tk.Button(self, text="Show Data CSV", command=self.show_csv,font=("Arial", fontsize))
        show_csv_button.pack(pady=3)


 # Create a separator line
        separator2 = tk.Frame(self, bd=3, relief='sunken', height=5)
        separator2.pack(fill="x", pady=3, padx=3)
   
    
      # Create the start record button
        self.dataset_button = tk.Button(self, text="Create Dataset", command=self.show_dataset,font=("Arial", fontsize))
        self.dataset_button.pack(pady=3, anchor='center')
   
    # Create the start record button
        self.addlabel_button = tk.Button(self, text="Add Label", command=self.open_dataset_file,font=("Arial", fontsize))
        self.addlabel_button.pack(pady=3, anchor='center')
 
  # Create the start record button
        self.train_button = tk.Button(self, text="Train Labeled Dataset", command=self.train_dataset_file,font=("Arial", fontsize))
        self.train_button.pack(pady=3, anchor='center')

  # Create the start record button
        self.unseen_button = tk.Button(self, text="Create Unseen Dataset", command=self.unseen_dataset_file,font=("Arial", fontsize))
        self.unseen_button.pack(pady=3, anchor='center')

# Create the start record button
        self.test_button = tk.Button(self, text="Test Unseen Data", command=self.test_dataset_file,font=("Arial", fontsize))
        self.test_button.pack(pady=3, anchor='center')

 # Create a separator line
        separator2 = tk.Frame(self, bd=3, relief='sunken', height=5)
        separator2.pack(fill="x", pady=3, padx=3)
   
  # Create the start record button
        self.test_button = tk.Button(self, text="Raw Data", command=self.show_rawdata,font=("Arial", fontsize))
        self.test_button.pack(pady=3, anchor='center')

  
   #Create a separator line
        separator2 = tk.Frame(self, bd=3, relief='sunken', height=5)
        separator2.pack(fill="x", pady=3, padx=3)
   
  
        # Create the exit button
        exit_button = tk.Button(self, text="Exit", command=self.exit_app,font=("Arial", fontsize))
        exit_button.pack(pady=3)
  
    
        """ end 
            all menu button
            left side
        """

        """ START 
            all FUNCTION
            left side
        """

    # function Open a text editor or input field for editing configuration
  
     
    def show_rawdata(self):
        plt.switch_backend('TkAgg')  # Specify the backend

        print("show_rawdata")
        folder_pathdata = "rawdata"
        file_selected = "normal_2menit.csv"
        rawdata_file = os.path.join(folder_pathdata, file_selected)

        # Load EEG data from CSV file
        eeg_data = np.genfromtxt(rawdata_file, delimiter=',')

        # Apply FFT to raw signal
        fft_signal = np.fft.fft(eeg_data)

        # Define frequency bands
        lowbeta_band = [13, 16.75]
        highbeta_band = [18, 29.75]

        # Find indices corresponding to frequency bands
        n = len(eeg_data)
        fs = 512
        freq = np.fft.fftfreq(n, 1/fs)  # Frequency axis

        lowbeta_idx = np.where((freq >= lowbeta_band[0]) & (freq < lowbeta_band[1]))[0]
       
        # Set values outside frequency bands to zero
        fft_lowbeta = fft_signal.copy()
        fft_lowbeta[np.setdiff1d(range(n), lowbeta_idx)] = 0
        lowbeta_signal = np.fft.ifft(fft_lowbeta)

      
        # Generate time vector
        t = np.arange(n) / fs

        # Plot the signals
        plt.figure(figsize=(10, 6))

        plt.subplot(2, 1, 1)
        plt.plot(t, np.real(lowbeta_signal))
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Low Beta Band')

        plt.tight_layout()
        plt.show()

    
    
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

    
    # function editor menambahkan label untuk data yg belum dilabel
    # combined_group_sum_averages.csv hasilnya di save di combined_group_sum_averages_labeled.csv
    def open_dataset_file(self):
       
        folder_pathdata = "dataset" 
        file_selected = "combined_group_sum_averages.csv"# Specify the folder path
        csv_file = os.path.join(folder_pathdata, file_selected) 
               
        try:
            subprocess.run([csv_file], shell=True)
        except FileNotFoundError:
            print(f"Unable to open file '{csv_file}' with the specified text editor.")

 
    


    # function training dari  combined_group_sum_averages_labeled.csv
    # outputnya svm model disimpan difolder model
  
    def train_dataset_file(self):
        # Call the function to plot decision boundaries
        
        self.right_frame.plot_frame.pack_forget()
       
        folder_pathdata = "dataset" 
        flabeled = "combined_group_sum_averages_labeled.csv"# Specify the folder path
        folder_pathmodel = "model" 
        fmodel = "svm_model.pkl"# Specify the folder path
        labeled_file = os.path.join(folder_pathdata, flabeled) 
        model_file = os.path.join(folder_pathmodel, fmodel) 
        
         # Load the labeled dataset
        data = pd.read_csv(labeled_file)
        
        # Separate the features (X) and target labels (y)
        X = data.drop("Target", axis=1)
        y = data["Target"]

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=15)

        # Create an SVM classifier object
        clf = svm.SVC()

        # Train the SVM model on the training data
        clf.fit(X_train, y_train)

        # Save the trained model to a file
        joblib.dump(clf, model_file)

        # Make predictions on the test data
        y_pred = clf.predict(X_test)

        # Evaluate the accuracy of the model
        accuracy = accuracy_score(y_test, y_pred)
      
        self.right_frame.train_dataset_list(data,accuracy)
        
        self.right_frame.csv_listbox.pack_forget()
        self.right_frame.csv_listbox2.pack_forget()
        self.right_frame.treeview_frame.pack_forget()
        self.right_frame.text_widget.pack_forget()
     


    def unseen_dataset_file(self):
        self.right_frame.unseen_dataset_list()
        
        self.right_frame.csv_listbox.pack_forget()
        self.right_frame.treeview_frame.pack_forget()
        self.right_frame.plot_frame.pack_forget()
        self.right_frame.dataset_treeview.pack_forget()
        self.right_frame.text_widget.pack_forget()

    # Generate some random data for demonstration
        # function test data unseen dari folder unseendata
    # outputna akurasi
    def test_dataset_file(self):
         
         
        self.right_frame.test_dataset_list()
        
        self.right_frame.plot_frame.pack_forget()
        self.right_frame.treeview_frame.pack_forget()
        self.right_frame.dataset_treeview.pack_forget()
        self.right_frame.csv_listbox.pack_forget()
        self.right_frame.text_widget.pack_forget()
        
    
    
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
        self.right_frame.csv_listbox2.pack_forget()
        self.right_frame.treeview_frame.pack_forget()
        self.right_frame.dataset_frame.pack_forget()
        self.right_frame.plot_frame.pack_forget()
        self.right_frame.average_label.pack_forget()
       

    
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
                    columns = [self.capturecolumn]  # Specify the column indices you want to save
                    data_columns = [int(data.split(',')[col])  for col in columns]  # Divide by 10000

                    # Prepend timestamp to the extracted columns
                    #timestamp = datetime.now().strftime("%M:%S")
                    #timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #row_data = [timestamp] + data_columns

                    # Append the received data to the CSV file
                    csv_file_path = os.path.join(self.respondent_folder, f"{self.filename}.csv")
                    is_new_file = not os.path.exists(csv_file_path)  # Check if the file is new

                   # ini untuk raw data 
                    csv_file_pathrawdata = os.path.join(self.respondent_folderrawdata, f"{self.filename}.csv")
                    is_new_filerawdata = not os.path.exists(csv_file_path)  # Check if the file is new
                 
                     # Get the current number of rows in the CSV file
                    num_rows = 0
                    if not is_new_file:
                        with open(csv_file_path, "r") as csv_file:
                            reader = csv.reader(csv_file)
                            num_rows = sum(1 for _ in reader)

                   # ini untuk raw data 
                    if not is_new_filerawdata:
                        with open(csv_file_pathrawdata, "r") as csv_file:
                            reader = csv.reader(csv_file)
 
                    
                    
                    with open(csv_file_path, "a", newline="") as csv_file:
                        writer = csv.writer(csv_file)
                        if is_new_file:  # Write the header if the file is new
                            writer.writerow(["Timestamp", "Data"])  # Replace with your actual header names
                        writer.writerow([num_rows, *data_columns])

                
                   # ini untuk raw data 
                    with open(csv_file_pathrawdata, "a", newline="") as csv_file:
                        writer = csv.writer(csv_file)
                        if is_new_filerawdata:  # Write the header if the file is new
                            writer.writerow(["Data"])  # Replace with your actual header names
                        writer.writerow([*data_columns])

            
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
        self.right_frame.csv_listbox2.pack_forget()
        self.right_frame.treeview_frame.pack_forget()
        self.right_frame.plot_frame.pack_forget()
        self.right_frame.dataset_frame.pack_forget()
        self.right_frame.average_label.pack_forget()
       

    def exit_app(self):
        self.master.destroy()

   
    def show_csv(self):
        self.right_frame.treeview_frame.pack_forget()
     
        self.right_frame.update_csv_list()
        
        self.right_frame.text_widget.pack_forget()
        self.right_frame.plot_frame.pack_forget()
        self.right_frame.dataset_frame.pack_forget()
        self.right_frame.csv_listbox2.pack_forget()
        self.right_frame.average_label.pack_forget()
       

    def show_plot(self):
        self.right_frame.plot_frame.pack_forget()
            
        self.right_frame.update_plot_list()
        
        self.right_frame.text_widget.pack_forget()
        self.right_frame.treeview_frame.pack_forget()
        self.right_frame.dataset_frame.pack_forget()
        self.right_frame.csv_listbox2.pack_forget()
        self.right_frame.average_label.pack_forget()
       
        
# fungsi membuat ratarata dari data pwe 120  
    def show_dataset(self):
     
       
         
        self.right_frame.text_widget.pack_forget()
      #  self.right_frame.plot_frame.pack_forget()
        self.right_frame.csv_listbox.pack_forget()
        self.right_frame.csv_listbox2.pack_forget()
        self.right_frame.average_label.pack_forget()
        self.right_frame.update_dataset_list()
       