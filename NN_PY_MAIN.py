#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 22:39:53 2018

@author: Damian Piuselli
"""

import tkinter as tk                
from tkinter import font  as tkfont 


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=11, slant="italic")
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
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, Compile):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
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
        self.title.grid(row=0, rowspan=1)
        #first widget gets the number of layers of the NN.
        #apply button, call the draw_layers method
        self.label = tk.Label(self, text='Number of Layers :')
        self.layers = tk.Spinbox(self, from_ =1, to_ =20, increment=1)
        self.layers_apply = tk.Button(self, text='Apply', command=self.draw_layers)
        self.label.grid(row=1, column=0, padx=5)
        self.layers.grid(row=1, column=1, padx=5)
        self.layers_apply.grid(row=1, column=2)
        #list of widgets initialized empty
        self.layers_widgets = []
        self.layers_widgets_values = []
                
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
            widget[0].destroy()
            widget[1].destroy()
        for values in self.layers_widgets_values:
            values.set('')
        
        #deleting all references
        self.layers_widgets = []
        self.layers_widgets_values = []
        
        #creating the appropiate number of widgets and storing a reference
        #in layers_widgets list
        option_list = ('opcion1','opcion2')
        for i in range(int(self.layers.get())):
            selected_option = tk.StringVar()
            selected_option.set(option_list[0])
            n_layer = tk.Label(self, text='Layer number %s :' %(i+1))
            layer_widget = tk.OptionMenu(self,selected_option,*option_list)
            n_layer.grid(row=int(i)+2, column=0, padx=1)
            layer_widget.grid(row=int(i)+2, column=1, padx=1)
            self.layers_widgets.append([n_layer,layer_widget])
            self.layers_widgets_values.append(selected_option)
        
        
        


class Toolbar(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
              
        #make a toolbar button for switching between frames
        for F in ('StartPage', 'PageOne', 'PageTwo', 'Compile'):
            self.new_button(controller,F)
        
    #make a toolbar button for switching between frames
    def new_button(self,controller, page_name):
        button = tk.Button(self, text=page_name,
                           command=lambda: controller.show_frame(page_name))
        button.pack(side='left', fill='x', expand=False, ipady=3)


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