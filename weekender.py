#!/usr/bin/env python

from __future__ import print_function

import datetime
import requests
import logging
import urllib
import json
import os


class LocationFinder(object):
    def __init__(self, api_key=None):
        """Connection to Google Maps Location APIs

        Args:
            api_key (str): Key for google maps API.
        """

        self.raw_url = ('https://maps.googleapis.com'
                        '/maps/api/place/textsearch/json'
                        '?{{query}}'
                        '&key={key}'.format(key=keys['google_maps']))

    def _query(self, text):
        """Hit API

        Args:
            text (str): Query text for maps geolocation tool.

        Returns:
            response (dict): JSON API response.
        """
        formatted_text = urllib.urlencode({'query': text})
        url = self.raw_url.format(query=formatted_text)
        response = requests.get(url)
        return response.json()

    def find(self, text):
        """"""
        response = self._query(text)
        if response['status'] == 'OK' and len(response['results']) > 0:
            result = response['results'][0]
            data = {
                'name': result['name'],
                'lat': result['geometry']['location']['lat'],
                'lon': result['geometry']['location']['lng'],
            }
            return data

        else:
            logging.warning('Google maps API bad response')
            return None


class WeatherForecaster(object):
    def __init__(self, key):
        self.raw_url = ('https://api.darksky.net/forecast/'
                        '{key}/'
                        '{{lat}},{{lon}}'.format(key=key))

    def _query(self, lat, lon):
        url = self.raw_url.format(lat=lat, lon=lon)
        response = requests.get(url)
        return response.json()

    def report(self, lat, lon):
        weather_report = []
        data = self._query(lat=lat, lon=lon)
        for day in data['daily']['data']:
            summary = {
                'time': unix_to_datetime(day['time']),
                'max_temp': day['temperatureMax'],
                'min_temp': day['temperatureMin'],
                'precip_prob': day['precipProbability'],
                'summary': day['summary']
            }
            weather_report.append(summary)
        return weather_report


def unix_to_datetime(timestamp, format='%A %D'):
    date = datetime.datetime.fromtimestamp(timestamp).strftime(format)
    return date


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    keys = json.load(open(os.path.join('static', 'api_keys.json')))

    finder = LocationFinder(api_key=keys['google_maps'])
    weather = WeatherForecaster(key=keys['dark_sky'])

    info = finder.find('boulder colorado')
    forecast = weather.report(lat=info['lat'], lon=info['lon'])

    print(json.dumps(forecast, indent=2))






