import json

import requests


def get_collection_stats(collection_slug):
    url = f'https://api.opensea.io/api/v1/collection/{collection_slug}/stats'
    headers = {"Accept": "application/json"}

    return requests.request("GET", url, headers=headers).json()


def get_floor_price(slug_name):
    collection_stats = get_collection_stats(slug_name)

    collection_floor = float(collection_stats["stats"]["floor_price"])

    datetime_now = dt.datetime.now()
    datetime_rounded = datetime_now - dt.timedelta(seconds=datetime_now.second,
                                                   microseconds=datetime_now.microsecond)

    return [datetime_rounded, slug_name, collection_floor]


def write_to_file(content, filename="collection_stats.txt"):
    with open(filename, 'w') as f:
        #     f.write(response.prettify)
        json.dump(content, f, sort_keys=True, indent=4)
        print('Written to file:', filename)


def notify(title, text):
    import os

    os.system(f"""
              osascript -e 'display notification "{text}" with title "{title}"'
              """)


def dialogue():

    import os

    os.system(f"""
              osascript - e 'display dialog "{text}" with title "{title}"'
              """)


class PriceAlert:
    def __init__(self, collection_slug, direction, price_target):
        # direction = 'below' or 'above'
        self.collection_slug = collection_slug
        self.direction = direction
        self.price_target = price_target

    def collection_stats(self):
        response = get_collection_stats(self.collection_slug)
        return response

    def compare_floor_to_price_alert(self, print_alert=False):
        collection_floor = self.collection_stats()["stats"]["floor_price"]

        if self.direction.lower() == "below":
            if collection_floor <= self.price_target:
                alert = f"{self.collection_slug} - floor_price ({collection_floor}) <= price_target ({self.price_target})"
                if print_alert:
                    print(alert)
                return alert

            else:
                alert = f"{self.collection_slug} - floor_price ({collection_floor}) > price_target ({self.price_target})"
                if print_alert:
                    print(alert)

        if self.direction.lower() == "above":
            if collection_floor >= self.price_target:
                alert = f"{self.collection_slug} - floor_price ({collection_floor}) >= price_target ({self.price_target})"
                if print_alert:
                    print(alert)
                return alert

            else:
                alert = f"{self.collection_slug} - floor_price ({collection_floor}) < price_target ({self.price_target})"
                if print_alert:
                    print(alert)

    def update__floor_file(self):
        collection_floor = self.collection_floor()


def compare_floor_for_list(price_alert_list):
    import time

    true_email_alerts_list = []

    for price_alert in price_alert_list:
        alert = price_alert.compare_floor_to_price_alert()
        if alert:
            true_email_alerts_list.append(alert)
            notify('NFT Price Alert', alert)
        time.sleep(5)

    # print(true_email_alerts_list)

    # notify('NFT Price Alert', "\n".join(true_email_alerts_list))


if __name__ == "__main__":
    # response = get_collection_stats(collection_slug="slotienft")
    # write_to_file(response)

    slotie = PriceAlert('slotienft', 'below', .42)
    zombie = PriceAlert('billionairezombiesclub', 'above', .1)
    bigtime = PriceAlert('bigtime-founders', 'above', .21)

    price_alert_list = [bigtime, slotie, zombie]

    compare_floor_for_list(price_alert_list)
