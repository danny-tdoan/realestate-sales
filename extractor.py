from bs4 import BeautifulSoup
import requests

ARTICLE_CLASS = 'css-3xqrp1'
SUBURB_CLASS = 'css-1czqru0'
UL_CLASS = 'css-ymwd1t'
PROPERTY_CLASS = 'css-1hnr0ia'
PROPERTY_DETAILS = 'css-dpwygs'
NUM_BEDS_CLASS = 'css-1g2pbs1'
OUTCOME_CLASS = 'css-43wvni'
AGENT_CLASS = 'css-1wxwou3'
PASSEDIN_CLASS = 'css-pczn8c'


def get_one_page(url):
    response = requests.get(url)

    return response.text


def extract_one_property(suburb_name, property):
    address = ""
    domain_link = ""
    property_type = ""
    property_beds = ""
    agent = ""
    outcome_sold = ""
    outcome_price = ""

    res = {}

    property_link = property.find('a', {'class': PROPERTY_CLASS})
    address = property_link.text
    domain_link = property_link['href']

    # Get the details
    property_details = property.find('li', {'class': PROPERTY_DETAILS})
    try:
        property_details = property_details.find_all('span')
        property_type = property_details[0].text
        property_beds = property_details[1].text
    except:
        pass

    # Get the agent
    try:
        agent = property.find('li', {'class': AGENT_CLASS}).find('a').text
    except:
        pass

    # Get the outcome
    outcome = property.find('li', {'class': OUTCOME_CLASS})
    try:
        outcome = outcome.find_all('span')
        outcome_sold = outcome[0].text
        outcome_price = outcome[1].text
    except:
        # if fail, try to get the pass in
        outcome = property.find('li', {'class': PASSEDIN_CLASS})
        if len(outcome)>0:
            outcome_sold = "Passed in"
            outcome_price = -1

    res['suburb_name'] = suburb_name
    res['address'] = address
    res['domain_link'] = domain_link
    res['property_type'] = property_type
    res['property_beds'] = property_beds
    res['agent'] = agent
    res['outcome_sold'] = outcome_sold
    res['outcome_price'] = outcome_price

    return res


def extract_one_suburb_section(suburb):
    try:
        suburb_name = suburb.find('header', {'class': SUBURB_CLASS}).find('h3').text
    except:
        suburb_name = "Unable to extract"

    all_properties = suburb.find_all('ul', {'class': UL_CLASS})

    return suburb_name, all_properties


def extract_all_suburbs(page):
    soup = BeautifulSoup(page)

    all_suburbs = soup.find_all('article', {'class': ARTICLE_CLASS})

    return all_suburbs
