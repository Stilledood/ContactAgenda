import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from tkcalendar import Calendar
import datetime
import database
import customtkinter
import sv_ttk
from customtkinter import CTk



customtkinter.set_appearance_mode("System")



class SampleApp(tk.Tk):
    '''Class to control all windows from entire app'''

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("800x650")
        self._frame=None
        self.switch_frame(StartPage)
        print(self._frame)


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
        self.master=master
        self.configure(bg='white')





        customtkinter.CTkLabel(self, text='Personal Agenda & Planner').place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.contacts_button = customtkinter.CTkButton(self,width=129, height=32, border_width=0.5, corner_radius=10, text='Contacts', text_font=('Helvetica', 10), text_color='grey18',  command= lambda : self.master.switch_frame(Contacts) )

        self.contacts_button.pack(padx=0.5, pady=30)
        self.planner_button = customtkinter.CTkButton(self, width=129, height=32, border_width=0.5, corner_radius=10, text='Tasks', text_font=('Helvetica', 10),text_color='grey18', command=lambda: self.master.switch_frame(Planner))
        self.planner_button.pack(padx=0.5, pady=50)





class Contacts(tk.Frame):
    '''Class to construct the tkinter window to display all the contacts from database'''

    contact_to_be_displayed=None

    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master = master

        # Check if the database exists-if not-create the database and tables
        database.create_check_database()
        self.contacts=database.display_all_contacts()


        # Adding labels for conatct updating/adding form
        self.label_contact_first_name = tk.Label(self.master,text='First Name', font=('Helvetica',8)).place(rely=0.2,relx=0.4,anchor='ne')
        self.label_contact_last_name = tk.Label(self.master,text='Last Name', font =('Helvetica', 8)).place(rely=0.25, relx=0.4, anchor='ne')
        self.label_contact_email = tk.Label(self.master, text='Email', font=('Helvetica', 8) ).place(rely=0.3, relx=0.367, anchor='ne')
        self.label_contact_phone = tk.Label(self.master, text='Phone', font=('Helvetica', 8)).place(rely=0.35, relx=0.372, anchor='ne')

        #Adding entries for updating/adding contacts

        self.entry_contact_first_name = customtkinter.CTkEntry(self.master)
        self.entry_contact_first_name.place(rely=0.2,relx=0.6,relheight=0.028,anchor='ne')
        self.entry_contact_last_name = customtkinter.CTkEntry(self.master)
        self.entry_contact_last_name.place(rely=0.25, relx=0.6,relheight=0.028, anchor='ne')
        self.entry_contact_email = customtkinter.CTkEntry(self.master)
        self.entry_contact_email.place(rely=0.3, relx=0.6, relheight=0.028, anchor='ne')
        self.entry_contact_phone = customtkinter.CTkEntry(self.master)
        self.entry_contact_phone.place(rely=0.35, relx=0.6, relheight=0.028, anchor='ne')


        #Adding buttons to add/updarte /delete a contact and to clear the form

        self.add_button=customtkinter.CTkButton(self.master, text='Add Contact' ,text_font=('Helvetica', 8),width=30, corner_radius=10,text_color='white', command=self.add_contact).place(rely=0.45,relx=0.3,anchor='ne')

        self.update_contact=customtkinter.CTkButton(self.master, text= 'Update Contact', text_font=('Helvetica', 8),width=30,corner_radius=10, text_color='white', command=self.update_contact).place(rely=0.45, relx=0.45, anchor='ne')
        self.delete_contact = customtkinter.CTkButton(self.master, text='Delete Contact', text_font=('Helvetica', 8), width=30,corner_radius=10, text_color='white', command=self.delete_contact).place(rely=0.45, relx=0.595,anchor='ne')
        self.clear_data= customtkinter.CTkButton(self.master, text='Clear', text_font=('Helvetica', 8), width=30,corner_radius=10,text_color='white', command=self.clear_form).place(rely=0.45, relx=0.68, anchor='ne')
        self.show_all_contacts = customtkinter.CTkButton(self.master, text='Show All' , text_font=('Helvetica', 8), width=30 ,corner_radius=10, text_color='white',  command=self.display_selected_contacts).place(rely=0.45, relx=0.79, anchor='ne')

        #Adding a tree to display contacts from database
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=10,
                        font=('Helvetica', 8), relief='flat', borderwidth=0.5)  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Helvetica', 9, 'bold'), background='blue58')  # Modify the font of the headings

        columns = ('Id','First Name', 'Last Name', 'Email', 'Phone')
        self.contact_display = ttk.Treeview(self.master, show='headings',height=10, columns=columns, style='mystyle.Treeview')
        self.contact_display.place(rely=0.7,relx=0.5,width=540,anchor='center')
        self.contact_display.heading('Id', text= 'Id', anchor='center')
        self.contact_display.column('Id', width=70, anchor='center')
        self.contact_display.heading('First Name', text='First Name', anchor='center')
        self.contact_display.column('First Name',width=70, anchor='center')
        self.contact_display.heading('Last Name', text='Last Name', anchor='center')
        self.contact_display.column('Last Name', width=70, anchor='center')
        self.contact_display.heading('Email', text='E-mail', anchor='center')
        self.contact_display.column('Email', width=70, anchor='center')
        self.contact_display.heading('Phone', text='Phone Number', anchor='center')
        self.contact_display.column('Phone', width=70, anchor='center')
        self.contact_display.bind(self.display_selected_contacts())
        self.contact_display.bind("<<TreeviewSelect>>",self.show_selected_contact)


        #Adding scrollbar
        self.scrool_bar = customtkinter.CTkScrollbar(self.master,border_spacing=3,height=225, width=10, scrollbar_hover_color='blue', command= self.contact_display.yview)
        self.scrool_bar.place(x=662, y= 342 ,width=15)
        self.contact_display.configure(yscrollcommand=self.scrool_bar.set)


        #Adding A search bar and button-to search contacts by last name

        self.search_button = customtkinter.CTkButton(self.master, text='Search By Last Name', text_font=('Helvetica', 8), width=39, corner_radius=10, text_color='white', command=self.display_searched_contacts).place(rely=0.9,relx=0.45,anchor='ne')
        self.search_bar= customtkinter.CTkEntry(self.master)
        self.search_bar.place(rely=0.9 , relx=0.77, relheight=0.045, relwidth=0.3, anchor='ne')

        #Adding Tab view to change between contacts window and tasks window
        self.contacts_button = customtkinter.CTkButton(self.master, text='Contacts', text_color='white', text_font=('Helvetica', 8), corner_radius=10, width=30, state='disabled')
        self.contacts_button.place(relx=0.5, rely=0.05, anchor='ne', relwidth=0.15)
        self.task_button = customtkinter.CTkButton(self.master, text='Tasks', text_font=('Helvetica', 8), text_color='white', corner_radius=10, width=30, command= self.switch_to_tasks)
        self.task_button.place(relx=0.51, rely=0.05, relwidth=0.15)





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

    def switch_to_tasks(self):
        self.master.destroy()
        app=SampleApp()
        app.switch_frame(Planner)
        app.mainloop()





class Planner(tk.Frame):
    '''Class to construct the window to display all planned events stored in the database'''

    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master=master
        tasks = database.fetch_all_events()

        today = datetime.date.today()
        self.calendar=Calendar(self.master, selectmode='day', year=today.year, month=today.month, day=today.day, font=('Helvetica', 10), headersbackground ='#3090C7', headersforeground='white',bordercolor='white', weekendbackground='light blue',background='#1589FF',borderwidthint=0, cursor='hand1' )
        self.calendar.place(rely=0.1, relx=0.68, anchor='ne',relwidth=0.6, relheight=0.3)
        # Adding buttons to display selected tasks based on day,month,year
        self.daily_task_button = customtkinter.CTkButton(self.master, text= 'Daily Tasks', text_font=('Helvetica', 8),width=50,corner_radius=10, text_color='white')
        self.daily_task_button.place(rely=0.1, relx=0.915, anchor='ne', relwidth=0.15)
        self.weekly_task_button = customtkinter.CTkButton(self.master, text= 'Weekly Tasks', text_font=('Helvetica', 8),width=30,corner_radius=10, text_color='white')
        self.weekly_task_button.place(rely=0.165, relx=0.915, anchor='ne', relwidth=0.15)
        self.monthly_task_button = customtkinter.CTkButton(self.master, text= 'Monthly Tasks', text_font=('Helvetica', 8),width=30,corner_radius=10, text_color='white')
        self.monthly_task_button.place(rely=0.23, relx=0.915, anchor='ne', relwidth=0.15)
        self.day_search_button = customtkinter.CTkButton(self.master, text= 'Day Search', text_font=('Helvetica', 8),width=30,corner_radius=10, text_color='white')
        self.day_search_button.place(rely=0.295, relx=0.915, anchor='ne', relwidth=0.15 )
        self.month_search_button = customtkinter.CTkButton(self.master, text= 'Month Search', text_font=('Helvetica', 8),width=30,corner_radius=10, text_color='white')
        self.month_search_button.place(rely=0.36, relx=0.915, anchor='ne', relwidth=0.15)

        #Adding a Tree view to display tasks from events table
        columns=('Id', 'Task', 'Description', 'Date Added', 'Due Date')
        self.tasks_view = ttk.Treeview(self.master, show='headings',height=10, columns=columns)
        self.tasks_view.place(rely=0.635, relx=0.85, anchor='ne', width=540)
        self.tasks_view.heading('Id', text= 'Id', anchor='center')
        self.tasks_view.column('Id', width=70, anchor='center')
        self.tasks_view.heading('Task', text='Task', anchor='center')
        self.tasks_view.column('Task', width=70, anchor='center')
        self.tasks_view.heading('Description', text='Description', anchor='center')
        self.tasks_view.column('Description', width=70,anchor='center')
        self.tasks_view.heading('Date Added', text='Date Added', anchor='center')
        self.tasks_view.column('Date Added', width=70, anchor='center')
        self.tasks_view.heading('Due Date', text='Due Date', anchor='center')
        self.tasks_view.column('Due Date', width=70, anchor='center')
        self.tasks_view.bind(self.display_all_tasks())
        self.tasks_view.bind("<<TreeviewSelect>>", self.show_selected_tasks)

        #Adding labels to display selected task
        self.label_task_name = tk.Label(self.master, text='Task', font=('Helvetica', 8))
        self.label_task_name.place(relx=0.15, rely=0.42, anchor='ne')
        self.label_task_description = tk.Label(self.master, text='Description', font=('Helvetica', 8))
        self.label_task_description.place(relx=0.15, rely=0.46, anchor='ne')
        self.label_task_due_date = tk.Label(self.master, text='Due Date', font=('Helvetica', 8))
        self.label_task_due_date.place(relx=0.15, rely=0.5, anchor='ne')

        # Adding Entries to display selected tasks from list
        self.entry_task_title = customtkinter.CTkEntry(self.master)
        self.entry_task_title.place(rely=0.42, relx=0.375, relheight=0.028, anchor='ne', width=150)
        self.entry_tast_description = customtkinter.CTkEntry(self.master)
        self.entry_tast_description.place(rely=0.46, relx=0.375, relheight=0.028, anchor='ne', width=150)
        self.entry_task_due_date = customtkinter.CTkEntry(self.master)
        self.entry_task_due_date.place(rely=0.50, relx=0.375, relheight=0.028, anchor='ne', width=150)

        # Adding Buttons to add/update/delete/clear form a task
        self.add_task_button = customtkinter.CTkButton(self.master, text= 'Add Task', text_font=('Helvetica', 8),width=40,corner_radius=10, text_color='white')
        self.add_task_button.place(rely=0.465, relx=0.55, anchor='ne',relwidth=0.10)
        self.update_task_button =customtkinter.CTkButton(self.master, text= 'Change Task', text_font=('Helvetica', 8),width=30,corner_radius=10, text_color='white')
        self.update_task_button.place(rely=0.465, relx=0.67, anchor='ne', relwidth=0.10)
        self.delete_task_button = customtkinter.CTkButton(self.master, text= 'Delete Task', text_font=('Helvetica', 8),width=30,corner_radius=10, text_color='white')
        self.delete_task_button.place(rely=0.465, relx=0.79, anchor='ne',relwidth=0.10)
        self.clear_form_button= customtkinter.CTkButton(self.master, text='Clear',text_font=('Helvetica', 8), width=30, corner_radius=10, text_color='white')
        self.clear_form_button.place(rely=0.465, relx=0.91, anchor='ne', relwidth=0.10)

        #Adding button to search for a specific tast based on title
        self.search_task_button = customtkinter.CTkButton(self.master, text='Search Task By Title', text_font=('Helvetica', 8), width=30, corner_radius=10, text_color='white')
        self.search_task_button.place(rely=0.9, relx=0.45, anchor='ne')
        self.search_entry =customtkinter.CTkEntry(self.master)
        self.search_entry.place(rely=0.9, relx=0.73, anchor='ne',relwidth=0.25)

        #Adding separators
        self.separator = customtkinter.CTkProgressBar(self.master, corner_radius=5, width=5,height=200,orient='vertical')
        self.separator.set(100,100)
        self.separator.place(rely=0.1, relx=0.725, anchor='ne')

        self.second_separator = customtkinter.CTkProgressBar(self.master, corner_radius=5, width=5, height =80, orient='vertical')
        self.second_separator.set(100,100)
        self.second_separator.place(rely=0.42, relx=0.43, anchor='ne')

        # Adding Tab view to change between contacts window and tasks window
        self.contacts_button = customtkinter.CTkButton(self.master, text='Contacts', text_color='white',
                                                       text_font=('Helvetica', 8), corner_radius=10, width=30,command=self.switch_to_contacts )
        self.contacts_button.place(relx=0.5, rely=0.02, anchor='ne', relwidth=0.15)
        self.task_button = customtkinter.CTkButton(self.master, text='Tasks', text_font=('Helvetica', 8),
                                                   text_color='white', corner_radius=10, width=30,state='disabled')
        self.task_button.place(relx=0.51, rely=0.02, relwidth=0.15)












    def display_all_tasks(self):
        '''Method to populate Treeview with tasks from MySQL events table'''

        tasks = database.fetch_all_events()
        if tasks:
            for task in tasks:
                print(task[3].date())
                self.tasks_view.insert('', 'end', values=(task[0], task[1], task[2], task[3].date(), task[4].date()))


    def clear_form(self):
        '''Method to clear all form fileds'''

        self.entry_task_title.delete(0, tk.END)
        self.entry_tast_description.delete(0, tk.END)
        self.entry_task_due_date.delete(0, tk.END)



    def show_selected_tasks(self,event):
        '''Method to display in form selected task from the table'''

        self.clear_form()
        for selection in self.tasks_view.selection():
            item= self.tasks_view.item(selection)
            global task_id_num
            task_id_num, task, description,_, due_date = item['values'][:5]
            self.entry_task_title.insert(0, task)
            self.entry_tast_description.insert(0, description)
            self.entry_task_due_date.insert(0, due_date)

    def switch_to_contacts(self):
        self.master.destroy()
        app=SampleApp()
        app.switch_frame(Contacts)
        app.mainloop()



































































app=SampleApp()
sv_ttk.set_theme('light')
app.mainloop()