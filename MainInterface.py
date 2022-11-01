import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import database


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



class Contacts(tk.Frame):
    '''Class to construct the tkinter window to display all the contacts from database'''

    def __init__(self,master):
        tk.Frame.__init__(self,master)
        database.create_check_database()
        self.contacts=database.display_all_contacts()
        tk.Label(self,text='Contacts').pack(side='top', fill='x',pady= 0)
        self.tree=ttk.Treeview(columns=('First Name', 'Last Name', 'Email', 'Phone' ), show='headings')
        self.tree.heading('First Name',text='First Name')
        self.tree.heading('Last Name', text='Last Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Phone', text='Phone')

        try:
            for contact in self.contacts:
                self.tree.insert("",'end',values=(contact[1],contact[2],contact[3],contact[4]))
        except:
            pass

        self.tree.pack()













app=SampleApp()
app.mainloop()