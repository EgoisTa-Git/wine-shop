import argparse
import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pprint import pprint

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

WINERY_FOUNDING_YEAR = 1920


def get_winery_age(founding_year):
    age = datetime.date.today().year - founding_year
    if 0 < age % 10 < 5:
        return f'{age} года'
    else:
        return f'{age} лет'


def get_wines(wines_data_frame):
    wines_serial = wines_data_frame.to_dict(orient='records')
    # pprint(wines_serial)
    # print(type(wines_serial))
    wines = defaultdict(list)
    for wine in wines_serial:
        category, *values = wine.values()
        wines[category].append(wine)
    return wines


def parse_argument():
    parser = argparse.ArgumentParser(description='Сайт магазина авторского вина')
    parser.add_argument(
        '--wine',
        default='wine.xlsx',
        help='Excel-файл с ассортиментом продукции',
    )
    arg = parser.parse_args()
    return arg.wine


if __name__ == '__main__':
    winery_age = get_winery_age(WINERY_FOUNDING_YEAR)
    wine_path = parse_argument()
    wines_df = pandas.read_excel(
        io=wine_path,
        na_values='nan',
        keep_default_na=False,
    )
    wines = get_wines(wines_df)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        age=winery_age,
        wines=wines,
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
