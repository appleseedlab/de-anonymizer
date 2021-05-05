

import re
import sys
from dbf_helper import get_streets_from_dbf
from scrape_wp import search_wp
from parse_wp import parse_all_html
from proc_wp import correlate_partials


def get_candidate_addresses(partial_address, streets):
    # returns streets that start in partial address. use lowercase and remove punc to mitigate false negatives
    street = re.sub(r'[^\w\s]', '', partial_address)
    results = list()
    street_number = street.split(" ")[0]
    if not street_number.isnumeric():
        return []
    street_name = " ".join(street.split(" ")[1:])

    candidates = list(filter(lambda x: x.startswith(street_name.lower()), streets))
    return candidates

if __name__ == '__main__':
    if(len(sys.argv) != 4 ):
        print("usage:")
        print("main.py anon.csv streets.dbf city-state")
        exit()
    searches = list()
    anonymized = sys.argv[1]
    white_pages_quereies = list()
    city_state = sys.argv[3]
    records = get_streets_from_dbf(sys.argv[2])
    
    with open(anonymized) as fp:
        for line in fp:
            partial_name = line.split(",")[0].strip().lower()
            partial_addy = line.split(",")[1].strip().lower()
            street_number = partial_addy.split(" ")[0]
            if not street_number.isnumeric(): continue
            candidates = get_candidate_addresses(partial_addy, records)
            for c in candidates:
                cur_search = [street_number + " " + c, partial_addy, partial_name]
                wp_query = street_number + " " + c.title() + "/" + city_state
                searches.append(cur_search)
                white_pages_quereies.append(wp_query)

    for wpq in white_pages_quereies:
        search_wp(wpq)
    addy_map = parse_all_html()
    de_anoned = correlate_partials(searches, addy_map, city_state)
    
    for res in de_anoned:
        print(res)