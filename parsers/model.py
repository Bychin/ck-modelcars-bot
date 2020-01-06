import re
from string import Template

from bs4 import BeautifulSoup
import requests

from .constants import CK_URL, CK_ADD_TO_CART_API, MODELS_LIMIT


URL_TEMPLATE = Template(CK_URL+'p-$id/')
URL_REGEX = re.compile(r'.*/p-(\d+)/')


class Model():
    def __init__(self, model_id, parse=False):
        self.id = model_id
        self.url = self.__url()

        if parse:
            self.parse_info()

    @classmethod
    def from_url(cls, model_url, parse=False):
        m = URL_REGEX.match(model_url)
        if m is None:
            return None

        return cls(m.group(1), parse)

    def parse_info(self):
        with requests.get(self.url) as r:
            soup = BeautifulSoup(r.text, 'lxml')

        full_name = None
        img_urls = []

        tags_with_img = soup.findAll(class_='div_shopcontent_leftimage')
        for tag in tags_with_img:
            a_tag = tag.find('a')
            img_urls.append(a_tag.get('href'))

            if full_name is None:
                full_name = a_tag.get('title')

        self.full_name = full_name
        self.img_urls = img_urls

        available = soup.find('span', {'itemprop': 'availability'}).get('content')
        self.available = True if available == 'InStock' else False

        self.price = soup.find(class_='div_preis').find('span').text

    def str_html(self):
        available_sign = '✅' if self.available else '❌'
        image = '<a href="{}">&#8204;</a>'.format(self.img_urls[0])
        text = '<a href="{}">{}</a> | {} | {}'.format(
            self.url, self.full_name, available_sign, self.price)

        return image + text

    def available_amount(self):
        with requests.get(CK_ADD_TO_CART_API, params={'produkt': self.id, 'menge': MODELS_LIMIT}) as r:
            soup = BeautifulSoup(r.text, 'lxml')

        amount_in_cart = soup.find('input', {'name': 'menge_'+str(self.id)})
        if amount_in_cart is None:
            return 0

        return amount_in_cart.get('value')

    '''
    Returns URL of model by it's id.

    E.g. for id 12345 returns 'https://ck-modelcars.de/en/p-12345/'
    '''
    def __url(self):
        return URL_TEMPLATE.substitute(id=self.id)
