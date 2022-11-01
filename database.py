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



def fetch_all_events():
    '''Function to fetch all events from events table'''

    mydb = mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    mycursor = mydb.cursor()
    sql_query = "SELECT * FROM events"
    try:
        mycursor.execute(sql_query)
        records = mycursor.fetchall()
    except:
        records = 'No events added'
    if not records:
        records = 'No events added'
    print(records)



def add_event(title, description, finalizing_date):
    '''Function to add an evnet on the event table'''

    mydb = mysql.connector.connect(host='localhost', user=username, password=password, database='personalagenda')
    sql_query = "INSERT INTO events(title,description,finalizing_date) VALUES(%s, %s, %s)"
    val = (title, description, finalizing_date)
    mycursor = mydb.cursor()
    mycursor.execute(sql_query, val)
    mydb.commit()
    mycursor.close()









