import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import database



class SampleApp(tk.Tk):
    '''Class to control all windows from entire app'''

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("800x650+351+174")

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
        tk.Label(self, text='Personal Agenda').pack(side='top', fill ='x', pady =10)
        tk.Button(self, text='Contacts',command= lambda : master.switch_frame(Contacts)).pack()
        tk.Button(self, text='Event Planner',command = lambda : master.switch_frame(Planner)).pack()



class Contacts(tk.Frame):
    '''Class to construct the tkinter window to display all the contacts from database'''

    contact_to_be_displayed=None

    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master = master

        # Check if the database exists-if not-create the database and tables
        database.create_check_database()
        self.contacts=database.display_all_contacts()

        tk.Label(self,text='Contacts').pack(side='top', fill='x',pady= 0)
        # Adding labels for conatct updating/adding form
        self.label_contact_first_name = tk.Label(self.master,text='First Name', font=('Helvetica',8)).place(rely=0.2,relx=0.4,anchor='ne')
        self.label_contact_last_name = tk.Label(self.master,text='Last Name', font =('Helvetica', 8)).place(rely=0.25, relx=0.4, anchor='ne')
        self.label_contact_email = tk.Label(self.master, text='Email', font=('Helvetica', 8) ).place(rely=0.3, relx=0.367, anchor='ne')
        self.label_contact_phone = tk.Label(self.master, text='Phone', font=('Helvetica', 8)).place(rely=0.35, relx=0.372, anchor='ne')

        #Adding entries for updating/adding contacts

        self.entry_contact_first_name = tk.Entry(self.master).place(rely=0.2,relx=0.6,relheight=0.028,anchor='ne')
        self.entry_contact_last_name = tk.Entry(self.master).place(rely=0.25, relx=0.6,relheight=0.028, anchor='ne')
        self.entry_contact_email = tk.Entry(self.master).place(rely=0.3, relx=0.6, relheight=0.028, anchor='ne')
        self.entry_contact_phone = tk.Entry(self.master).place(rely=0.35, relx=0.6, relheight=0.028, anchor='ne')


        #Adding buttons to add/updarte /delete a contact and to clear the form

        self.add_button=tk.Button(self.master, text='Add Contact' ,font=('Helvetica', 8), bg='grey', fg='white').place(rely=0.45,relx=0.4,anchor='ne')
        self.update_contact=tk.Button(self.master, text= 'Update Contact', font=('Helvetica', 8),bg= 'grey', fg= 'white').place(rely=0.45, relx=0.52, anchor='ne')
        self.delete_contact = tk.Button(self.master, text='Delete Contact', font=('Helvetica', 8), bg='grey', fg='white').place(rely=0.45, relx=0.64,anchor='ne')
        self.clear_data= tk.Button(self.master, text='Clear', font=('Helvetica', 8),bg='grey', fg='white').place(rely=0.45, relx=0.70, anchor='ne')

        #Adding a tree to display contacts from database
        columns = ('First Name', 'Last Name', 'Email', 'Phone')
        self.contact_display = ttk.Treeview(self.master, show='headings',height='10', columns=columns)
        self.contact_display.place(rely=0.7,relx=0.5,width=500,anchor='center')

        self.contact_display.heading('First Name', text='First Name', anchor='center')
        self.contact_display.column('First Name',width=70)
        self.contact_display.heading('Last Name', text='Last Name', anchor='center')
        self.contact_display.column('Last Name', width=70)
        self.contact_display.heading('Email', text='E-mail', anchor='center')
        self.contact_display.column('Email', width=70)
        self.contact_display.heading('Phone', text='Phone Number', anchor='center')
        self.contact_display.column('Phone', width=70)




































app=SampleApp()
app.mainloop()