

class Person:
    '''Class to construct a model for each person from agenda'''

    def __init__(self,first_name=None,last_name=None,phone=None,mobile_phone=None,email=None):

        self.first_name=first_name
        self.last_name=last_name
        self.phone=phone
        self.mobile_phone=mobile_phone
        self.email=email

    def __repr__(self):
        return f'Person({self.first_name,self.last_name,self.phone,self.mobile_phone,self.email})'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    