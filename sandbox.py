#!/usr/bin/env python

from __future__ import print_function

import datetime
import json
import os


def unix_to_datetime(timestamp, format='%A %D'):
    date = datetime.datetime.fromtimestamp(timestamp).strftime(format)
    return date


data = json.load(open(os.path.join('static', 'dark_sky.json')))
for day in data['daily']['data']:
    summary = {
        'time': unix_to_datetime(day['time']),
        'max_temp': day['temperatureMax'],
        'min_temp': day['temperatureMin'],
        'precip_prob': day['precipProbability'],
        'precip_type': day['precipType'],
        'summary': day['summary']
    }

    print(json.dumps(summary, indent=2))

