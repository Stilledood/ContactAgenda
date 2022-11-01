import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo


class SampleApp(tk.Tk):
    '''Class to control all windows from entire app'''

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame=None
        self.switch_frame(StartPage)

    def switch_frame(self,frame_class):
        '''Destroy curent frame and replace the old one with new one'''
        new_frame=frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame=new_frame
        self._frame.pack()




class StartPage(tk.Frame):
    '''Class to construct main window using tkinter'''

    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text='Personal Agenda').pack(side='top', fill ='x', pady =10)
        tk.Button(self,text='Contacts',command= lambda : master.switch_frame(Contacts)).pack()
        tk.Button(self,text='Event Planner',command = lambda : master.switch_frame(Planner)).pack()








app=SampleApp()
app.mainloop()