from bs4 import BeautifulSoup
import requests

CK_F1_MODELS_URL = 'https://ck-modelcars.de/en/l/t-gesamt/k-formel1/'

CK_URL = 'https://ck-modelcars.de/en/'
CK_CART = 'w'

CK_ADD_TO_CART_API = 'w'
CK_ADD_TO_CART_URL = CK_URL+CK_ADD_TO_CART_API

MODELS_AMOUNT = 20  # CK allows to order up to 18 same models


# 58696 - Lotus 99T Senna
# 58697 - Matra MS80

def get_amount(model_id):
    soup = BeautifulSoup()

    with requests.get(CK_ADD_TO_CART_URL, params={'produkt': model_id, 'menge': MODELS_AMOUNT}) as r:
        soup = BeautifulSoup(r.text)

    el = soup.find('input', {'name': 'menge_'+str(model_id)})
    if el is None:
        return 0
    else:
        return el.get('value')