import time
from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import connections

import requests

from selectolax.parser import HTMLParser

from cameras.models import IpCamera
from recorder.models import IpRecorder

SHORT_TIME = 5
LONG_TIME = 20

ADDRESSES = {
    'IpCamera': 'https://www.eltrox.pl/monitoring/monitoring-ip/kamery-ip.html?dir=desc&order=name',
    'IpRecorder': 'https://www.eltrox.pl/monitoring/monitoring-ip/rejestratory-ip.html?dir=desc&order=name'
}

connection = connections.create_connection(hosts=['127.0.0.1:9200'], timeout=20)
for k, v in ADDRESSES.items():
    current_model = eval(k)
    response = requests.get(v)
    if response.status_code == 200:
        start = time.time()
        docs = []
        tree = HTMLParser(response.content)
        count_pages = int(tree.css('.button.last')[0].text())
        for idx, _ in enumerate(range(count_pages)):
            tree = HTMLParser(response.content)
            items_on_page = tree.css('.item')
            items_on_page_count = len(items_on_page)
            for item in items_on_page:
                item_spec = {}
                link_to_product = item.css('.product-name')[0].child.next.attributes['href']
                product = requests.get(link_to_product)
                product_tree = HTMLParser(product.content)
                price_list = product_tree.css_first('.l-v2-price').text().split('\xa0', 4)
                price = price_list[0] if len(price_list) < 3 else ''.join([_ for _ in price_list[:-1]])
                table = product_tree.css('#product-attribute-specs-table')[0]
                labels = table.css('.label')
                data = table.css('.data')
                for i, label in enumerate(labels):
                    item_spec[label.text()] = " ".join(data[i].text().split())
                if 'Numer katalogowy' in item_spec and item_spec['Numer katalogowy'] != 'Brak danych':
                    kwargs = {
                        'manufacturer_id': item_spec['Numer katalogowy'],
                        'manufacturer': item_spec['Producent'] if 'Producent' in item_spec else None,
                        'model': item_spec['Model'] if 'Model' in item_spec else None,
                        'type': item_spec['Typ kamery'] if 'Typ kamery' in item_spec else None,
                        'resolution': item_spec['Rozdzielczość'] if 'Rozdzielczość' in item_spec else None,
                        'ip': item_spec['Klasa szczelności'] if 'Klasa szczelności' in item_spec else None,
                        'networ_interface': item_spec['Interfejs sieciowy'] if 'Interfejs sieciowy' in item_spec else None,
                        'network_protocols': item_spec[
                            'Wspierane protokoły sieciowe'] if 'Wspierane protokoły sieciowe' in item_spec else None,
                        'price': price,
                        'add_date': datetime.now(),
                        'meta': {'id': item_spec['Numer katalogowy']}
                    }
                    docs.append(current_model(**kwargs).to_dict(include_meta=True))
                    print('+', end='')
            if idx != count_pages - 1:
                next_page = tree.css('.button.next.i-next')[0].attributes['href']
                response = requests.get(next_page)
        bulk(Elasticsearch(), docs)
        end = time.time()
        print('\n')
        print(f'It takes {end - start}')

# list_of_cameras = go_through_every_item_on_site()
