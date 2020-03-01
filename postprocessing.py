import numpy as np

def convert_price(price):
    if np.isnan(price) or price == -1:
        return -1
    else:
        if 'm' in price:
            factor = 1e6
        elif 'k' in price:
            factor = 1e4

        price = float(price[1:-1])*factor

    return price
    # $1.116m, $530k
