import datetime as dt
import json
import os.path

import matplotlib.pyplot as plt
import pandas as pd
import requests

datetime_now = dt.datetime.now()

print(datetime_now)

datetime_rounded = datetime_now - dt.timedelta(minutes=datetime_now.minute % 10,
                                               seconds=datetime_now.second,
                                               microseconds=datetime_now.microsecond)

print(datetime_rounded)
