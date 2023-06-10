import tkinter as tk
import tkinter.ttk as ttk
import csv
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class RightFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create a text title label
        title_label = tk.Label(self, text="Brainwave Monitoring - Naira - versi 0.2", font=("Arial", 15))
        title_label.pack(pady=0)



      # Create a text widget
        self.text_widget = tk.Text(self, font=("Arial", 12))
        self.text_widget.visible = False
 
        # Create a listbox to display the CSV filenames
        self.csv_listbox = tk.Listbox(self, height=5, font=("Arial", 10))
        self.csv_listbox.visible = False
       
       # Configure the grid to expand the listbox when the window is resized
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

 
   # Create a frame for the Treeview and scrollbar
        self.treeview_frame = tk.Frame(self,width=50)
        self.csv_treeview = ttk.Treeview(self.treeview_frame, show="headings")
        self.treeview_frame.visible = False
      
    
  # Create a frame for the plot canvas
        self.plot_frame = tk.Frame(self,width=300)
        self.plot_frame.visible = False
      
        
  
    def update_csv_list(self, csv_files):
       
        # Clear the listbox
        self.csv_listbox.pack(fill='both', expand=False)
        self.csv_listbox.bind("<<ListboxSelect>>", self.show_selected_data)
        self.csv_listbox.delete(0, tk.END)

        # Add the CSV filenames to the listbox
        for file in csv_files:
            self.csv_listbox.insert(tk.END, file)

# Create the Treeview widget
        self.treeview_frame.pack(fill="both", expand=True)
        self.csv_treeview.pack(fill="both", expand=True, pady=(0, 2))
        
        self.text_widget.pack_forget()
        self.plot_frame.pack_forget()
      
   
    
    def update_plot_list(self, csv_files):
          # Create a listbox to display the CSV filenames
        self.csv_listbox.pack()
        self.csv_listbox.bind("<<ListboxSelect>>", self.show_selected_data)
        self.csv_listbox.delete(0, tk.END)
        
        
       
        # Add the CSV filenames to the listbox
        for file in csv_files:
            self.csv_listbox.insert(tk.END, file)
 
        self.plot_frame.pack(fill="both", expand=True)
   
        self.fig, self.ax = plt.subplots()
        self.plot_canvas = None
       
        self.text_widget.pack_forget()
        self.treeview_frame.pack_forget()
      
    
    def show_selected_data(self, event):
            # Get the selected filename from the listbox
            
            selected_index = self.csv_listbox.curselection()
            if selected_index:
                selected_file = self.csv_listbox.get(selected_index)

                # Clear the treeview
                self.csv_treeview.delete(*self.csv_treeview.get_children())

                # Read and display the CSV data in the treeview
                with open('D:\\python-project\\respondent\\' + selected_file, 'r') as file:
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

                self.clear_plot()
                # Plot the data from the CSV file
                self.plot_csv_data(selected_file)
   
   
    def clear_plot(self):
        # Clear the previous plot
        if self.plot_canvas:
            self.ax.clear()  # Clear the plot axes
            self.plot_canvas.draw()  # Redraw the canvas to clear the plot
            self.plot_canvas.get_tk_widget().destroy()  # Destroy the canvas widget
            self.plot_canvas = None  # Set the plot canvas to None

    
    
    def plot_csv_data(self, csv_file):
        # Clear the previous plot
        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().destroy()

        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv('D:\\python-project\\respondent\\' + csv_file)

        # Extract the data for plotting
        x = data['Timestamp']
        y = data['Data']

        # Plot the data
        self.ax.plot(x, y)

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