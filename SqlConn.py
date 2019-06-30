import sqlite3
import pandas as pd


class SqlConn:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.c = self.conn.cursor()
        self.connstat = 'Active'
        print("Connection status: " + self.connstat)

    def matches_df(self, season):
        self.c.execute("""SELECT *
                          FROM Matches
                          WHERE Season IN (""" +
                       str(season) +
                       """) AND Div IN ('D1','D2')
                          ORDER BY Date""")

        df = pd.DataFrame(self.c.fetchall())
        df.columns = [x[0] for x in self.c.description]
        print("Connection status: " + self.connstat)
        return df

    def close_conn(self):
        print("Closing connection")
        self.c.close()
        self.conn.close()
        self.connstat = 'Closed'
        print("Connection status: " + self.connstat)
