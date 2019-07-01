import datetime
# from datetime import date
from dateutil.parser import parse
# from dateutil import tz
import json
import requests
import pandas as pd

#Season_start_date and season_end_date can take any standard format as strings.
class RainData:
    def __init__(self, season_start_date, season_end_date):
        self.start_date = parse(season_start_date)
        self.end_date = parse(season_end_date)
        self.date_range = (parse(season_end_date) -
                           parse(season_start_date)).days
        self.dates = [str(self.start_date + datetime.timedelta(i)).split()[0]
                      for i in range(self.date_range)]

    def get_rain_df(self, api_key):
        urls = ["https://api.darksky.net/forecast/"+str(api_key) +
                "/52.5200,13.4050,"+str(date) +
                "T15:00:00?exclude=currently,hourly,flags"
                for date in self.dates]

        # retrieve data and unstring
        data = []
        for i in urls:
            data.append(json.loads(requests.get(i).text))

        # unnest dictionaries
        daily_data = [data[i]['daily']['data'][0] for i in range(len(data))]
        
        #Create a data frame with date and rain dummy variable columns
        precipType = []
        for i in range(len(daily_data)):
            if 'precipType' in daily_data[i].keys():
                precipType.append(daily_data[i]['precipType'])
            else:
                precipType.append('0')
        raindf = pd.DataFrame(
            list(zip(self.dates, precipType)), columns=['Date', 'Rain'])
        raindf['Rain'] = raindf['Rain'].map(
            {'0': 0, 'rain': 1, 'sleet': 0, 'snow': 0})
        self.raindf = raindf

        return raindf
