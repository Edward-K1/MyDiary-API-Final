""" This class sets up the project's database, and commits data to
    to its respective table

    Call create_tables() or drop_tables() to create or drop the database tables

"""

###
###### Note : Executing this file directly creates the required tables
###
import psycopg2
from werkzeug.security import check_password_hash


class DatabaseManager(object):
    """ Manages database operations for the API """
    connection_str = "dbname='mydiary' user='postgres' password='postgres'"

    @staticmethod
    def connect_db():
        """ Returns an active database connection to mydiary database """
        conn = None

        try:
            conn = psycopg2.connect(DatabaseManager.connection_str)
        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)

        return conn

    @staticmethod
    def insert_user(fname, lname, uname, email, password):
        """ Inserts new user into database """
        result = ''
        error = ''

        insert_query = """INSERT INTO users(firstname,lastname,username,email,password)
        VALUES('{0}','{1}','{2}','{3}','{4}') RETURNING uid;"""

        insert_query = insert_query.format(fname, lname, uname, email,
                                           password)

        conn = DatabaseManager.connect_db()

        try:
            cur = conn.cursor()

            cur.execute(insert_query)

            result = cur.fetchone()[0]
            cur.close()
            conn.commit()
        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)
            error = str(ex.pgerror)
        finally:
            conn.close()

        return result, error

    @staticmethod
    def check_login_user(email, passw):
        """
        Checks the passed login credencials of a user and compares them with
        those in the database.

        Returns :tuple(user_id,error_msg)

        When the credencials don't match, None will be returned in the place
        of the user's id
        """
        uid = None
        error = ''

        query = "SELECT uid,email,password FROM users WHERE email='{}'"
        query = query.format(email)
        result = None

        conn = DatabaseManager.connect_db()

        try:
            cur = conn.cursor()

            cur.execute(query)

            result = cur.fetchone()
            cur.close()

            if result:

                if check_password_hash(result[2], passw):
                    uid = result[0]
                else:
                    error = 'invalid login credencials'
            else:
                error = 'invalid login credencials'

        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)
            error = str(ex.pgerror)
        finally:
            conn.close()

        return uid, error

    @staticmethod
    def check_username_exists(username):
        status = False
        error = ''
        query = "select * from users where username='{}'".format(username)

        conn = DatabaseManager.connect_db()

        try:
            cur = conn.cursor()
            cur.execute(query)
            record = cur.fetchone()
            if record:
                status = True

            cur.close()
            conn.commit()
        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)
            error = str(ex.pgerror)
        finally:
            conn.close()

        return status, error

    @staticmethod
    def check_email_exists(email):
        status = False
        error = ''
        query = "select * from users where email='{}'".format(email)

        conn = DatabaseManager.connect_db()

        try:
            cur = conn.cursor()
            cur.execute(query)
            record = cur.fetchone()
            if record:
                status = True

            cur.close()
            conn.commit()
        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)
            error = str(ex.pgerror)
        finally:
            conn.close()

        return status, error

    @staticmethod
    def insert_diary_entry(uid, title, content):
        """ Inserts new diary entry into database """
        status = False
        error = ''

        insert_query = """INSERT INTO diary(uid,title,content)
        VALUES('{0}','{1}','{2}') RETURNING eid;"""

        insert_query = insert_query.format(uid, title, content)

        conn = DatabaseManager.connect_db()

        try:
            cur = conn.cursor()

            cur.execute(insert_query)

            cur.close()
            conn.commit()
        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)
            error = str(ex.pgerror)
        finally:
            conn.close()

        return status, error

    @staticmethod
    def get_diary_entries(uid):
        """ Get all diary entries for a particular user """
        query = "SELECT eid,title,content,created FROM diary WHERE uid='{}'"
        query = query.format(uid)
        result = None
        error = ''

        conn = DatabaseManager.connect_db()

        try:
            cur = conn.cursor()

            cur.execute(query)

            result = cur.fetchall()
            cur.close()

        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)
            error = str(ex.pgerror)
        finally:
            conn.close()

        return result, error

    @staticmethod
    def get_single_diary_entry(eid):
        """ Fetches a single diary entry based on its eid """
        query = "SELECT eid,title,content,created FROM diary WHERE eid='{}'"
        query = query.format(eid)
        result = None
        error = ''

        conn = DatabaseManager.connect_db()
        try:
            cur = conn.cursor()

            cur.execute(query)
            result = cur.fetchone()
            cur.close()

            if not result:
                error = "no entry with selected id found"

        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)
            error = str(ex.pgerror)
        finally:
            conn.close()

        return result, error

    @staticmethod
    def update_diary_entry(eid, title, content):
        """ Update a diary entry based on its eid """
        status = False
        error = ''

        query = "UPDATE diary SET title='{}',content='{}' WHERE eid={}"
        select = "SELECT * FROM diary WHERE eid={}".format(eid)
        query = query.format(title, content, eid)

        conn = DatabaseManager.connect_db()

        try:
            cur = conn.cursor()
            cur.execute(select)
            record = cur.fetchone()

            if not record:
                error = 404
                return status, error

            from datetime import datetime

            if not str(datetime.now())[9] == str(record[4])[9]:
                error = 403
                return status, error

            cur.execute(query)
            cur.close()
            conn.commit()
            status = True
        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)
            error = str(ex.pgerror)
        finally:
            conn.close()

        return status, error

    @staticmethod
    def delete_diary_entry(eid):
        """ Deletes a diary entry """
        status = False
        error = ''

        query = "DELETE FROM diary WHERE eid={}".format(eid)
        select = "SELECT * FROM diary WHERE eid={}".format(eid)

        conn = DatabaseManager.connect_db()

        try:
            cur = conn.cursor()

            cur.execute(select)
            record = cur.fetchone()

            if not record:
                error = "no entry with selected id found"
                return status, error

            cur.execute(query)
            cur.close()
            conn.commit()
            status = True
        except psycopg2.DatabaseError as ex:
            print(ex.pgerror)
            error = str(ex.pgerror)
        finally:
            conn.close()

        return status, error

    @staticmethod
    def create_tables():
        """ This method creates the tables in which the API stores data """

        commands = ("""
            CREATE TABLE IF NOT EXISTS users
(
    uid serial,
    firstname varchar(30) NOT NULL,
    lastname varchar(30) NOT NULL,
    username varchar(30) NOT NULL UNIQUE,
    email varchar(100) NOT NULL UNIQUE,
    password varchar(160) NOT NULL,
    PRIMARY KEY (uid)
    );""", """CREATE TABLE IF NOT EXISTS diary
(
    eid serial,
    uid integer NOT NULL,
    title varchar(200) NOT NULL,
    content text NOT NULL,
    created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (eid),
    FOREIGN KEY(uid) REFERENCES users(uid) ON UPDATE NO ACTION ON DELETE CASCADE
); """, """CREATE TABLE IF NOT EXISTS notifications
(
    nid serial,
    uid integer NOT NULL,
    created date NOT NULL DEFAULT CURRENT_DATE,
    frequency integer,
    PRIMARY KEY (nid, uid),
    FOREIGN KEY(uid) REFERENCES users(uid) ON UPDATE NO ACTION ON DELETE CASCADE
); """)

        conn = DatabaseManager.connect_db()

        try:
            cur = conn.cursor()

            for sql_command in commands:
                cur.execute(sql_command)

            cur.close()
            conn.commit()

        except Exception as ex:
            print(ex)
        finally:
            conn.close()

    @staticmethod
    def drop_tables():
        commands = ("DROP TABLE IF EXISTS notifications",
                    "DROP TABLE IF EXISTS diary", "DROP TABLE IF EXISTS users")

        dbm = DatabaseManager()
        conn = dbm.connect_db()

        try:
            cur = conn.cursor()

            for command in commands:
                cur.execute(command)

            cur.close()
            conn.commit()

        except Exception as ex:
            print(ex)
        finally:
            conn.close()


if __name__ == '__main__':
   # DatabaseManager.drop_tables()
    DatabaseManager.create_tables()
