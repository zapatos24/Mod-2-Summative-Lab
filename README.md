# Mod-2-Summative-Lab
Shared Mod 2 Lab Repo
In this project we created four classes to accomplish the following tasks:

1. SQLConn: Accessing soccer data from SQL database, and returning the relevant data from SQL as a pandas dataframe

2. PandaHandler: Creating aggregate team statistics on goals scored and match results, and creating match results bar charts, and later merging weather data into the df and using it to create statistics.

3. RainData: Accessing the Dark Sky api to return weather data for the dates of the matche and merging it into the existing data frame

4. MongoHandler: Storing the results in a Mongo database

Notes on SQLConn:
Can take a list of seasons as the season argument


Notes on RainData:
Exists in two iterations: a basic one, and an improved version capable of taking in any location and time and automatically returning data with the correct timezone and day light savings modifications

Notes on MongoHandler:
Prevents user from accessing graphs within a jupyter notebook to avoid compatibility issues 
Provides the option to pass user-created dictionaries to mongo or to convert an entire dataframe into a list of dictionaries and then pass it to mongo




