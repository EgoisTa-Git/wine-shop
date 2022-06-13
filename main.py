import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

WINERY_FOUNDING_YEAR = 1920
winery_age = datetime.date.today().year - WINERY_FOUNDING_YEAR
if 0 < winery_age % 10 < 5:
    winery_age = f'{winery_age} года'
else:
    winery_age = f'{winery_age} лет'

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    age=winery_age,
    image='',
    title='',
    grape='',
    price='',
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
