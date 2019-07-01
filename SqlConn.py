import sqlite3
import pandas as pd


class SqlConn:
    # Initializes the object with a connection name and cursor for use in the
    # desired SQL Database
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.c = self.conn.cursor()
        self.connstat = 'Active'
        print("Connection status: " + self.connstat)

    # Takes in a list of seasons and returns a DataFrame from the Matches table
    # of the Division 1 and 2 matches from the specified seasons
    def matches_df(self, list_of_seasons):
        self.c.execute("""SELECT *
                          FROM Matches
                          WHERE Season IN (""" +
                       ', '.join([str(year) for year in list_of_seasons]) +
                       """) AND Div IN ('D1','D2')
                          ORDER BY Date""")

        df = pd.DataFrame(self.c.fetchall())
        df.columns = [x[0] for x in self.c.description]
        print("Connection status: " + self.connstat)
        return df

    # Closes the connection to the SQL database
    def close_conn(self):
        print("Closing connection")
        self.c.close()
        self.conn.close()
        self.connstat = 'Closed'
        print("Connection status: " + self.connstat)
