import mysql.connector
from databasedata import username,password




def create_check_database():
    '''Function to check if the database exists-if it not exists it creates the database and all the tables '''

    mydb = mysql.connector.connect(host ='localhost', user =username, password =password, consume_results =True)
    mycursor = mydb.cursor(buffered = True)
    mycursor.execute('SHOW DATABASES')

    if ('personalagenda',) in mycursor:
        return

    else:
        mycursor.execute('CREATE DATABASE personalagenda')
        mycursor.close()

        # Creating the contacts table
        mydb = mysql.connector.connect(host='localhost', user=username, password=password, consume_results=True)
        mycursor = mydb.cursor(buffered =True)
        mycursor.execute('USE personalagenda')
        mycursor.execute("""CREATE TABLE contacts(
                         id INT  AUTO_INCREMENT PRIMARY KEY,
                         first_name VARCHAR(255) DEFAULT 'no name',
                         last_name VARCHAR(255) DEFAULT 'no name' ,
                         email VARCHAR(255),
                         phone VARCHAR(25))"""
                         )

        mycursor.close()


        # Creating the events table
        mydb = mysql.connector.connect(host='localhost', user=username, password=password, consume_results=True)
        mycursor = mydb.cursor(buffered =True)
        mycursor.execute('USE personalagenda')
        mycursor.execute("""CREATE TABLE events(
                         id INT  AUTO_INCREMENT PRIMARY KEY,
                         title VARCHAR(255) ,
                         description VARCHAR(255) ,
                         date_added TIMESTAMP DEFAULT NOW(),
                         finalizing_date DATETIME)"""
                         )
        # Commiting all the changes
        mycursor.close()



def display_all_contacts():
    '''Function to fetch all the contacts from contacts table'''

    mydb = mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    mycursor = mydb.cursor()
    query='SELECT * FROM contacts'
    mycursor.execute(query)
    records = mycursor.fetchall()
    mycursor.close()
    for record in records:
        print(record)
    return records






def add_contact(first_name, last_name, email,phone):
    '''Function to add a contact in table contacts'''

    mydb = mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    mycursor = mydb.cursor()
    #Adding the contact
    sql_query = "INSERT INTO contacts(first_name,last_name,email,phone) VALUES(%s, %s, %s, %s)"
    val = (first_name, last_name, email, phone)
    mycursor.execute(sql_query, val)
    mydb.commit()

    mycursor.close()


def search_contact(last_name):
    '''Function to search contacts based on last name'''

    mydb = mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    my_cursor = mydb.cursor()
    sql_query = 'SELECT * FROM contacts WHERE last_name = %s'
    val=(last_name,)
    my_cursor.execute(sql_query,val)
    records = my_cursor.fetchall()
    if records:
        my_cursor.close()
        return records

    else:
        records =[]
        my_cursor.close()
        return records



def update_contact(id, first_name, last_name, email, phone):
    '''Function to update a contact from contacts table'''


    mydb = mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    my_cursor = mydb.cursor()
    mysql_query = 'UPDATE contacts SET first_name = %s , last_name = %s , email = %s, phone = %s WHERE id = %s'
    vals = (first_name, last_name, email, phone, id)
    my_cursor.execute(mysql_query, vals)
    mydb.commit()
    my_cursor.close()


def delete_contact(id):
    '''Function to delete a entry from contacts table base on the id value'''

    mydb= mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    my_cursor = mydb.cursor()

    mysql_query = 'DELETE FROM contacts WHERE id = %s'
    val=(id,)

    my_cursor.execute(mysql_query,val)
    mydb.commit()
    my_cursor.close()





def fetch_all_events():
    '''Function to fetch all events from events table'''

    mydb = mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    mycursor = mydb.cursor()
    sql_query = "SELECT * FROM events"
    try:
        mycursor.execute(sql_query)
        records = mycursor.fetchall()
        mycursor.close()
    except:
        records = []
    return records






def add_event(title, description, finalizing_date):
    '''Function to add an evnet on the event table'''

    mydb = mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    sql_query = "INSERT INTO events(title,description,finalizing_date) VALUES(%s, %s, %s)"
    val = (title, description, finalizing_date)
    mycursor = mydb.cursor()
    mycursor.execute(sql_query, val)
    mydb.commit()
    mycursor.close()


def update_event(id, title, description, date):
    '''Function to update a task'''

    mydb = mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    my_cursor = mydb.cursor()
    sql_query = "UPDATE events SET title = %s , description = %s, finalizing_date = %s WHERE id = %s"
    vals=(title, description, date, id)
    my_cursor.execute(sql_query, vals)
    mydb.commit()
    my_cursor.close()

def delete_event(id):
    '''Function to delete a task from events tabel'''

    mydb =mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    my_cursor= mydb.cursor()
    sql_query = 'DELETE FROM events WHERE id = %s'
    vals = (id,)
    my_cursor.execute(sql_query, vals)
    mydb.commit()
    my_cursor.close()

def search_task_by_day(date):
    '''Function to search for task task with due date on a selected day'''

    mydb = mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    mycursor = mydb.cursor(buffered=True)
    sql_query = "SELECT * FROM events WHERE finalizing_date = %s"
    vals = (date,)
    mycursor.execute(sql_query, vals)
    records = mycursor.fetchall()
    mycursor.close()
    return records


