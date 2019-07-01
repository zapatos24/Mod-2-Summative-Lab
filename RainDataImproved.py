import pytz
import datetime
from datetime import date
from dateutil.parser import parse
from dateutil import tz
import json
import requests
import pandas as pd
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
geolocator = Nominatim(user_agent="Je/Remy")
tf = TimezoneFinder(in_memory=True)
TimezoneFinder.using_numba()


class RainData:

    def __init__(self, season_start_date, season_end_date,
                 location='Berlin', time_24hours='15:00'):
        self.location = geolocator.geocode(location, language='en-US')
        self.timezone = tf.timezone_at(
            lng=self.location.longitude, lat=self.location.latitude)
        self.start_date = parse(season_start_date)
        self.end_date = parse(season_end_date)
        self.date_range = (parse(season_end_date) -
                           parse(season_start_date)).days
        self.dates = [str(self.start_date + datetime.timedelta(i)).split()[0]
                      for i in range(self.date_range)]
        offsets = [pytz.timezone(self.timezone).localize(
            parse(i)).strftime('%z') for i in self.dates]
        times = ['T' + str(time_24hours) + ':00' + offset[:3] +
                 ':' + offset[3:] for offset in offsets]
        self.datetimes = [self.dates[i] + times[i]
                          for i in range(len(self.dates))]

    def get_rain_df(self, api_key):
        urls = ["https://api.darksky.net/forecast/"+str(api_key)+"/" +
                str(self.location.latitude)+','+str(self.location.longitude) +
                ',' + datetime + "?exclude=currently,hourly,flags"
                for datetime in self.datetimes]

        # retrieve data and unstring
        data = []
        for i in urls:
            data.append(json.loads(requests.get(i).text))

        # unnest dictionaries
        daily_data = [data[i]['daily']['data'][0] for i in range(len(data))]
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
