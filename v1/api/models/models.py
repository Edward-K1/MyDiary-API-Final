from werkzeug.security import generate_password_hash
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

    def save(self):
        """ Commit current instance of a user to the database """
        result = dbm.insert_user(self.__firstname, self.__lastname,
                                 self.__username, self.__email,
                                 self.__password)

        return result

    @staticmethod
    def get_login_user(email, password):
        """
        Return user id if the given login credencials match those of any user
        in the database
        """
        return dbm.check_login_user(email, password)


class DiaryEntry(object):
    def __init__(self, uid, title, content):
        """
        Create a new instance of a diary entry
        """
        self.__uid = uid
        self.__title = title
        self.__content = content

    def save(self):
        """
        Commit current instance of a diary entry to the database
        """
        return dbm.insert_diary_entry(self.__uid, self.__title, self.__content)


    @staticmethod
    def get_all_diary_entries(uid):
        """ Fetch the diary entries of a particular user """
        return dbm.get_diary_entries(uid)

    @staticmethod
    def get_single_entry(eid):
        """ Fetch a specific diary entry based on its id """
        return dbm.get_single_diary_entry(eid)

    @staticmethod
    def modify_entry(eid, title, content):
        """
        Modifies a diary entry based on its eid
        """
        return dbm.update_diary_entry(eid, title, content)

    @staticmethod
    def delete_entry(eid):
        """
        Deletes a diary entry
        """
        return dbm.delete_diary_entry(eid)
