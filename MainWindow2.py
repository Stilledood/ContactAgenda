import tkinter as tk
import customtkinter
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk
import database
from tkinter import messagebox as mb
from tkcalendar import Calendar
from dateutil import parser

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme("green")
PATH='Images'

class Contacts(customtkinter.CTkFrame):
    '''Class to construct the contacts part of the window'''

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

        #Construct the form to display selected contact
        self.first_name_entry =customtkinter.CTkEntry(self, placeholder_text='First Name', width=300, height=35, corner_radius=10)
        self.first_name_entry.place(relx=0.5, rely=0.1, anchor='ne')
        self.last_name_entry =customtkinter.CTkEntry(self, placeholder_text='Last Name', width=300, height=35, corner_radius=10)
        self.last_name_entry.place(relx=0.5, rely=0.17, anchor='ne')
        self.email_entry = customtkinter.CTkEntry(self, placeholder_text='E-mail', width=300, height=35, corner_radius=10)
        self.email_entry.place(relx=0.5, rely=0.24, anchor='ne')
        self.phone_entry = customtkinter.CTkEntry(self,placeholder_text='Phone Number', width=300, height=35, corner_radius=10)
        self.phone_entry.place(relx=0.5, rely=0.31, anchor='ne')

        #Adding Search Function
        self.search= customtkinter.CTkButton(self,text='Search By Last Name',corner_radius=10,border_color='#0E86D4',bg_color='gray19', fg_color='#0E86D4',command=self.display_searched_contacts)
        self.search.place(relx=0.4, rely=0.922, anchor='ne')
        self.search_entry = customtkinter.CTkEntry(self, width=250, height=35, corner_radius=10)
        self.search_entry.place(relx=0.775, rely=0.92 , anchor='ne')

        #Adding Utility buttons
        self.clear_form_button = customtkinter.CTkButton(self, text='Clear Form', corner_radius=10,border_color='#0E86D4', bg_color='gray19', fg_color='#0E86D4', command=self.clear_form)
        self.clear_form_button.place(relx=0.85, rely=0.1, anchor='ne', relwidth=0.2)
        self.add_contact_button = customtkinter.CTkButton(self, text='Add Contact', corner_radius=10, border_color='#0E86D4', bg_color='gray19', fg_color='#0E86D4', command=self.add_contact)
        self.add_contact_button.place(relx=0.85, rely=0.17, anchor='ne',relwidth=0.2)
        self.update_contact_button = customtkinter.CTkButton(self, text='Update Contact', corner_radius=10, border_color='#0E86D4', bg_color='gray19', fg_color='#0E86D4',command=self.update_contact)
        self.update_contact_button.place(relx=0.85, rely=0.24, anchor='ne', relwidth=0.2)
        self.delete_contact_button = customtkinter.CTkButton(self, text='Delete Contact', corner_radius=10, border_color='#0E86D4', bg_color='gray19', fg_color='#0E86D4', command= self.delete_contact)
        self.delete_contact_button.place(relx=0.85, rely=0.31, anchor='ne', relwidth=0.2)

        #Adding tree view to display contacts from contacts table from database
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", highlightthickness=1, bd=1,
                        font=('Helvetica', 8), borderwidth=0, background ='gray19', foreground='#B1B1B1',fieldbackground='gray19')  # Modify the font of the body
        style.configure("Treeview.Heading", font=('Helvetica', 9, 'bold'),
                        background='gray29')  # Modify the font of the headings
        style.map('Treeview',background=[('selected','green')])
        columns = ('Id', 'First Name', 'Last Name', 'Email', 'Phone')
        self.contact_display = ttk.Treeview(self.master, show='headings', height=10, columns=columns,
                                            )
        self.contact_display.place(rely=0.7, relx=0.5, width=540, anchor='center')
        self.contact_display.heading('Id', text='Id', anchor='center')
        self.contact_display.column('Id', width=70, anchor='center')
        self.contact_display.heading('First Name', text='First Name', anchor='center')
        self.contact_display.column('First Name', width=70, anchor='center')
        self.contact_display.heading('Last Name', text='Last Name', anchor='center')
        self.contact_display.column('Last Name', width=70, anchor='center')
        self.contact_display.heading('Email', text='E-mail', anchor='center')
        self.contact_display.column('Email', width=70, anchor='center')
        self.contact_display.heading('Phone', text='Phone Number', anchor='center')
        self.contact_display.column('Phone', width=70, anchor='center')
        self.contact_display.place(relx=0.6,rely=0.5, anchor='ne', relwidth=0.1)
        self.contact_display.bind(self.display_all_contacts())
        self.contact_display.bind("<<TreeviewSelect>>",self.show_selected_contact)

        # Adding button to display all contacts
        self.show_all_button = customtkinter.CTkButton(self, text='Display All Contacts', corner_radius=10, border_color='#0E86D4', bg_color='gray19', fg_color='#0E86D4', command=self.display_all_contacts)
        self.show_all_button.place(relx=0.6, rely=0.45, anchor='ne', relwidth=0.2)


    def clear_form(self):
        '''Method to clear all form fields'''

        self.first_name_entry.delete(0,100)
        self.last_name_entry.delete(0,100)
        self.email_entry.delete(0,100)
        self.phone_entry.delete(0,100)
        self.first_name_entry.configure(placeholder_text='First Name')
        self.last_name_entry.configure(placeholder_text='Last Name')
        self.email_entry.configure(placeholder_text='E-mail')
        self.phone_entry.configure(placeholder_text='Phone')

    def display_all_contacts(self):
        '''Method to extract all conatcts from databse and populate the view'''
        contacts = database.display_all_contacts()

        for contact in contacts:
            self.contact_display.insert('', 'end',values = (contact[0], contact[1], contact[2], contact[3], contact[4]))


    def show_selected_contact(self,event):
        '''Method to display contact details in form'''
        for selection in self.contact_display.selection():
            item = self.contact_display.item(selection)
            global id_num
            id_num, first_name, last_name, email, phone = item['values'][:5]
            self.first_name_entry.configure(placeholder_text = first_name)
            self.last_name_entry.configure(placeholder_text = last_name)
            self.email_entry.configure(placeholder_text = email)
            self.phone_entry.configure(placeholder_text = phone)


    def display_searched_contacts(self):
        '''Method to display search results'''

        contact_name =self.search_entry.get()
        records = database.search_contact(contact_name)
        if records:
            self.contact_display.delete(*self.contact_display.get_children())
            for contact in records:
                self.contact_display.insert('','end', values=(contact[0], contact[1], contact[2],contact[3], contact[4]))
        else:
            return


    def add_contact(self):
        '''Method to add a contact base on data inserted in form'''

        contact_first_name = self.first_name_entry.get()
        contact_last_name = self.last_name_entry.get()
        contact_email = self.email_entry.get()
        contact_phone =self.phone_entry.get()

        if contact_first_name == 'First Name':
            mb.askquestion('Add Contact','Are you sure you want your contact first name to be First Name')
            if mb == 'yes':
                contact_first_name ='First Name'
        if contact_last_name == 'Last Name':
            mb.askquestion('Add Contact','Are you sure you want your contact last name to be Last Name')
            if mb == 'yes':
                contact_last_name ='Last Name'
        if not contact_phone.isdigit():
            mb.showerror(title='Add Contact', message='Phone number should contain only digits')
            return
        database.add_contact(contact_first_name,contact_last_name,contact_email,contact_phone)

        self.clear_form()
        self.display_all_contacts()


    def update_contact(self):
        '''Method to update contact'''

        contact_id=id_num
        contact_first_name = self.first_name_entry.get()
        if not contact_first_name:
            contact_first_name = self.first_name_entry.placeholder_text
        contact_last_name = self.last_name_entry.get()
        if not contact_last_name:
            contact_last_name = self.last_name_entry.placeholder_text
        contact_email = self.email_entry.get()
        if not contact_email:
            contact_email = self.email_entry.placeholder_text
        contact_phone = self.phone_entry.get()
        if not  contact_phone:
            contact_phone = self.phone_entry.placeholder_text
        print(contact_id,contact_first_name,contact_last_name,contact_email,contact_phone)


        confirm_box = mb.askquestion('Update Contact',f"Are you Sure you want to update: {contact_first_name} {contact_last_name} contact ?")
        if confirm_box == 'yes':
            database.update_contact(contact_id, contact_first_name, contact_last_name, contact_email, contact_phone)
        self.clear_form()
        mb.showinfo('Update Contact','Contact succesfully updated')
        self.contact_display.delete(*self.contact_display.get_children())
        records = database.display_all_contacts()
        for contact in records:
            self.contact_display.insert('','end', values=(contact[0], contact[1], contact[2], contact[3], contact[4]))

    def delete_contact(self):

        contact_id = id_num
        contact_first_name = self.first_name_entry.get()
        if not contact_first_name:
            contact_first_name = self.first_name_entry.placeholder_text
        contact_last_name = self.last_name_entry.get()
        if not contact_last_name:
            contact_last_name = self.last_name_entry.placeholder_text
        confirm_box = mb.askquestion('Delete Contact',f"Are you sure you want to delete {contact_first_name} {contact_last_name} ?")
        if confirm_box == 'yes':
            database.delete_contact(contact_id)
            self.clear_form()
            records = database.display_all_contacts()
            self.contact_display.delete(*self.contact_display.get_children())
            for contact in records:
                self.contact_display.insert('', 'end',
                                            values=(contact[0], contact[1], contact[2], contact[3], contact[4]))
        else:
            return






class Tasks(customtkinter.CTkFrame):
    '''Class to construct a frame for tasks window'''

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", highlightthickness=1, bd=1,
                        font=('Helvetica', 8), borderwidth=0, background='gray19', foreground='#B1B1B1',
                        fieldbackground='gray19')  # Modify the font of the body
        style.configure("Treeview.Heading", font=('Helvetica', 9, 'bold'),
                        background='gray29')  # Modify the font of the headings
        style.map('Treeview', background=[('selected', 'green')])
        columns = ('Id', 'Title','Short Description','Due Date')

        self.task_view = ttk.Treeview(self,show='headings', columns=columns, height=7)
        self.task_view.place(relx=0.95, rely=0.55, anchor='ne', relwidth=0.9)
        self.task_view.heading('Id',text='Id', anchor='center')
        self.task_view.column('Id', width=30 ,anchor='center', stretch='False')
        self.task_view.heading('Title', text='Title', anchor='center')
        self.task_view.column('Title', width=90, anchor='center', stretch='False')
        self.task_view.heading('Short Description', text='Description',anchor='center')
        self.task_view.column('Short Description',width=90,anchor='ne')
        self.task_view.heading('Due Date', text='Due Date', anchor='center')
        self.task_view.column('Due Date', width=90, anchor='ne')
        self.task_view.bind(self.display_all_tasks())
        self.task_view.bind("<<TreeviewSelect>>", self.display_selected_task)

        #Adding text area to display selected task details

        self.task_text_area = customtkinter.CTkTextbox(self,width=250, height=100, corner_radius=10,text_color='gray39')
        self.task_text_area.place(relx=0.85, rely=0.84, anchor='ne')
        self.task_title_entry = customtkinter.CTkEntry(self, placeholder_text='Task Title', width=200, height=35, corner_radius=10)
        self.task_title_entry.place(relx=0.775, rely=0.785, anchor='ne')

        #Adding calendar widget

        self.calendar = Calendar(self)
        self.calendar.place(relx=0.65, rely=0.03, anchor='ne',relwidth=0.6)

        #Adding Meniu button to select tasks(day , week , month)
        self.today_tasks_button = customtkinter.CTkButton(self, text="Today's Tasks", corner_radius=10, border_color='white', bg_color='gray19', fg_color='gray29', text_font=('Futura', 9),border_width=2, command=self.display_day_tasks)
        self.today_tasks_button.place(relx=0.975, rely=0.03, anchor='ne',relwidth=0.275, relheight=0.035)
        self.week_task_button = customtkinter.CTkButton(self, text ='Weekly Tasks', corner_radius=10, border_color='white', bg_color='gray19', fg_color='gray29', text_font=('Futura', 9), border_width=2)
        self.week_task_button.place(relx=0.975, rely=0.08, anchor='ne',relwidth=0.275, relheight=0.035)
        self.day_search_tasks_button = customtkinter.CTkButton(self,text='Day Search',corner_radius=10, border_color='white', bg_color='gray19', fg_color='gray29', text_font=('Futura', 9),border_width=2)
        self.day_search_tasks_button.place(relx=0.975, rely=0.13, anchor='ne', relwidth=0.275,relheight=0.035)
        self.week_search_task_button =customtkinter.CTkButton(self, text='Week Search', corner_radius=10, border_color='white', bg_color='gray19', fg_color='gray29', text_font=('Futura', 9),border_width=2)
        self.week_search_task_button.place(relx=0.975, rely=0.18, anchor='ne', relwidth=0.275, relheight=0.035)
        self.month_search_task_button = customtkinter.CTkButton(self, text='Month Search', corner_radius=10, border_color='white', bg_color='gray19', fg_color='gray29', text_font=('Futura', 9),border_width=2)
        self.month_search_task_button.place(relx=0.975, rely=0.23, anchor='ne', relwidth=0.275, relheight=0.035)

        #Adding entries to add/update/delete tasks
        self.task_name_entry = customtkinter.CTkEntry(self, placeholder_text='Title', width=150, height=30, corner_radius=10 )
        self.task_name_entry.place(relx=0.46, rely=0.3, anchor='ne')
        self.task_description_entry = customtkinter.CTkEntry(self,placeholder_text='Description', corner_radius=10, width=150, height=30)
        self.task_description_entry.place(relx=0.46, rely=0.35, anchor='ne')
        self.task_due_date_entry = customtkinter.CTkEntry(self,placeholder_text='Due Date', corner_radius=10, width=150, height=30)
        self.task_due_date_entry.place(relx=0.46, rely=0.4, anchor='ne')

        #Adding buttons to add/delete/update a task
        self.add_task_button = customtkinter.CTkButton(self, text='Add Tasks', corner_radius=10, border_color='#0E86D4', bg_color='gray19', fg_color='#0E86D4', command=self.add_task)
        self.add_task_button.place(relx=0.9, rely=0.3, anchor='ne',relwidth=0.3)
        self.update_task_button = customtkinter.CTkButton(self,text='Update Tasks', corner_radius=10, border_color='#0E86D4', bg_color='gray19', fg_color='#0E86D4', command=self.update_task)
        self.update_task_button.place(relx=0.9, rely=0.35, anchor='ne', relwidth=0.3)
        self.delete_task_button = customtkinter.CTkButton(self, text='Delete Tasks', corner_radius=10,
                                                          border_color='#0E86D4', bg_color='gray19', fg_color='#0E86D4', command=self.delete_task)
        self.delete_task_button.place(relx=0.9, rely=0.4, anchor='ne', relwidth=0.3)

        #Add button to clear form fields and another one to reset the table view
        self.clear_form_button= customtkinter.CTkButton(self, text='Clear Form', corner_radius=10, border_color='#0E86D4', bg_color='gray19', fg_color='#0E86D4', command=self.clear_form)
        self.clear_form_button.place(relx=0.35, rely=0.5, anchor='ne' ,relwidth=0.3)
        self.show_all_button =customtkinter.CTkButton(self, text='Show All Tasks' , corner_radius=10, border_color='#0E86D4', bg_color='gray19', fg_color='#0E86D4', command=self.display_all_tasks)
        self.show_all_button.place(relx = 0.9, rely=0.5, anchor='ne', relwidth=0.3)



    def clear_form(self):

        self.task_name_entry.delete(0,100)
        self.task_name_entry.configure(placeholder_text='Title')
        self.task_description_entry.delete(0,100)
        self.task_description_entry.configure(placeholder_text='Description')
        self.task_due_date_entry.delete(0,100)
        self.task_due_date_entry.configure(placeholder_text='Due Date')


    def display_all_tasks(self):
        tasks = database.fetch_all_events()
        for task in tasks:
            self.task_view.insert('', 'end', values=(task[0], task[1], task[2],task[4].date()))


    def display_selected_task(self,event):
        for selection in self.task_view.selection():
            item = self.task_view.item(selection)

            global task_id
            task_id, task_title, task_description, task_due_date = item['values'][:5]
            self.task_text_area.insert("10.0", task_description)
            self.task_title_entry.configure(placeholder_text=task_title)
            self.task_name_entry.configure(placeholder_text=task_title)
            self.task_description_entry.configure(placeholder_text=task_description)
            self.task_due_date_entry.configure(placeholder_text=task_due_date)

    def add_task(self):

        task_title = self.task_name_entry.get()
        task_description = self.task_description_entry.get()
        task_due_date = self.task_due_date_entry.get()

        database.add_event(task_title,task_description,task_due_date)
        mb.showinfo('Add Task','Task succesfully added')
        self.clear_form()
        self.task_view.delete(*self.task_view.get_children())
        self.display_all_tasks()

    def update_task(self):

        id_task =task_id
        task_title = self.task_name_entry.get()
        if not task_title:
            task_title = self.task_name_entry.placeholder_text
        task_description = self.task_description_entry.get()
        if not task_description:
            task_description = self.task_description_entry.placeholder_text
        task_due_date = self.task_due_date_entry.get()
        if not task_due_date:
            task_due_date = self.task_due_date_entry.placeholder_text
        try:
            task_due_date = parser.parse(task_due_date)
        except:
            mb.showerror('Update Task', 'Date should be in format: Year-Month-Day')
            return

        database.update_event(id_task, task_title, task_description, task_due_date)
        self.clear_form()
        self.task_view.delete(*self.task_view.get_children())
        self.display_all_tasks()

    def delete_task(self):

        id_task= task_id
        task_title = self.task_name_entry.get()

        if not task_title:
            task_title = self.task_name_entry.placeholder_text

        confirm_box = mb.askquestion('Delete Task', f"Are you sure you want to delete {task_title} ?")
        if confirm_box == 'yes':
            database.delete_event(id_task)
            mb.showinfo('Delete Task', 'Task succesfully deleted')
            self.clear_form()
            self.task_view.delete(*self.task_view.get_children())
            self.display_all_tasks()
        else:
            return


    def display_all_tasks(self):

        tasks = database.fetch_all_events()
        self.task_view.delete(*self.task_view.get_children())
        for task in tasks:
            self.task_view.insert('','end', values=(task[0], task[1], task[2], task[4].date()))


    def display_day_tasks(self):
        date=self.calendar.get_date()
        lst_date=date.split('/')
        year = '20'+lst_date[-1]
        if len(lst_date[0]) == 1:
            month = '0'+lst_date[0]
        else:
            month = lst_date[0]
        if len(lst_date[1]) == 1:
            day = '0'+lst_date[1]
        else:
            day = lst_date[1]
        final_date = f"{year}-{month}-{day}"

        tasks = database.search_task_by_day(final_date)
        self.task_view.delete(*self.task_view.get_children())
        for task in tasks:
            self.task_view.insert('','end', values=(task[0], task[1], task[2],task[4].date()))




















class MainApp(customtkinter.CTk):
    '''Class to create main window'''

    def __init__(self):
        super().__init__()
        self.geometry('1200x800')
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure((0,1), weight=1)
        self.contacts = Contacts(self)
        self.contacts.grid(row=1, columns=1, padx=10, pady=50)
        self.contacts.place(relx=0.625,rely=0.02, anchor='ne',relwidth=0.6,relheight=0.95)

        self.tasks= Tasks(self)
        self.tasks.grid(row=1,columns=2,padx=300,pady=50)
        self.tasks.place(relx=0.98, rely=0.02, anchor='ne', relwidth=0.3, relheight=0.95)







def load_images(path,size):
    '''Function to load and transform images'''
    return ImageTk.PhotoImage(Image.open(PATH+path).resize((size,size)))


app = MainApp()
app.mainloop()