import pymongo
import pandas as pd


class MongoHandler:
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
        print('Collection '+collName+' added')
        return collection

    # Clears the collection passed of all data
    def clear_collection(self, db, collName):
        self.client[db][collName].delete_many({})
        print('Collection cleared')

    # Fills the collection with the dataframe passed in
    def fill_db(self, db, collName, DataFrame):
        list_of_teams = []
        for i in range(len(DataFrame)):
            team_to_add = {'name': DataFrame.index[i],
                           '2011_goals': int(DataFrame.iloc[i].tot_home_goals),
                           '2011_wins': int(DataFrame.iloc[i].tot_home_win),
                           '2011_loss': int(DataFrame.iloc[i].tot_home_loss),
                           '2011_draw': int(DataFrame.iloc[i].tot_home_draw),
                           '2011_graph': DataFrame.iloc[i].graph
                           }
            list_of_teams.append(team_to_add)

        results = self.client[db][collName].insert_many(list_of_teams)
        return results.inserted_ids

    # Query the database, makes sure no one tries to call the graph
    # (because .ipynb hates it)
    def query_db(self, db, collName, wdict={}, sdict={'graph': 0}):
        if sdict['graph'] != 0:
            print('Please do not query the graph, it breaks things in .ipynb')
        else:
            query = self.client[db][collName].find(wdict, sdict)
            return query
