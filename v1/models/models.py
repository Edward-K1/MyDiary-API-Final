from werkzeug.security import generate_password_hash
from datetime import datetime

users_db = []
entries_db = []


class User(object):
    def __init__(self, firstname, lastname, username, email, password):
        """
        Creates a new instance of an api user
        """
        self.__id = len(users_db) + 1
        self.__firstname = firstname
        self.__lastname = lastname
        self.__username = username
        self.__email = email
        self.__password = generate_password_hash(password)

    def json(self):
        """
        Returns the json representation of a user's information
        """

        return {
            "id": self.__id,
            "firstname": self.__firstname,
            "lastname": self.__lastname,
            "username": self.__username,
            "email": self.__email,
            "password": self.__password
        }

    def save(self):
        users_db.append(self)

    @staticmethod
    def get_all_users():
        return [x.json() for x in users_db]


class DiaryEntry(object):
    def __init__(self, title, content):
        """
        Create a new instance of a diary entry
        """
        self.__eid = len(entries_db) + 1
        self.__title = title
        self.__content = content
        self.__date = str(datetime.now())[:19]

    def json(self):
        """
        Returns the json representation of a diary entry.
        """
        return {
            "eid": self.__eid,
            "title": self.__title,
            "content": self.__content,
            "date": self.__date
        }

    def save(self):
        """
        Adds an instance of a diary entry to the list of entries
        """
        entries_db.append(self)

    @property
    def eid(self):
        return self.__eid

    @eid.setter
    def eid(self, eid):
        self.__eid = eid

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @staticmethod
    def get_all_diary_entries():

        return [x.json() for x in entries_db]

    @staticmethod
    def get_single_entry(eid):

        specific_entry = ''
        f=open("debug id file.txt","w")
        f.write(str(eid))


        for entry in entries_db:
            if entry.eid == eid:
                specific_entry = entry.json()

        f.write(str(specific_entry))
        f.close()

        return specific_entry

    @staticmethod
    def modify_entry(eid, title, content):
        """
        Modifies a diary entry based on its eid
        """
        status = False

        for x in entries_db:
            if x.eid == eid:
                new_entry = DiaryEntry(title, content)
                new_entry.eid = eid
                new_entry.date = x.date
                entries_db.remove(x)
                entries_db.append(new_entry)
                status = True

        return status

    @staticmethod
    def delete_entry(eid):
        status = False

        for entry in entries_db:
            if entry.eid == eid:
                entries_db.remove(entry)
                status = True

        return status
