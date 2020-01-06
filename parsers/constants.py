CK_URL = 'https://ck-modelcars.de/en/'

CK_CART_URL = CK_URL+'w'  # shop's cart

'''
API that adds item into shop's cart

Useful parameters:
    produkt: id of an item.
    menge: quantity of an item.
'''
CK_ADD_TO_CART_API = CK_CART_URL

MODELS_LIMIT = 18  # CK allows to add to cart up to 18 same items
