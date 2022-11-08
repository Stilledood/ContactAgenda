import tkinter as tk
import customtkinter
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk
import database
from tkinter import messagebox as mb

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