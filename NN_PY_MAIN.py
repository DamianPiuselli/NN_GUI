#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 22:39:53 2018

@author: Damian Piuselli
"""

import tkinter as tk
from tkinter import ttk as ttk
from tkinter import font as tkfont 


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
        for F in (StartPage, PageOne, PageTwo, Compile):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        
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


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="change status",
                           command=lambda: controller.statusbar.set_status("tessssssst1"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="change status",
                           command=lambda: controller.statusbar.set_status("tessssssst2"))
        button.pack()

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
        self.compile_button = ttk.Button(self, text='Compile', command=self.model_data) 
        self.compile_button.grid(rows=int(self.layers.get())+6, column = 8)
        
    #this function gets a list of dictionary for each layer, with the current 
    #user input configuration
    def model_data(self):
                
        self.model_configuration = []
        
        for widget in self.layers_widgets:
            self.model_configuration.append(widget.layer_data())
        print(self.model_configuration)
        return self.model_configuration
    
       
#custom widget for layers, to be drawn in the compile frame.        
class LayerWidget(tk.Frame):
    
    def __init__(self, parent, layer_index):
        tk.Frame.__init__(self, parent)
        #number of the layer stored in layed_index
        self.layer_index = layer_index
        #user info about the layer configuration is stored in a dict
        self.layer_dict = {}
        #type of the layer stored as a tk.stringvar
        self.layer_type = tk.StringVar()
        #default layer type is none
        self.default_layer_type = None
        #font for the labels
        self.description_font = tkfont.Font(size=10, weight='bold')
        #number of the layer label widget
        self.label = ttk.Label(self, text='Layer number %s :' %(self.layer_index+1), justify='left')
        self.label.grid(row=0, column=0, rowspan=2, padx=1)
        #option menu for the layer type and description 
        self.layertype_label = ttk.Label(self, text='Layer type', font=self.description_font)
        self.layertype_label.grid(row=0, column=1, padx=1)
        self.layertype_widget = ttk.OptionMenu(self,self.layer_type,
                                               self.default_layer_type,*parent.layer_types)
        self.layertype_widget.grid(row=1, column=1, padx=1)
        #add a separator below the widget
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.grid(row=2, column=0,  columnspan=20, sticky="we")
        #add a trace to the layer type
        self.layer_type.trace('w', self.draw_options)
        #initialize options_widget as an empty frame (hidden)
        self.options_widget = tk.Frame()    
             
    #this method will draw the corresponding options for a type of layer, once
    #the layer type is selected.
    def draw_options(self, *args):
        Ltype = self.layer_type.get()
        if Ltype == 'Dense':
            self.options_widget.destroy()
            self.options_widget = DenseLayerWidget(self, self.layer_index)
            self.options_widget.grid(column = 2, row = 0, rowspan = 2)
        elif Ltype == 'Dropout':
            self.options_widget.destroy()
            self.options_widget = DropoutLayerWidget(self, self.layer_index)
            self.options_widget.grid(column = 2, row = 0, rowspan = 2)

    #this method outputs a dictionary of the current information about the layer
    #calls the relevant layer options widget for configuration information        
    def layer_data(self):
        self.layer_dict = self.options_widget.export_options()
        Ltype = self.layer_type.get()
        self.layer_dict['layer_type'] = Ltype
        return self.layer_dict
    
        

#this class will display all the configuration options for the Dense layer type
#and store the user entered values to be used by the keras compiler
class DenseLayerWidget(tk.Frame):
    
    def __init__(self, parent, layer_index):
        tk.Frame.__init__(self, parent)
        self.layer_index = layer_index
        #initialize options_dict empty, to store user input
        self.options_dict = {}
        #Configurable parameteres for dense layers
        self.dense_options = ['units', 'activation', 'use_bias', 'kernel_initilializer',
                         'bias_initializer', 'input_shape']
                
        #Types of available activation functions, etc
        activation_options = ['linear', 'sigmoid', 'tanh', 'softmax', 'relu',
                              'selu', 'elu','none']
        kernel_initilializer_options = ['randomNormal', 'randomUniform', 'zeros', 'ones']
        bias_initilializer_options = ['randomNormal', 'randomUniform', 'zeros', 'ones']
        
        #drawing the necesary widgets to gather user input
        self.units_label = ttk.Label(self, text = 'Units', font = parent.description_font)
        self.units = tk.Spinbox(self, from_ =1, to_ =999, increment=1)
        self.units_label.grid(row=0, column= 0, padx= 5)
        self.units.grid(row=1, column= 0, padx= 5)
        
        self.activation = tk.StringVar()
        self.activation_label = ttk.Label(self, text = 'Activation', font = parent.description_font)
        self.activation_widget = ttk.OptionMenu(self, self.activation, activation_options[0], 
                                                *activation_options)
        self.activation_label.grid(row=0, column= 1, padx= 5)
        self.activation_widget.grid(row=1, column= 1, padx= 5)

        self.use_bias = tk.BooleanVar()
        self.use_bias.set(True)
        self.use_bias_label = ttk.Label(self, text = 'Use Bias', font = parent.description_font)
        self.use_bias_widget = ttk.Checkbutton(self, variable= self.use_bias,
                                                 onvalue= True, offvalue= False) 
        self.use_bias_label.grid(row=0, column= 2, padx= 5)
        self.use_bias_widget.grid(row=1, column= 2, padx= 5)
        
        self.kernel_initializer = tk.StringVar()
        self.kernel_initializer_label = ttk.Label(self, text = 'Kernel Initializer'
                                                  , font = parent.description_font)
        self.kernel_initializer_widget = ttk.OptionMenu(self, self.kernel_initializer, kernel_initilializer_options[0], 
                                                *kernel_initilializer_options)
        self.kernel_initializer_label.grid(row=0, column= 3, padx= 5)
        self.kernel_initializer_widget.grid(row=1, column= 3, padx= 5)
        
        self.bias_initializer = tk.StringVar()
        self.bias_initializer_label = ttk.Label(self, text = 'Bias Initializer'
                                                  , font = parent.description_font)
        self.bias_initializer_widget = ttk.OptionMenu(self, self.bias_initializer, bias_initilializer_options[0], 
                                                *bias_initilializer_options)
        self.bias_initializer_label.grid(row=0, column= 4, padx= 5)
        self.bias_initializer_widget.grid(row=1, column= 4, padx= 5)
        
        # inputshape widget only if the layer is the first layer, the rest of the layers
        #get the inputshape from the previous layer in the model automatically.
        if self.layer_index == 0:
            self.input_shape_label = ttk.Label(self, text = 'Input Shape', font = parent.description_font)
            self.input_shape = tk.Spinbox(self, from_ =1, to_ =9999, increment=1)
            self.input_shape_label.grid(row=0, column= 5, padx= 5)
            self.input_shape.grid(row=1, column= 5, padx= 5)
        
        # export_options generates a dictionary of the current user values in the widget        
    def export_options(self):
        #generating keys for the dictionary, if not the first layer, no input shape required
        if self.layer_index == 0: 
            keys = self.dense_options[:-1]
        else:
            keys = self.dense_options
        
        #generating values
        values = []
        values.append(self.units.get())
        values.append(self.activation.get())
        values.append(self.use_bias.get())
        values.append(self.kernel_initializer.get())
        values.append(self.bias_initializer.get())
        if self.layer_index == 0: 
            values.append(self.input_shape.get())
            
        #generating dictionary
        self.options_dict = dict(zip(keys,values))
        return self.options_dict

     
#Class for the droput layer widget.
            
class DropoutLayerWidget(tk.Frame):
    
    def __init__(self, parent, layer_index):
        tk.Frame.__init__(self, parent)
        self.layer_index = layer_index
        #initialize options_dict empty, to store user input
        self.options_dict = {}
        
        self.rate_label = ttk.Label(self, text = 'Drop rate', font = parent.description_font)
        self.rate = tk.Spinbox(self, from_ =0, to_ =1, increment=0.01)
        self.rate_label.grid(row=0, column= 0, padx= 5)
        self.rate.grid(row=1, column= 0, padx= 5)
    
    # export_options generates a dictionary of the current user values in the widget        
    def export_options(self):
        self.options_dict = {}
        rate = self.rate.get()
        self.options_dict['rate'] = rate
        return self.options_dict
        

        
class Toolbar(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
              
        #make a toolbar button for switching between frames
        for F in ('StartPage', 'PageOne', 'PageTwo', 'Compile'):
            self.new_button(controller,F)
        
    #make a toolbar button for switching between frames
    def new_button(self,controller, page_name):
        self.button = ttk.Button(self, text=page_name,
                           command=lambda: controller.show_frame(page_name))
        self.button.pack(side='left', fill='x', expand=False, ipady=3)


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

#run app if nn_py_main is main.
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()