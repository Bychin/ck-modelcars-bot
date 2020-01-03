from bs4 import BeautifulSoup
import requests

from constants import CK_F1_URL


def get_models_id():
    with requests.get(CK_F1_URL) as r:
        soup = BeautifulSoup(r.text, 'lxml')

    models_id = []
    model_listings = soup.findAll(class_='div_liste_punkt')

    for model_div in model_listings:
        model_a = model_div.find('h2').find('a')  # we can get item's name and link from <a> tag 
        model_id = model_a.get('href').split('/')[-2][2:]  # extract id from short url
        
        models_id.append(model_id)

    return models_id
