from string import Template

from bs4 import BeautifulSoup
import requests

from .constants import CK_URL, CK_ADD_TO_CART_API, MODELS_LIMIT


URL_TEMPLATE = Template(CK_URL+'p-$id/')


class Model():
    def __init__(self, model_id, parse=False):
        self.id = model_id
        self.url = self.__url()

        if parse:
            self.parse_info()

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
