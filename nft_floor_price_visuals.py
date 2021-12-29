import matplotlib.pyplot as plt
import pandas as pd


def plot_floor_data(floor_price_records_csv_filepath="./floor_price_records.csv", seperate_windows=True):
    floor_data_pd = pd.read_csv(floor_price_records_csv_filepath)

    if seperate_windows:
        grouped_pd = floor_data_pd.groupby(
            ['Datetime',  'Collection_Slug']).max()['Floor_Price'].unstack()
        grouped_pd.plot(subplots=True)

    else:
        grouped_pd = floor_data_pd.groupby(
            ['Datetime',  'Collection_Slug']).max()['Floor_Price'].unstack()
        grouped_pd.plot()

    print(grouped_pd)
    plt.xlabel('Datetime')
    plt.ylabel('Floor_Price')
    plt.show()


if __name__ == "__main__":
    plot_floor_data()
