#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 22:39:53 2018

@author: Damian Piuselli
"""

from tkinter import *

#ventana vacia
root = Tk()


topframe = Frame(root)
bottomframe = Frame(root)

topframe.pack()
bottomframe.pack(side=BOTTOM)

boton1 = Button(topframe,text='soy un boton, wiiii',fg='blue')
boton2 = Button(topframe,text='soy un boton, wiiii',fg='red')
boton3 = Button(topframe,text='soy un boton, wiiii',fg='white')
boton4 = Button(bottomframe,text='soy un boton, wiiii',fg='black')

boton1.pack(side=LEFT)
boton2.pack(side=LEFT)
boton3.pack(side=LEFT)
boton4.pack(fill=Y)



#mainloop, inicializa la ventana
root.mainloop()



