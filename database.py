import mysql.connector
from databasedata import username,password




def create_check_database():
    '''Function to check if the database exists-if it not exists it creates the database and all the tables '''

    mydb=mysql.connector.connect(host= 'localhost', user=username, password= password)
    mycursor=mydb.cursor()
    mycursor.execute('SHOW DATABASES')


    if ('agenda',) in mycursor:
        

        return
    else:
        mycursor.execute('USE agenda')
        mycursor.execute('CREATE DATABASE agenda')

        #Creating the contacts table
        mycursor.execute("CREATE TABLE contacts("
                         "id INT PRIMARY KEY AUTO_INCREMENT,"
                         "first_name VARCHAR(255) DEFAULT 'no name',"
                         "last_name VARCHAR(255) DEFAULT 'no name' ,"
                         "email VARCHAR(255),"
                         "phone VARCHAR(25),"
                         "adress VARCHAR(255)),"
                         "city VARCHAR(255),"
                         "country VARCHAR(255)")

        #Creating the events table
        mycursor.execute("CREATE TABLE events(id INT PRIMARY KEY AUTO_INCREMENT ,"
                         "title VARCHAR(255) ,"
                         "description VARCHAR(255) ,"
                         "date_added TIMESTAMP NOW(),"
                         "finalizing_date DATE"
                         )
        #Commiting all the changes
        mycursor.commit()
        mycursor.close()







