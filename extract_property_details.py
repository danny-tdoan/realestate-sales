import pandas as pd
from bs4 import BeautifulSoup
import property_detail_extractor as p
import pickle
import logging
import random
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(process)s %(levelname)s %(message)s',
    filename='/tmp/get-property_details.log',
    filemode='a'
)


url = 'https://www.domain.com.au/55-84-trenerry-crescent-abbotsford-vic-3067-2014242733'

urls = open('listing_url.csv').read().split()

ids = []
titles = []
descriptions = []

for url in urls:
    try:
        page = p.get_listing_page(url)
        soup = BeautifulSoup(page)
        js_var = p.get_js_variables(soup)

        listing_id = p.get_listing_id(js_var)

        # details
        title = p.get_title(js_var)
        description = p.get_description(js_var)

        # photos
        photos, floorplan = p.get_photos(js_var)

        p.download_photo(photos, floorplan, listing_id)

        ids.append(listing_id)
        titles.append(title)
        descriptions.append('\n'.join(description))

        logging.debug('Finished listing id {}'.format(listing_id))
        time.sleep(random.random())
    except:
        pass

df = pd.DataFrame({'ids': ids, 'titles': titles, 'descriptions': descriptions})

pickle.dump(df, open('id_title_description.pkl', 'wb'))
