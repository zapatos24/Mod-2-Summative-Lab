import pymongo
import pandas as pd


class MongoHandler():
    def __init__(self, mongoDBadd):
        self.client = pymongo.MongoClient(mongoDBadd)

    # Returns a list of the names of the databases on the server
    def check_dbs(self):
        return self.client.list_database_names()

    # Create a new database on the server
    def make_db(self, dbName):
        db = self.client[dbName]
        print('Database '+dbName+' added')
        return db

    # Create a new collection on the server
    def make_collection(self, db, collName):
        collection = self.client[db][collName]
        print('Collection '+collName+' added in '+db+' database')
        return collection

    # Returns the working tree for the passed collection name
    def enter_collection(self, db, collName):
        return self.client[db][collName]

    # Clears the collection passed of all data
    def clear_collection(self, db, collName):
        self.client[db][collName].delete_many({})
        print('Collection '+collName+' cleared')

    # Create dictionary for entry into MongoDB from Pandas DataFrame
    def make_dict_from_df(DataFrame, rownum):
        season = str(int(DataFrame.Season.iloc[rownum]))
        team_to_add = {'name': DataFrame.index[rownum],
                       season+'_goals': int(DataFrame.iloc[rownum].GoalsScored),
                       season+'_wins': int(DataFrame.iloc[rownum].Wins),
                       season+'_losses': int(DataFrame.iloc[rownum].Losses),
                       season+'_draws': int(DataFrame.iloc[rownum].Draws),
                       season+'_raingames': int(DataFrame.iloc[rownum].RainGames),
                       season+'_nonraingames': int(DataFrame.iloc[rownum].NonRainWins),
                       season+'_rainwin%': float(DataFrame.iloc[rownum]['RainWin%']),
                       season+'_nonrainwin%': float(DataFrame.iloc[rownum]['NonRainWin%']),
                       season+'_change%': float(DataFrame.iloc[rownum]['%ChangeWinWithRain']),
                       'graph': DataFrame.iloc[rownum].graph
                       }
        return team_to_add

    # Create list of dictionaries for entry into database
    def list_of_dicts(DataFrame):
        list_of_teams = []
        for i in range(len(DataFrame)):
            team_to_add = MongoHandler.make_dict_from_df(DataFrame, i)
            list_of_teams.append(team_to_add)
        return list_of_teams

    # Query the database, makes sure no one tries to call the graph
    # (because Jupyter Notebooks hate it)
    def query_db(self, db, collName, wdict={}, sdict={'_id': 0, 'graph': 0}):
        if sdict['graph'] != 0:
            print("Please don't query the graph, Jupyter Notebooks get cranky")
            return []
        else:
            query = self.client[db][collName].find(wdict, sdict)
            return query
