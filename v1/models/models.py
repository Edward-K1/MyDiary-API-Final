import sys
from datetime import datetime

class User(object):
    users_db=[]
    def __init__(self,firstname,lastname,username,email,password):
        """
        Creates a new instance of an api user
        """
        self.__id=len(users_db)+1
        self.__firstname=firstname
        self.__lastname=lastname
        self.__username=username
        self.__email=email
        self.__password=password

    def json(self):
        """
        Returns the json representation of a user's information
        """
        return {
        "id":self.__id
        "firstname":self.__firstname
        "lastname":self.__lastname
        "username":self.__username
        "email":self.__email
        "password":self.__password
        }



class DiaryEntry(object):
    entries_db=[]
    def __init__(self,title,content,date):
        """
        Create a new instance of a diary entry
        """
        self.__eid=len(entries_db)+1
        self.__title=title
        self.__content=content
        self.__date=date

    def json(self):
        """
        Returns the json representation of a diary entry.
        """
        return {
        "eid":self.__eid
        "title":self.__title
        "content":self.__content
        "date":self.__date
        }


