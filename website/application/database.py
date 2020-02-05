import sqlite3
from sqlite3 import Error
import os
from datetime import datetime
import pickle


cwd = os.getcwd()

FILE = "messages.db"
PLAYLIST_TABLE = "Messages"


class DataBase:
    def __init__(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(FILE)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self._create_table()

    def close(self):
        self.conn.close()

    def _create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {PLAYLIST_TABLE}
                    (name TEXT, content TEXT, time Date, id INTEGER PRIMARY KEY AUTOINCREMENT)"""
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_messages(self, limit=100):
        """
        returns all messages
        """
        query = f"SELECT * FROM {PLAYLIST_TABLE} LIMIT {limit}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        results = []
        for r in result:
            name, content, date, _id = r
            data = {"name":name, "message":content, "time":date}
            results.append(data)

        return results

    def save_message(self, name, msg, time):
        """
        saves the given message
        :param name: str
        :param msg: str
        :param time: datetime
        :return:
        """
        query = f"INSERT INTO {PLAYLIST_TABLE} VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (name, msg,time, None))
        self.conn.commit()

