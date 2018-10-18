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
        self.container.pack(side="top", fill="both", expand=True, anchor='nw' )
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
        self.title = tk.Label(self, text="Compile Model",bd=5, font=controller.title_font)
        self.title.grid(row=0, columnspan=1)
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.grid(row=1, column=0,  columnspan=20, sticky="we")
        #first widget gets the number of layers of the NN.
        #apply button, call the draw_layers method
        self.label = ttk.Label(self, text='Number of Layers :')
        self.layers = tk.Spinbox(self, from_ =1, to_ =20, increment=1)
        self.layers_apply = ttk.Button(self, text='Apply', command=self.draw_layers)
        self.label.grid(row=2, column=0)
        self.layers.grid(row=2, column=1)
        self.layers_apply.grid(row=2, column=2)
        self.separator2 = ttk.Separator(self, orient="horizontal")
        self.separator2.grid(row=3, column=0,  columnspan=20, sticky="we")
        #list of widgets initialized empty
        self.layer_types = ('opcion1','opcion2')
        self.layers_widgets = []
                
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
            
        #deleting all references
        self.layers_widgets = []
        
        #creating the appropiate number of widgets and storing a reference
        #in layers_widgets list
        
        for i in range(int(self.layers.get())):
            layer_widget = LayerWidget(self,i)
            layer_widget.grid(row=i+4, columnspan=5, sticky='w')
            self.layers_widgets.append(layer_widget)
            
            
        
#custom widget for layers, to be drawn in the compile frame.        
class LayerWidget(tk.Frame):
    
    def __init__(self, parent, layer_index):
        tk.Frame.__init__(self, parent)
        self.layer_index = layer_index
        self.layer_type = tk.StringVar()
        self.default_layer_type = parent.layer_types[0]
        self.description_font = tkfont.Font(size=10, weight='bold')
        #number of the layer
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
        self.layer_type.trace('w',self.draw_options)
    #this method will draw the corresponding options for a type of layer, once
    #the layer type is selected.
    def draw_options(self, *args):
        self.layertype_label1 = ttk.Label(self, text='Layer type')
        self.layertype_label1.grid(row=0, column=2, padx=1)

        
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