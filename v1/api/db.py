""" This class sets up the project's database, and commits data to
    to its respective table
"""
import psycopg2
from werkzeug.security import check_password_hash


class DatabaseManager(object):
    def __init__(self):
        self.connection_str = "dbname='mydiary' user='postgres' password='postgres'"

    def connect_db(self):
        conn = None

        try:
            conn = psycopg2.connect(self.connection_str)

        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)

        return conn

    @staticmethod
    def insert_user(fname, lname, uname, email, password):
        """ Inserts new user into database """
        result = ''

        insert_query = """INSERT INTO users(firstname,lastname,username,email,password)
        VALUES('{0}','{1}','{2}','{3}','{4}') RETURNING uid;"""

        insert_query = insert_query.format(fname, lname, uname, email,
                                           password)

        dbm = DatabaseManager()
        conn = dbm.connect_db()

        if not conn:
            return False

        try:
            cur = conn.cursor()

            cur.execute(insert_query)

            result = cur.fetchone()[0]
            cur.close()
            conn.commit()
        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)
        finally:
            conn.close()

        return result

    @staticmethod
    def check_login_user(email, passw):
        """
        Checks the passed login credencials of a user and compares them with
        those in the database.

        Returns :boolean: indicating whether the credencials match those of any
        user.
        """
        status = False
        query = "SELECT username,email,password FROM users WHERE email='{}'"
        query = query.format(email)
        result = None

        dbm = DatabaseManager()
        conn = dbm.connect_db()

        try:
            cur = conn.cursor()

            cur.execute(query)

            result = cur.fetchone()
            cur.close()
        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)
        finally:
            conn.close()



        return status
