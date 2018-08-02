from werkzeug.security import generate_password_hash
from ..db import DatabaseManager


class User(DatabaseManager):
    def __init__(self,
                 firstname=None,
                 lastname=None,
                 username=None,
                 email=None,
                 password=''):
        """
        Creates a new instance of an api user
        """
        DatabaseManager.__init__(self)
        self.__firstname = firstname
        self.__lastname = lastname
        self.__username = username
        self.__email = email
        self.__password = generate_password_hash(password)

    def save(self):
        """ Commit current instance of a user to the database """
        username_check = self.check_username_exists(self.__username)
        email_check = self.check_email_exists(self.__email)

        if username_check[0]:
            return "The selected username is not available", 409
        else:
            if email_check[0]:
                return "The selected email already exists. Please log in.", 409

        result = self.insert_user(self.__firstname, self.__lastname,
                                  self.__username, self.__email,
                                  self.__password)

        return result

    def get_login_user(self, email, password):
        """
        Return user id if the given login credencials match those of any user
        in the database
        """
        return self.check_login_user(email, password)


class DiaryEntry(DatabaseManager):
    """ Create a new instance of a diary entry """

    db_labels = ("eid", "title", "content", "created")

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
        return self.insert_diary_entry(self.__uid, self.__title,
                                       self.__content)

    @staticmethod
    def jsonify_and_attach_labels(items: list):
        return {
            DiaryEntry.db_labels[0]: items[0],
            DiaryEntry.db_labels[1]: items[1],
            DiaryEntry.db_labels[2]: items[2],
            DiaryEntry.db_labels[3]: items[3]
        }

    def get_all_diary_entries(self, uid):
        """ Fetch the diary entries of a particular user """
        result = self.get_diary_entries(uid)
        jsonified_list = []
        for entry in result[0]:
            jsonified_list.append(DiaryEntry.jsonify_and_attach_labels(entry))

        return jsonified_list

    def get_single_entry(self, eid):
        """ Fetch a specific diary entry based on its id """
        entry = self.get_single_diary_entry(eid)
        jsonified = ''
        if isinstance(entry[0], tuple):
            jsonified = DiaryEntry.jsonify_and_attach_labels(entry[0])
        return jsonified, entry[1]

    def modify_entry(self,eid, title, content):
        """
        Modifies a diary entry based on its eid
        """
        return self.update_diary_entry(eid, title, content)

    def delete_entry(self,eid):
        """
        Deletes a diary entry
        """
        return self.delete_diary_entry(eid)
