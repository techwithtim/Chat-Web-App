import sqlite3
from sqlite3 import Error
import os
from datetime import datetime
import time

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
        """
        close the db connection
        :return: None
        """
        self.conn.close()

    def _create_table(self):
        """
        create new database table if one doesn't exist
        :return: None
        """
        query = f"""CREATE TABLE IF NOT EXISTS {PLAYLIST_TABLE}
                    (name TEXT, content TEXT, time Date, id INTEGER PRIMARY KEY AUTOINCREMENT)"""
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_messages(self, limit=100):
        """
        returns all messages
        :param limit: int
        :return None
        """
        query = f"SELECT * FROM {PLAYLIST_TABLE}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        results = []
        for r in sorted(result, key=lambda x: x[3], reverse=True)[:limit]:
            name, content, date, _id = r
            data = {"name":name, "message":content, "time":str(date)}
            results.append(data)

        return list(reversed(results))

    def save_message(self, name, msg):
        """
        saves the given message in the table
        :param name: str
        :param msg: str
        :param time: datetime
        :return: None
        """
        query = f"INSERT INTO {PLAYLIST_TABLE} VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (name, msg, datetime.now(), None))
        self.conn.commit()

