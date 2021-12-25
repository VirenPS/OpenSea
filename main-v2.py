import datetime as dt
import json
import os.path

import matplotlib.pyplot as plt
import pandas as pd
import requests


def get_collection_stats(collection_slug):
    url = f"https://api.opensea.io/api/v1/collection/{collection_slug}/stats"
    headers = {"Accept": "application/json"}

    return requests.request("GET", url, headers=headers).json()


def get_floor_price(slug_name):
    collection_stats = get_collection_stats(slug_name)

    collection_floor = float(collection_stats["stats"]["floor_price"])

    datetime_now = dt.datetime.now()
    datetime_rounded = datetime_now - dt.timedelta(seconds=datetime_now.second,
                                                   microseconds=datetime_now.microsecond)

    return [datetime_rounded, slug_name, collection_floor]


def append_floor_data_to_file(tracked_slug_list, filepath="floor_price_records.csv"):
    new_floor_data = []

    for slug in tracked_slug_list:
        slug_floor = get_floor_price(slug)
        new_floor_data.append(slug_floor)
        # print(slug_floor)

    new_floor_data_df = pd.DataFrame(new_floor_data, columns=[
        'Datetime', 'Collection_Slug', 'Floor_Price'])

    if not os.path.exists(filepath):
        print(f'File not found at {filepath}')
        new_floor_data_df.to_csv(filepath, index=False)
        print(f'Created new floor data file: {filepath}')
    else:
        print(f'File found at {filepath}')

        old_floor_price_df = pd.read_csv("floor_price_records.csv")

        updated_floor_price_df = old_floor_price_df.append(
            new_floor_data_df, ignore_index=True)

        updated_floor_price_df.to_csv(filepath, index=False)
        print(f'Appended latest floor data to file. \n{filepath}')


def plot_floor_data(floor_price_records_csv_filepath="floor_price_records.csv", seperate_windows=True):
    floor_data_pd = pd.read_csv(floor_price_records_csv_filepath)

    # # # unstack transposes - i.e. pushes datetime horizontal.
    # test_pd = floor_data_pd.groupby(
    #     ['Collection_Slug', 'Datetime']).max()['Floor_Price'].unstack()
    # print(test_pd)

    if seperate_windows:
        floor_data_pd.groupby(
            ['Datetime',  'Collection_Slug']).max()['Floor_Price'].unstack().plot(subplots=True)

    else:
        floor_data_pd.groupby(
            ['Datetime',  'Collection_Slug']).max()['Floor_Price'].unstack().plot()

    plt.show()


if __name__ == "__main__":
    tracked_slug_list = [
        "bigtime-founders", "slotienft", "billionairezombiesclub"]

    append_floor_data_to_file(tracked_slug_list)

    plot_floor_data()
