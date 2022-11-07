import tkinter as tk
import customtkinter
import customtkinter as ctk
from PIL import Image, ImageTk

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme("green")
PATH='Images'

class Contacts(customtkinter.CTkFrame):
    '''Class to construct the contacts part of the window'''

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

        #Construct the form to display selected contact

        self.first_name_entry =customtkinter.CTkEntry(self, placeholder_text='First Name', width=200, height=35, corner_radius=10)
        self.first_name_entry.place(relx=0.3, rely=0.1, anchor='ne')
        self.last_name_entry =customtkinter.CTkEntry(self, placeholder_text='Last Name', width=200, height=35, corner_radius=10)
        self.last_name_entry.place(relx=0.3, rely=0.17, anchor='ne')


        self.search= customtkinter.CTkButton(text='Search',corner_radius=10,border_color='#0E86D4',bg_color='gray19', fg_color='#0E86D4')
        self.search.grid(row=2,columns=1,padx=1,pady=15)
        self.search.place(relx=0.2, rely=0.3, anchor='ne')


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