from bs4 import BeautifulSoup
from string import Template

import requests

from .constants import CK_URL


CK_LISTING_TEMPLATE = Template(CK_URL+'l/t-gesamt/k-$category')
CK_F1_CATEGORY = 'formel1'


class Listing():
    def __init__(self, category):
        self.category = category
        self.url = CK_LISTING_TEMPLATE.substitute(category=self.category)

        self.__cached_models_id = set()

    '''
    Tries to find new models id in CK shop (new listings).

    Returns list of new models id that were found in CK shop and were not cached before.
    '''
    def get_new_models_id(self):
        latest_m_ids = self.__get_models_id()

        new_models_id = latest_m_ids.difference(self.__cached_models_id)
        self.__cached_models_id = latest_m_ids

        return new_models_id

    '''
    Gets up to 18 (CK default limit, can be changed via URL) of the latest models.
    '''
    def __get_models_id(self):
        with requests.get(self.url) as r:
            soup = BeautifulSoup(r.text, 'lxml')

        models_id = set()
        model_listings = soup.findAll(class_='div_liste_punkt')

        for model_div in model_listings:
            model_a = model_div.find('h2').find('a')  # we can get item's name and link from <a> tag 
            model_id = model_a.get('href').split('/')[-2][2:]  # extract id from short url

            models_id.add(model_id)

        return models_id

def new_F1_listing():
    return Listing(CK_F1_CATEGORY)
