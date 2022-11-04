import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from tkcalendar import Calendar
import datetime
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

        self.entry_contact_first_name = tk.Entry(self.master)
        self.entry_contact_first_name.place(rely=0.2,relx=0.6,relheight=0.028,anchor='ne')
        self.entry_contact_last_name = tk.Entry(self.master)
        self.entry_contact_last_name.place(rely=0.25, relx=0.6,relheight=0.028, anchor='ne')
        self.entry_contact_email = tk.Entry(self.master)
        self.entry_contact_email.place(rely=0.3, relx=0.6, relheight=0.028, anchor='ne')
        self.entry_contact_phone = tk.Entry(self.master)
        self.entry_contact_phone.place(rely=0.35, relx=0.6, relheight=0.028, anchor='ne')


        #Adding buttons to add/updarte /delete a contact and to clear the form

        self.add_button=tk.Button(self.master, text='Add Contact' ,font=('Helvetica', 8), bg='grey', fg='white',command=self.add_contact).place(rely=0.45,relx=0.4,anchor='ne')
        self.update_contact=tk.Button(self.master, text= 'Update Contact', font=('Helvetica', 8),bg= 'grey', fg= 'white',command=self.update_contact).place(rely=0.45, relx=0.52, anchor='ne')
        self.delete_contact = tk.Button(self.master, text='Delete Contact', font=('Helvetica', 8), bg='grey', fg='white', command=self.delete_contact).place(rely=0.45, relx=0.64,anchor='ne')
        self.clear_data= tk.Button(self.master, text='Clear', font=('Helvetica', 8), bg='grey', fg='white', command=self.clear_form).place(rely=0.45, relx=0.70, anchor='ne')
        self.show_all_contacts = tk.Button(self.master, text='Show All' , font=('Helvetica', 8), bg='grey', fg='white', command=self.display_selected_contacts).place(rely=0.45, relx=0.79, anchor='ne')

        #Adding a tree to display contacts from database
        columns = ('Id','First Name', 'Last Name', 'Email', 'Phone')
        self.contact_display = ttk.Treeview(self.master, show='headings',height=10, columns=columns)
        self.contact_display.place(rely=0.7,relx=0.5,width=540,anchor='center')
        self.contact_display.heading('Id', text= 'Id', anchor='center')
        self.contact_display.column('Id', width=70)
        self.contact_display.heading('First Name', text='First Name', anchor='center')
        self.contact_display.column('First Name',width=70)
        self.contact_display.heading('Last Name', text='Last Name', anchor='center')
        self.contact_display.column('Last Name', width=70)
        self.contact_display.heading('Email', text='E-mail', anchor='center')
        self.contact_display.column('Email', width=70)
        self.contact_display.heading('Phone', text='Phone Number', anchor='center')
        self.contact_display.column('Phone', width=70)
        self.contact_display.bind(self.display_selected_contacts())
        self.contact_display.bind("<<TreeviewSelect>>",self.show_selected_contact)

        #Adding scrollbar
        self.scrool_bar = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command= self.contact_display.yview)
        self.scrool_bar.place(x=660, y= 400 ,width=20)
        self.contact_display.configure(xscrollcommand=self.scrool_bar.set)


        #Adding A search bar and button-to search contacts by last name

        self.search_button = tk.Button(self.master, text='Search By Last Name', font=('Helvetica', 8), bg='grey', fg='white' ,command=self.display_searched_contacts).place(rely=0.9,relx=0.45,anchor='ne')
        self.search_bar= tk.Entry(self.master)
        self.search_bar.place(rely=0.9 , relx=0.75, relheight=0.035, relwidth=0.25, anchor='ne')



    def display_selected_contacts(self):

        contacts = database.display_all_contacts()
        for contact in contacts:
            self.contact_display.insert('', 'end',values = (contact[0], contact[1], contact[2], contact[3], contact[4]))

    def display_searched_contacts(self):
        contact_last_name = self.search_bar.get()
        records=database.search_contact(contact_last_name)
        if records:
            self.contact_display.delete(*self.contact_display.get_children())
            for contact in records:
                self.contact_display.insert('','end', values=(contact[0], contact[1], contact[2], contact[3], contact[4]))
        else:
            pass

    def add_contact(self):

        contact_first_name = self.entry_contact_first_name.get()
        contact_last_name = self.entry_contact_last_name.get()
        contact_email = self.entry_contact_email.get()
        contact_phone = self.entry_contact_phone.get()
        database.add_contact(first_name=contact_first_name, last_name=contact_last_name, email=contact_email, phone=contact_phone)
        self.contact_display.delete(*self.contact_display.get_children())
        new_records = database.display_all_contacts()
        for record in new_records:
            self.contact_display.insert('','end',values=(record[0], record[1], record[2], record[3], record[4]))

    def clear_form(self):
        '''Method to delete all ther data present in the form'''

        self.entry_contact_first_name.delete(0,tk.END)
        self.entry_contact_last_name.delete(0,tk.END)
        self.entry_contact_email.delete(0,tk.END)
        self.entry_contact_phone.delete(0,tk.END)

    def show_selected_contact(self,event):
        '''Method to display contact details in form'''

        self.clear_form()
        for selection in self.contact_display.selection():
            item = self.contact_display.item(selection)
            global id_num
            id_num, first_name, last_name, email, phone = item['values'][:5]
            self.entry_contact_first_name.insert(0,first_name)
            self.entry_contact_last_name.insert(0,last_name)
            self.entry_contact_email.insert(0, email)
            self.entry_contact_phone.insert(0 ,phone)

    def update_contact(self):
        '''Method to update selected contact'''

        contact_id=id_num
        contact_first_name = self.entry_contact_first_name.get()
        contact_last_name = self.entry_contact_last_name.get()
        contact_email = self.entry_contact_email.get()
        contact_phone = self.entry_contact_phone.get()
        confirm_box = mb.askquestion('Update Contact','Are you sure you want to update the selected contact?')
        if contact_first_name:
            if confirm_box == 'yes':
                database.update_contact(contact_id, contact_first_name, contact_last_name, contact_email, contact_phone)
            else:
                return
        contacts=database.display_all_contacts()
        self.contact_display.delete(*self.contact_display.get_children())
        for contact in contacts:
            self.contact_display.insert('', 'end' ,values=(contact[0], contact[1], contact[2], contact[3], contact[4]))

    def delete_contact(self):
        '''Method to delete selected contact'''

        contact_id = id_num
        confirm_box = mb.askquestion('Delete Contact','Are you sure you want to delete this contact?')
        if confirm_box == 'yes':
            database.delete_contact(contact_id)
        else:
            return
        #Re-Populating the table wit all contacts from contacts table
        self.contact_display.delete(*self.contact_display.get_children())
        contacts = database.display_all_contacts()

        for contact in contacts :
            self.contact_display.insert('', 'end', values=(contact[0], contact[1], contact[2], contact[3], contact[4]))




class Planner(tk.Frame):
    '''Class to construct the window to display all planned events stored in the database'''

    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master=master
        self.name = tk.Label(text='Tasks' ,font=('Helvetica' ,12)).pack(side='top',padx=0, fill='x' )
        today = datetime.date.today()
        self.calendar=Calendar(self.master, selectmode='day', year=today.year, month=today.month, day=today.day, font=('Helvetica', 10), headersbackground ='light grey', headersforeground='black')
        self.calendar.place(rely=0.1, relx=0.67, anchor='ne')
        # Adding buttons to display selected tasks based on day,month,year
        self.daily_task_button = tk.Button(self.master, text='Today Tasks', font=('Helvetica', 8), bg='grey', fg='white')
        self.daily_task_button.place(rely=0.45, relx=0.32, anchor='ne')
        self.weekly_task_button = tk.Button(self.master, text='Weekly Tasks', font=('Helvetica', 8), bg='grey', fg='white')
        self.weekly_task_button.place(rely=0.45, relx=0.44, anchor='ne')
        self.monthly_task_button = tk.Button(self.master, text='Monthly Tasks', font=('Helvetica', 8), bg='grey', fg='white')
        self.monthly_task_button.place(rely=0.45, relx=0.56, anchor='ne')
        self.day_search_button = tk.Button(self.master, text='Day Search', font=('Helvetica', 8), bg='grey', fg='white')
        self.day_search_button.place(rely=0.45, relx=0.67, anchor='ne' )
        self.month_search_button = tk.Button(self.master, text='Month Search', font=('Helvetica', 8), bg='grey', fg='white')
        self.month_search_button.place(rely=0.45, relx=0.79, anchor='ne')






















































app=SampleApp()
app.mainloop()