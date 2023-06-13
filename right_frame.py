import os
import pickle
import statistics
import tkinter as tk
import tkinter.ttk as ttk
import csv
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn import svm
from sklearn.metrics import accuracy_score

class RightFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Create a text title label
        title_label = tk.Label(self, text="Brainwave Monitoring System - Naira - versi 0.2", font=("Arial", 15))
        title_label.pack(pady=0)

        # Create a text widget
        self.text_widget = tk.Text(self, font=("Arial", 12))
        self.text_widget.visible = False
 
        # Create a listbox to display the CSV filenames
        self.csv_listbox = tk.Listbox(self, height=5, font=("Arial", 10), width=50)
        self.csv_listbox.visible = False
       
        # Create a listbox to display the CSV filenames
        self.csv_listbox2 = tk.Listbox(self, height=5, font=("Arial", 10), width=50)
        self.csv_listbox2.visible = False
     
# Create a text title label
        self.average_label = tk.Label(self,text='yelo', font=("Arial", 10))
        self.average_label.visible = False
     
 
        # Configure the grid to expand the listbox when the window is resized
      #  self.grid_rowconfigure(1, weight=1)
       # self.grid_columnconfigure(2, weight=1)

        # Create a frame for the Treeview and scrollbar
        self.treeview_frame = tk.Frame(self,width=50)
        self.csv_treeview = ttk.Treeview(self.treeview_frame, show="headings")
        self.treeview_frame.visible = False
      
        # Create a frame for the Treeview and scrollbar
        self.dataset_frame = tk.Frame(self,width=200)
        self.dataset_treeview = ttk.Treeview(self.dataset_frame, show="headings")
        self.dataset_frame.visible = False
 
        # Create a frame for the plot canvas
        self.plot_frame = tk.Frame(self,width=50)
        self.plot_frame.visible = False
      


    def update_dataset_list(self):
        folder_pathtraining = "training"  # Specify the folder path
        folder_pathdataset = "dataset"  # Specify the folder path
        selected_file = "combined_group_sum_averages.csv"

        csv_files = [file for file in os.listdir(folder_pathtraining) if file.endswith(".csv")]

        self.average_label.pack_forget()
       
        # List to store the group sum averages for each CSV file
        all_group_sum_averages = []

        # Iterate over each CSV file
        for file in csv_files:

            #  print(file)
            data_values = []

        # Read the "Data" column from the current CSV file and append to data_values
            with open(os.path.join(folder_pathtraining, file), "r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data_values.append(int(row["Data"]))

        # Divide the data_values into four groups
            group_size = 120
            groups = [data_values[i:i+group_size] for i in range(0, len(data_values), group_size)]

        # Calculate the sum average for each group
            group_sum_averages = [round(sum(group) / group_size) for group in groups]

        # print(group_sum_averages)
            all_group_sum_averages.append(group_sum_averages)

        # Save the all_group_sum_averages to a combined CSV file
        # output_file = "combined_group_sum_averages.csv"
           
            with open(os.path.join(folder_pathdataset, selected_file), "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
            # Write the header row
                writer.writerow(["Baseline","Soal","Membaca"])
            # Write the data rows
                writer.writerows(all_group_sum_averages)
 
        # Create the Treeview widget
        self.dataset_frame.pack()
        self.dataset_treeview.pack()
        
        # Clear the treeview
        self.dataset_treeview.delete(*self.dataset_treeview.get_children())

        # Read and display the CSV data in the treeview
        with open(os.path.join(folder_pathdataset, selected_file), 'r') as file:
        
            # Process the file
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            self.dataset_treeview['columns'] = headers
            self.dataset_treeview.heading("#0", text="Row")      
            for header in headers:
                self.dataset_treeview.heading(header, text=header)
                self.dataset_treeview.column(header, width=100)
                row_number = 1
            for row in csv_reader:
                self.dataset_treeview.insert("", "end", text=str(row_number), values=row)
                row_number += 1
        
        self.text_widget.pack_forget()
        self.plot_frame.pack_forget()
        self.csv_listbox2.pack_forget()  
        # mulai average 
    #    data_valuesB = []
    #    data_valuesS = []
    #    data_valuesM = []
    #    column_averageB = []  # List to store column averages
    #    column_averageS = []  # List to store column averages
    #    column_averageM = []  # List to store column averages
    #    column_averages = []  # List to store column averages

     #   with open(os.path.join(folder_pathdataset, selected_file), "r") as csv_file:
     #       reader = csv.DictReader(csv_file)
     #       for row in reader:
      #          data_valuesB.append(int(row["Baseline"]))
       #         data_valuesS.append(int(row["Soal"]))
       #         data_valuesM.append(int(row["Membaca"]))
            
        #   print('data_valuesB', data_valuesB) 
        #   print('data_valuesS', data_valuesS) 
        #   print('data_valuesM', data_valuesM) 
     #   column_averageB = statistics.mean(data_valuesB)
     #   column_averageS = statistics.mean(data_valuesS)
     #   column_averageM = statistics.mean(data_valuesM)
          
        #   print('column_averageB', column_averageB) 
        #  print('column_averageS', column_averageS) 
        #  print('column_averageM', column_averageM)   
     #   column_averages.append(round(column_averageB))
     #   column_averages.append(round(column_averageS))
     #   column_averages.append(round(column_averageM))
        
        # print('column_averages = ', column_averages) 
     #   labels = ["Baseline", "Soal", "Membaca"]
     #   input_value = 129000

     #   self.dataset_treeview.insert("", "end", text="", values=("", "", ""))
     #   self.dataset_treeview.insert("", "end", text="", values=("", "", ""))
     #   self.dataset_treeview.insert("", "end", text="", values=("Average Baseline", "Average Soal", "Average Membaca"))
     #   self.dataset_treeview.insert("", "end", text=str(row_number), values=column_averages)
                 
      #  distances = np.abs(np.array(column_averages) - input_value)
      #  nearest_feature_index = np.argmin(distances)
      #  nearest_feature = labels[nearest_feature_index]

        # print(f"The nearest feature to {input_value} is '{nearest_feature}'")
        
        
        # data baru
      #  unseen_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]
      #  self.csv_listbox2.pack(side=tk.LEFT)
        
      #  self.csv_listbox2.bind("<<ListboxSelect>>", self.show_selected_average)
      #  self.csv_listbox2.delete(0, tk.END)
        
        # Add the CSV filenames to the listbox
       # for file in unseen_files:
        #    self.csv_listbox2.insert(tk.END, file) 



    def test_dataset_list(self):
        folder_pathdataset = "unseendata"  # Specify the folder path
        folder_pathmodel = "model"  # Specify the folder path
        model_file = "svm_model.pkl"

        self.average_label.pack_forget()
       
          
        # data baru
        unseen_files = [file for file in os.listdir(folder_pathdataset) if file.endswith(".csv")]
        self.csv_listbox2.pack(side=tk.LEFT)
        
        self.csv_listbox2.bind("<<ListboxSelect>>", self.show_selected_test)
        self.csv_listbox2.delete(0, tk.END)
        
        # Add the CSV filenames to the listbox
        for file in unseen_files:
            self.csv_listbox2.insert(tk.END, file) 
 
        
       


    def train_dataset_list(self,data,accuracy):

        print(data)
        print("Accuracy:", accuracy)

        folder_pathdataset = "dataset"  # Specify the folder path
        selected_file = "combined_group_sum_averages_labeled.csv"

       
         # Create the Treeview widget
        self.dataset_frame.pack(fill="none", expand=True)
        self.dataset_treeview.pack(fill="none", expand=True, pady=(0, 2))
        
        # Clear the treeview
        self.dataset_treeview.delete(*self.dataset_treeview.get_children())

        # Read and display the CSV data in the treeview
        with open(os.path.join(folder_pathdataset, selected_file), "r") as csv_file:
        
            # Process the file
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            self.dataset_treeview['columns'] = headers
            self.dataset_treeview.heading("#0", text="Row")      
            for header in headers:
                self.dataset_treeview.heading(header, text=header)
                self.dataset_treeview.column(header, width=100)
                row_number = 1
            for row in csv_reader:
                self.dataset_treeview.insert("", "end", text=str(row_number), values=row)
                row_number += 1
            
        self.average_label.config(text=f"Accuracy : {accuracy}\n   SVM Classification Mode saved at model folder", 
                          font=("Arial", 12), padx=10, pady=10)
        self.average_label.pack(side=tk.LEFT)
        self.plot_frame.pack_forget()
               

    def unseen_dataset_list(self):
        folder_pathdataset = "respondent"  # Specify the folder path
        self.average_label.pack_forget()
       
        # data baru
        unseen_files = [file for file in os.listdir(folder_pathdataset) if file.endswith(".csv")]
        self.csv_listbox2.pack(side=tk.LEFT)
        
        self.csv_listbox2.bind("<<ListboxSelect>>", self.show_selected_unseen)
        self.csv_listbox2.delete(0, tk.END)
        
        # Add the CSV filenames to the listbox
        for file in unseen_files:
            self.csv_listbox2.insert(tk.END, file) 
 
         
        self.plot_frame.pack_forget()
               

    def update_csv_list(self):
        folder_path = "respondent"  # Specify the folder path
        csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]
      
            # Clear the listbox
        self.csv_listbox.pack()
        self.csv_listbox.bind("<<ListboxSelect>>", self.show_selected_data)
        self.csv_listbox.delete(0, tk.END)

        # Add the CSV filenames to the listbox
        for file in csv_files:
            self.csv_listbox.insert(tk.END, file)

        # Create the Treeview widget
        self.treeview_frame.pack(fill="none", expand=False)
        self.csv_treeview.pack(fill="none", expand=False, pady=(0, 2))
        
        self.text_widget.pack_forget()
        self.plot_frame.pack_forget()
    
    def update_plot_list(self):
        # Create a listbox to display the CSV filenames
        folder_path = "respondent"  # Specify the folder path
        csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]
       
        if not self.csv_listbox.winfo_ismapped():
            
              
            self.csv_listbox.pack()
            self.csv_listbox.bind("<<ListboxSelect>>", self.show_selected_plot)
            self.csv_listbox.delete(0, tk.END)
        
           
        # Add the CSV filenames to the listbox
            for file in csv_files:
                self.csv_listbox.insert(tk.END, file)
            
            self.plot_frame.pack(fill="both", expand=True)
            
            self.text_widget.pack_forget()
            self.treeview_frame.pack_forget()
            self.csv_treeview.pack_forget()
        
        
        
        else:
            self.csv_listbox.pack()
            self.csv_listbox.bind("<<ListboxSelect>>", self.show_selected_plot)
            self.csv_listbox.delete(0, tk.END)
            
        
        # Add the CSV filenames to the listbox
            for file in csv_files:
                self.csv_listbox.insert(tk.END, file)
                
            self.plot_frame.pack_forget()
            self.clear_plot()
        
        self.fig, self.ax = plt.subplots()
        self.plot_canvas = None 
        
        self.text_widget.pack_forget()
        self.treeview_frame.pack_forget()

    def show_selected_data(self, event):
            # Get the selected filename from the listbox
        folder_path = "respondent"  # Specify the folder path
      
        selected_index = self.csv_listbox.curselection()
        if selected_index:
            selected_file = self.csv_listbox.get(selected_index)

                # Clear the treeview
            self.csv_treeview.delete(*self.csv_treeview.get_children())

                # Read and display the CSV data in the treeview
            with open(os.path.join(folder_path, selected_file), 'r') as file:
                    # Process the file
                csv_reader = csv.reader(file)
                headers = next(csv_reader)
                self.csv_treeview['columns'] = headers
                self.csv_treeview.heading("#0", text="Row")
                for header in headers:
                    self.csv_treeview.heading(header, text=header)
                    self.csv_treeview.column(header, width=100)
                    row_number = 1
                    for row in csv_reader:
                        self.csv_treeview.insert("", "end", text=str(row_number), values=row)
                        row_number += 1
                
        
    def show_selected_plot(self, event):
            # Get the selected filename from the listbox
        self.plot_frame.pack(fill="both", expand=True)
        selected_index = self.csv_listbox.curselection()
        if selected_index:
            selected_file = self.csv_listbox.get(selected_index)
                
            self.clear_plot()
                # Plot the data from the CSV file
            self.plot_csv_data(selected_file)

    def show_selected_average(self,event):
            # Get the selected filename from the listbox
        folder_pathdataset = "dataset"  # Specify the folder path
        folder_path = "respondent"  # Specify the folder path
      
      
       
        selected_index = self.csv_listbox2.curselection()
         
        if selected_index:
            selected_file = self.csv_listbox2.get(selected_index)
            print(selected_file)
            
            # mulai average 
            data_valuesB = []
            data_valuesS = []
            data_valuesM = []
            column_averageB = []  # List to store column averages
            column_averageS = []  # List to store column averages
            column_averageM = []  # List to store column averages
            column_averages = []  # List to store column averages

            with open(os.path.join(folder_pathdataset,'combined_group_sum_averages.csv'), "r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data_valuesB.append(int(row["Baseline"]))
                    data_valuesS.append(int(row["Soal"]))
                    data_valuesM.append(int(row["Membaca"]))
            
                #   print('data_valuesB', data_valuesB) 
                #   print('data_valuesS', data_valuesS) 
                #   print('data_valuesM', data_valuesM) 
                column_averageB = statistics.mean(data_valuesB)
                column_averageS = statistics.mean(data_valuesS)
                column_averageM = statistics.mean(data_valuesM)
          
                #  print('column_averageB', column_averageB) 
                #  print('column_averageS', column_averageS) 
                #  print('column_averageM', column_averageM) 
                column_averages.append(round(column_averageB))
                column_averages.append(round(column_averageS))
                column_averages.append(round(column_averageM))
                data_values = [] 

                # List to store the group sum averages for each CSV file
                all_group_sum_averages = []

                # Process the file
                with open(os.path.join(folder_path, selected_file), "r") as csv_file:
                    # Process the file
                    csv_reader = csv.reader(csv_file)
                    next(csv_reader) 
                    for row in csv_reader:
                        data_values.append(int(row[1]))
                # print(data_values)         
                # Divide the data_values into four groups
                group_size = 120
                groups = [data_values[i:i+group_size] for i in range(0, len(data_values), group_size)]

                # Calculate the sum average for each group
                group_sum_averages = [round(sum(group) / group_size) for group in groups]

                # print(group_sum_averages)
                all_group_sum_averages.append(group_sum_averages)
              
                # print(all_group_sum_averages[0][0]) 
                # print(all_group_sum_averages[0][1]) 
                # print(all_group_sum_averages[0][2]) 
                print('Average Dataset = ', column_averages) 
                print('Average Data Test = ', all_group_sum_averages[0]) 
                labels = ["Baseline", "Soal", "Membaca"]

                distances0 = np.abs(np.array(column_averages) - all_group_sum_averages[0][0])
                nearest_feature_index0 = np.argmin(distances0)
                nearest_feature0 = labels[nearest_feature_index0]
                print(f"The nearest feature to {all_group_sum_averages[0][0]} is '{nearest_feature0}'")

                distances1 = np.abs(np.array(column_averages) - all_group_sum_averages[0][1])
                nearest_feature_index1 = np.argmin(distances1)
                nearest_feature1 = labels[nearest_feature_index1]
                print(f"The nearest feature to {all_group_sum_averages[0][1]} is '{nearest_feature1}'")
  
                distances2 = np.abs(np.array(column_averages) - all_group_sum_averages[0][2])
                nearest_feature_index2 = np.argmin(distances2)
                nearest_feature2 = labels[nearest_feature_index2]
               
                print(f"The nearest feature to {all_group_sum_averages[0][2]} is '{nearest_feature2}'")
   
                self.average_label.config(text=f"{labels}\nAverage Dataset {column_averages}\nAverage Data Test {all_group_sum_averages[0]}\nThe nearest feature to {all_group_sum_averages[0][0]} is {nearest_feature0} \nThe nearest feature to {all_group_sum_averages[0][1]} is {nearest_feature1}\nThe nearest feature to {all_group_sum_averages[0][2]} is {nearest_feature2}", 
                          font=("Arial", 12), padx=10, pady=10)
                self.average_label.pack(side=tk.LEFT)
      

    def show_selected_test(self,event):
            # Get the selected filename from the listbox
        folder_pathdata = "unseendata"  # Specify the folder path
        folder_pathmodel = "model"  # Specify the folder path
        model_file= "svm_model.pkl"
       # Load the trained SVM model
        model = svm.SVC()
        model = joblib.load(os.path.join(folder_pathmodel,model_file))

       
        selected_index = self.csv_listbox2.curselection()
         
        if selected_index:
            selected_file = self.csv_listbox2.get(selected_index)
            print(selected_file)
            
             # Prepare your unseen data
            unseen_data = pd.read_csv(os.path.join(folder_pathdata,selected_file))
            X_unseen = unseen_data.drop('Target', axis=1)  # Remove the target variable if present

            # Preprocess the unseen data (e.g., scaling/normalization)

            # Make predictions on the unseen data
            predictions = model.predict(X_unseen)
            unseen_data['predicted_label'] = predictions

            print(unseen_data[['Target', 'predicted_label']])
        # Evaluate the model's performance
            accuracy = accuracy_score(unseen_data['Target'], predictions)
            print(f"Accuracy: {accuracy}")
    
            
            
            self.average_label.config(text=f"Accuracy : {accuracy}\n\n{unseen_data[['Target', 'predicted_label']]}", 
                          font=("Arial", 12), padx=10, pady=10)
            self.average_label.pack(side=tk.LEFT)



    def show_selected_unseen(self,event):
            # Get the selected filename from the listbox
        folder_pathunseen = "unseendata"  # Specify the folder path
        folder_path = "respondent"  # Specify the folder path
        
       
        selected_index = self.csv_listbox2.curselection()
         
        if selected_index:
            selected_file = self.csv_listbox2.get(selected_index)
            print(selected_file)
             
            all_group_sum_averages = []

            data_values = []
             # Read the "Data" column from the current CSV file and append to data_values
            with open(os.path.join(folder_path, selected_file), "r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data_values.append(int(row["Data"]))

        # Divide the data_values into four groups
            group_size = 120
            groups = [data_values[i:i+group_size] for i in range(0, len(data_values), group_size)]

        # Calculate the sum average for each group
            group_sum_averages = [round(sum(group) / group_size) for group in groups]
            group_sum_averages.append("''")

        # print(group_sum_averages)
            all_group_sum_averages.append(group_sum_averages)
          
            print(all_group_sum_averages)
           
            unseen_selected_file = "unseen_"+selected_file

            with open(os.path.join(folder_pathunseen, unseen_selected_file), "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
            # Write the header row
                writer.writerow(["Baseline","Soal","Membaca","Target"])
            # Write the data rows
                writer.writerows(all_group_sum_averages)
 
            
            self.average_label.config(text=f"Average Dataset\nBaseline   Soal   Mwmbaca\n {all_group_sum_averages[0]}\n\nUnseen Dataset created at unseendata folder", 
                          font=("Arial", 12), padx=10, pady=10)
            self.average_label.pack(side=tk.LEFT)
    


    def clear_plot(self):
        # Clear the previous plot
        if self.plot_canvas:
            self.ax.clear()  # Clear the plot axes
            self.plot_canvas.draw()  # Redraw the canvas to clear the plot
            self.plot_canvas.get_tk_widget().destroy()  # Destroy the canvas widget
            self.plot_canvas = None  # Set the plot canvas to None

    def plot_csv_data(self, csv_file):
        
        folder_pathdata = "respondent"  # Specify the folder path
        
        # Clear the previous plot
        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().destroy()

        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(os.path.join(folder_pathdata, csv_file))

        # Extract the data for plotting
        x = data['Timestamp']
        y = data['Data']

        # Plot the data
        self.ax.plot(x, y/10000)

        # Customize the plot if needed
        self.ax.set_xlabel('X-axis', fontsize=10)  # Increase the font size of x-axis label
        self.ax.set_ylabel('Y-axis', fontsize=10)  # Increase the font size of y-axis label
        self.ax.set_title('Data Plot', fontsize=10)  # Increase the font size of the plot title

        # Increase the font size of tick labels on both axes
        self.ax.tick_params(axis='x', labelsize=10)
        self.ax.tick_params(axis='y', labelsize=10)

        # Create a new canvas to display the plot
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.plot_canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Initialize other components or variables as needed