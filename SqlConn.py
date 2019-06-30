import sqlite3
import pandas as pd


class SqlConn:
    def __init__(self, database_name):
        if (database_name) is str:
            self.conn = sqlite3.connect(database_name)
            self.c = self.conn.cursor
        else:
            print('Database Name must be a string')

    def matches_df(self, season):
        self.c.execute("""SELECT *
                          FROM Matches
                          WHERE Season IN """ +
                       str(season) +
                       """ AND Div IN ('D1','D2')
                          ORDER BY Date""")

        df = pd.DataFrame(self.c.fetchall())
        df.columns = [x[0] for x in c.description]
        return df

    def close_conn(self):
        self.c.close()
        self.conn.close()
