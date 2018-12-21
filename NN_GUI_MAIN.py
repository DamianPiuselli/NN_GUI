# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 16:30:19 2018

@author: Damian Piuselli
"""
import tkinter as tk
from tkinter import ttk as ttk
from tkinter import font as tkfont 
from tkinter import filedialog
import pandas as pd
import numpy as np
#from keras import Sequential
#from keras.layers import Dense, Dropout
#from keras import backend as K

#Main class for the App, main window.
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Verdana', size=12, weight='bold')
        self.title('NN_GUI')
        
        #Creating a container for a toolbar at the top of the main window
        self.toolbar_container = tk.Frame(self)
        self.toolbar_container.pack(side="top", fill="x", expand=True, anchor='n')
         
        #Creating a toolbar for switching between frames
        self.toolbar = Toolbar(parent=self.toolbar_container, controller=self)
        self.toolbar.pack(side="top", fill="x", expand=True)
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="x", expand=True, anchor='n' )
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoadData, Compile): #Frame classes that make each window.
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoadData")
        
        #Creating a container for the statusbar at the bottom of the main window
        self.statusbar_container = tk.Frame(self)
        self.statusbar_container.pack(side="bottom", fill="x", expand=True, anchor='s')   
        
        #Creating a statusbar
        self.statusbar = StatusBar(parent=self.statusbar_container, controller=self)
        self.statusbar.pack(side="bottom", fill="x", expand=True)


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
#toolbar class
class Toolbar(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
              
        #make a toolbar button for switching between frames
        for F in ('LoadData', 'Compile'):
            self.new_button(controller,F)
        
    #make a toolbar button for switching between frames
    def new_button(self,controller, page_name):
        self.button = ttk.Button(self, text=page_name,
                           command=lambda: controller.show_frame(page_name))
        self.button.pack(side='left', fill='x', expand=False, ipady=3)

#status bar class
class StatusBar(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self,text='testing...', bd=1, relief='sunken', anchor='sw')
        self.label.pack(fill='x')

    def set_status(self, status_text):
        self.label.config(text=status_text)
        self.label.update_idletasks()
    
    def clear_status(self):
        self.label.config(text='')
        self.label.update_idletasks()

#Load Data window class
class LoadData(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #reference to controller app
        self.controller = controller
        #title
        self.title = tk.Label(self, text="Load Data", font=controller.title_font, anchor= 'nw', bd=5)
        self.title.grid(row=0, columnspan=1, sticky='NW')
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.grid(row=1, column=0,  columnspan=10, sticky="WE")
        #initializing train and test data
        self.data = None
        self.train_data = None
        self.test_data = None
        #load data widgets
        self.load_data_button = ttk.Button(self, text="Open training data file",
                           command=lambda: self.load_train_data())
        self.load_data_button.grid(row=2, column=0, sticky="W")
        self.separator2 = ttk.Separator(self, orient="horizontal")
        self.separator2.grid(row=3, column=0,  columnspan=10, sticky="WE") 
        #displaying data dimensions
        self.data_shape = tk.StringVar()
        self.data_shape.set('No loaded data')
        self.dim_label = tk.Label(self, textvariable= self.data_shape)
        self.dim_label.grid(row=2, column=1, sticky='W')
        #spliting loaded data between x_data and y_data
        self.split_label = tk.Label(self, text= 'Split data between \nfeatures and labels')
        self.split_label.grid(row= 4, column=0, sticky='W')
        
    #load csv or excel files as train_data    
    def load_train_data(self):
        #ask for the filepath, then import as a dataframe with pandas with the appropiate function
        
        file_path = filedialog.askopenfilename(title= 'select file', filetypes= [('Tabular Data', '*.csv *.xls *.xlsx')])
        if file_path[-3:] == 'csv':
            self.data = pd.read_csv(file_path)
        elif file_path[-3:] == 'xls' or file_path[-4:] == 'xlsx':
            self.data = pd.read_excel(file_path)
        else:
            self.data = None
        #number of columns and rows in the datafile
        if self.data is not None:
            rows, columns = self.data.shape
            self.data_shape.set('Loaded data has '+str(columns) +' columns and ' +str(rows)+' rows')
        else:
            self.data_shape.set('No Loaded Data')

#Compile window class.
class Compile(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #reference to controller app
        self.controller = controller
        #title
        self.title = tk.Label(self, text="Compile Model",bd=5, 
                              font=controller.title_font, anchor= 'w')
        self.title.grid(row=0, columnspan=1, sticky='NW')
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.grid(row=1, column=0,  columnspan=10, sticky="WE")
        #first widget gets the number of layers of the NN.
        #apply button, call the draw_layers method
        self.label = ttk.Label(self, text='Number of Layers :', anchor= 'w')
        self.layers = tk.Spinbox(self, from_ =1, to_ =25, increment=1)
        self.layers_apply = ttk.Button(self, text='Apply', command=self.draw_layers)
        self.label.grid(row=2, column=0)
        self.layers.grid(row=2, column=1)
        self.layers_apply.grid(row=2, column=2)
        self.separator2 = ttk.Separator(self, orient="horizontal")
        self.separator2.grid(row=3, column=0,  columnspan=10, sticky="WE")
        
        #list of widgets initialized empty
        self.layer_types = ('Dense','Dropout')
        self.layers_widgets = []
        #list of dicts with the user inputted configuration
        self.model_configuration = []
        # Compile buttton initilalizated as an empty frame
        self.compile_button = tk.Frame()
                
    #each type of layer have a different set of options and therefore 
    #different gui elements asociated to it. first draw_layers will display
    #a list of all the available layers types. Then when the type is selected
    #the rest of the gui elements are dynamically drawn.
    #for each layer im reserving 2 rows of space, to allow for options heavy
    #layer types to potentially have more space available.
    #the widgets are stored in a list 
    def draw_layers(self):
        #destroying all widgets created on the last call to the function
        for widget in self.layers_widgets:
            widget.destroy()
            
        self.compile_button.destroy()
        
        #deleting all references
        self.model_configuration = []
        self.layers_widgets = []
        
        #creating the appropiate number of widgets and storing a reference
        #in layers_widgets list
        
        for i in range(int(self.layers.get())):
            layer_widget = LayerWidget(self,i)
            layer_widget.grid(row=i+4, columnspan=5, sticky='w')
            self.layers_widgets.append(layer_widget)
            
        #shows a compile button in the last row    
        self.compile_button = ttk.Button(self, text='Compile', command=self.compile_network) 
        self.compile_button.grid(rows=int(self.layers.get())+6, column = 8)
        
    #this function gets a list of dictionary for each layer, with the current 
    #user input configuration
    def model_data(self):                
        self.model_configuration = []
        
        for widget in self.layers_widgets:
            self.model_configuration.append(widget.layer_data())

    #returns the adequate keras function to build the network from the information
    #passed in each dictionary in model_data
    def compile_layer(self, **kargs):
        
        if kargs['layer_type'] == 'Dense' and kargs['layer_index'] == 0:
            self.model.add(Dense(units= int(kargs['units']), activation= kargs['activation'], 
                            use_bias= kargs['use_bias'], kernel_initializer= kargs['kernel_initializer'],
                            bias_initializer= kargs['bias_initializer'], input_dim= int(kargs['input_shape'])))
        
        elif kargs['layer_type'] == 'Dense':
            self.model.add(Dense(units= int(kargs['units']), activation= kargs['activation'], 
                            use_bias= kargs['use_bias'], kernel_initializer= kargs['kernel_initializer'],
                            bias_initializer= kargs['bias_initializer']))
            
        elif kargs['layer_type'] == 'Dropout':
            self.model.add(Dropout(rate= float(kargs['rate'])))
        
        
    #multiple calls to compile layer method
    def compile_network(self):
        
        K.clear_session()
        self.model = Sequential()
        
        self.model_data()
               
        for layer in self.model_configuration:
            print(layer)
            self.compile_layer(**layer)
        print(self.model.summary())














#run app if nn_py_main is main.
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()