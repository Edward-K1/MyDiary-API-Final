""" This class sets up the project's database, and commits data to
    to its respective table
"""
import psycopg2


class DatabaseManager(object):
    def __init__(self):
        self.connection_str = "dbname='mydiary' user='postgres' password='postgres'"

    def connect_db(self):
        conn = None

        try:
            conn = psycopg2.connect(self.connection_str)

        except Exception as ex:
            print(ex)

        return conn

    def insert_user(self, fname, lname, uname, email, password):
        """ Inserts new user into database """
        result = ''

        insert_query = "INSERT INTO users(firstname,lastname,username,email,password) VALUES({0},{1},{2},{3},{4}) RETURNING uid;"
        insert_query = insert_query.format(fname, lname, uname, email, password)

        conn = self.connect_db()

        cur = conn.cursor()

        cur.execute(insert_query)

        result = cur.fetchone()[0]
        cur.close()
        conn.commit()
        return result
