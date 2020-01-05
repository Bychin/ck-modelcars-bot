from bs4 import BeautifulSoup
import requests

from .constants import CK_ADD_TO_CART_API, MODELS_LIMIT


def get_amount(model_id):
    with requests.get(CK_ADD_TO_CART_API, params={'produkt': model_id, 'menge': MODELS_LIMIT}) as r:
        soup = BeautifulSoup(r.text, 'lxml')

    el = soup.find('input', {'name': 'menge_'+str(model_id)})
    if el is None:
        return 0

    return el.get('value')

