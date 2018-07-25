from werkzeug.security import generate_password_hash
from datetime import datetime
from ..db import DatabaseManager as dbm


class User(object):
    def __init__(self, firstname, lastname, username, email, password):
        """
        Creates a new instance of an api user
        """
        self.__uid = ''
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
            "id": self.__uid,
            "firstname": self.__firstname,
            "lastname": self.__lastname,
            "username": self.__username,
            "email": self.__email,
            "password": self.__password
        }

    def save(self):
        user_id = dbm.insert_user(self.__firstname, self.__lastname, self.__username,
                              self.__email, self.__password)
        if not user_id:
            return False
        self.uid = user_id

        return user_id

    @property
    def uid(self):
        return self.__uid

    @uid.setter
    def uid(self, uid):
        self.__uid = uid

    @staticmethod
    def get_user():
        return [x.json() for x in users_db]


class DiaryEntry(object):
    def __init__(self, title, content):
        """
        Create a new instance of a diary entry
        """
        self.__eid = ''
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

        for entry in entries_db:
            if entry.eid == eid:
                specific_entry = entry.json()

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
                new_entry.eid = x.eid
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
