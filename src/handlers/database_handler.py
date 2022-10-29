import sqlite3
from os import path

from rich import print


class SqliteHandler:
    def __init__(self, database_name: str):
        self.__init_database(database_name)
        self.database_name = database_name
        self.con = sqlite3.connect(database_name, isolation_level=None)

    def insert_feed(self, feed_name: str, feed_url: str):
        curs = self.con.cursor()
        duplicate = curs.execute('SELECT COUNT(*) FROM FEEDS WHERE FEED_URL = ?', (feed_url,)).fetchone()[0]
        if duplicate:
            print("Already have this in the database, stopping insert")
            return
        else:
            curs.execute('INSERT INTO FEEDS(FEED_NAME,FEED_URL) values(?,?)', (feed_name, feed_url))
            print('Inseted the feed into the database')
            curs.close()

    def delete_feed(self, feed_url):
        curs = self.con.cursor()
        curs.execute('DELETE FROM FEEDS WHERE FEED_URL=?',(feed_url,))
        curs.close()

    def list_feeds(self):
        curs = self.con.cursor()
        res = curs.execute('SELECT * FROM FEEDS')
        res: list = res.fetchall()
        print('[green]Here is the list of feed [/green]')
        index = 1
        for title,url,time in res:
            print(index,title,url,time)
            index += 1

    def get_feeds(self):
        curs = self.con.cursor()
        res = curs.execute('SELECT * FROM FEEDS')
        res: list = res.fetchall()
        return res

    def __init_database(self, database_name: str):
        if path.isfile(database_name):
            print('[green]Database is up, you already got information[/green]')
        else:
            con = sqlite3.connect(database_name)
            cur = con.cursor()
            print('[red]There is no database, let make one[/red]')
            # will have a sql file in the future
            feed_schema = """
            CREATE TABLE FEEDS(
            FEED_NAME TEXT,
            FEED_URL TEXT,
            ADDED_AT DATETIME DEFAULT CURRENT_TIMESTAMP
                );"""
            cur.execute(feed_schema)
            print('[green]Database is created[/green]')
            con.close()
