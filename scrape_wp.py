from multiprocessing import Pool
import requests
import time
from os import path
import sys
import os
from requests.exceptions import ReadTimeout

payload={}
headers = {}


def scrape_geographic(city, state, scraper_key=""):
    url = f"https://geographic.org/streetview/usa/{state.lower()}/{city.lower()}.html"
    out_dir = "geographic.org"
    os.makedirs(out_dir, exist_ok=True)
    output_file = f"{city.lower()}-{state.lower()}"
    res = requests.request("GET", url, headers=headers, data=payload, timeout=0.5)
    if res.status_code != 200:
        print("FAILURE::{0}".format(url),file=sys.stderr)
        #suffx = ".fail"
    data = res.text

    with open( out_dir + "/" + output_file, "w") as f:
        f.write(data)

def search_wp(search,scraper_key=""):
    
    suffx = ".html"
    street = search[: search.index("/")]
    city_state = search[search.index("/") + 1 :]
    out_dir = "html_files"
    os.makedirs(out_dir,exist_ok=True)
    search = search.replace(" ", "-")
    output_file = street + f" - {city_state}"

    wp_url = f"https://www.whitepages.com/address/{search.strip()}"
    if len(scraper_key) > 0:
        url = f"http://api.scraperapi.com/?api_key={scraper_key}&url={wp_url}"
    else:
        url = wp_url
    print("Fetching " + url, file=sys.stderr)
    try:
        res = requests.request("GET", url, headers=headers, data=payload, timeout=10)
    except ReadTimeout:
        return
    if res.status_code != 200:
        print(f"HTTP ERROR (code {res.status_code})::{url}",file=sys.stderr)
        suffx = ".f3"
    data = res.text
    response =  {
            'html': data,
            'q': search

        }
    if "You're sending requests a bit too fast!" in data:
        suffx = ".f1"
    if "Sorry, we couldn't find that address." in data:
        suffx = ".f2"
    q = response['q']
    street = q[:q.index("/")]
    with open( out_dir + "/" + output_file + suffx, "w") as f:
        f.write(response['html'])

if __name__ == '__main__':
    if(len(sys.argv) != 4 ):
        print("usage:")
        print("whitepages.py search.csv city")
        print("search.csv 100-Windmill-Trl/Dallas-TX")
        exit()

    searchs_to_fetch = list()

    with open(sys.argv[1], "r") as f:
        for line in f:
            temp = line.strip()
            searchs_to_fetch.append(temp)
    city = sys.argv[2]

    if not os.path.exists(city): # make a dedicated dir for addresses from that city
        os.makedirs(city) 
    os.chdir(city)
    with Pool(4) as p:
        p.map(search_wp, searchs_to_fetch)