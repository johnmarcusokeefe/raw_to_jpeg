import sqlite3
from sqlite3 import Error

class ImageDB:

    def __init__(self, db_file_name):

        self.db_file_name = db_file_name

        try:
            self.conn = sqlite3.connect(db_file_name)
            print("Created db connection", sqlite3.version)

        except Error as e:
            print(e)
            self.conn.close()

    def open_db(self):

        conn = sqlite3.connect(self.db_file_name)
        return conn

    # create database tables
    def create_tables(self):

        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS file_data 
            (file_hash VARCHAR(255) PRIMARY KEY, saved_flag int DEFAULT 0) ''')
        self.conn.commit()

    def read_hash(self, hash_value):

        cur = self.conn.cursor()
        hash_value = cur.execute(''' SELECT COUNT(*) FROM file_data WHERE file_hash LIKE (?)''', (hash_value,))
        return hash_value.fetchall()
    #
    def get_saved_flag(self, hash_value):

        cur = self.conn.cursor()
        hash_value = cur.execute(''' SELECT * FROM file_data WHERE file_hash LIKE (?)''', (hash_value,))
        return hash_value.fetchall()

    def write_hash_to_db(self, hash_value, flag):

        cur = self.conn.cursor()
        cur.execute('''INSERT INTO file_data (file_hash, saved_flag) VALUES (?,?)''', (hash_value, flag))
        self.conn.commit()
        print("write hash and return result")
