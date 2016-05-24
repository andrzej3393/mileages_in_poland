from lxml import html
import requests
import collections
import re
import statistics
import time
import matplotlib.pyplot as plt


def get_data_from_page(page_num):
    url = 'http://otomoto.pl/osobowe/?page={}'.format(page_num)
    raw_html = requests.get(url)
    tree = html.fromstring(raw_html.content)
    built_years = tree.xpath("//ul[@class='om-params-list']/li[1]/span/text()")
    mileages = tree.xpath("//ul[@class='om-params-list']/li[2]/span/text()")
    return zip(built_years, mileages)


def save_page(page, raw_data):
    for item in page:
        try:
            built_year = int(item[0])
        except ValueError:
            continue
        mileage_stripped = re.sub('\D', '', item[1])
        try:
            mileage = int(mileage_stripped)
        except ValueError:
            continue
        if (mileage > 1000000):
            continue
        raw_data[built_year].append(mileage)


def avg_calculations(raw_data):
    averages = {}
    for year in raw_data:
        if len(raw_data[year]) < 10:
            continue
        averages[year] = statistics.mean(raw_data[year])
    return averages


def get_data_for_chart():
    raw_data = collections.defaultdict(list)
    for page in range(1, 501):
        print(page)
        page_raw_data = get_data_from_page(page)
        save_page(page_raw_data, raw_data)
        time.sleep(3)
    return avg_calculations(raw_data)


if __name__ == '__main__':
    data_for_chart = get_data_for_chart()
    plt.bar(data_for_chart.keys(), data_for_chart.values())
    plt.savefig("fig.png")
