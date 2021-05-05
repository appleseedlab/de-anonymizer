#!/usr/bin/env python3
import sys
import re
import argparse
from dbf_helper import get_streets_from_dbf
from scrape_wp import search_wp, scrape_geographic
from html_parsers import parse_all_html, parse_streets
from correlate import correlate_partials

def get_candidate_addresses(partial_address, streets, maxn=12):
    # returns streets that start in partial address. use lowercase and remove punc to mitigate false negatives
    street = re.sub(r'[^\w\s]', '', partial_address)
    results = list()
    street_number = street.split(" ")[0]
    if not street_number.isnumeric():
        return []
    street_name = " ".join(street.split(" ")[1:])

    candidates = list(filter(lambda x: x.startswith(street_name.lower()), streets))
    return candidates[:maxn]



parser = argparse.ArgumentParser(
    description='An OSINT tool for de-anonymizing identities based on partial name and address tuples. e.g: (Joh,123 Ma,Orlando, FL)')
subparsers = parser.add_subparsers(help='commands')

main_parser = subparsers.add_parser('deanon', help="Run de-anonymizer")

main_parser.add_argument("-t", required=True, metavar="TARGETS",
                              dest="file", help="Comma-seperated list of anonymized identities Format: partialName,partialAddress,City,State")
main_parser.add_argument("-s", required=True, metavar="STEETS",
                              dest="streets", help="Comma-seperated list of streets for bruteforce. Format: Main St,Orlando,FL")
main_parser.add_argument("--candidates", required=False, action="store_true",
                              dest="candidates", help="Only output candidate addresses (flag)")

dbf_parser = subparsers.add_parser(
    'dbf', help='Parse a DBF file')

dbf_parser.add_argument("-f", required=True, metavar="FILE",
                              dest="file", help="A dbf file from census, may be used to generate a street list. \n https://www.census.gov/cgi-bin/geo/shapefiles/index.php")
dbf_parser.add_argument("-code", required=True, metavar="City State",
                              dest="code", help="The city and state e.g Denver CO")


# scraper_parser = subparsers.add_parser('scrape', help="Scrape public directories")
# scraper_parser.add_argument('-f', required=True, metavar="FILE",
#                               dest="file", help="List of addresses to scrape")

geo_parser = subparsers.add_parser(
    'geographic.org', help="generate candidates based on anonymized (name, address) and streets file")
geo_parser.add_argument("--state", required=True, metavar="STATE",
                              dest="state", help="US State Code (2 chars)")
geo_parser.add_argument(
    "--city", metavar="CITY", dest="city", help="outputs the list to a dictionary", required=True)



args = parser.parse_args()

try:
    vars(args)["action"] = sys.argv[1]
except IndexError as e:
    parser.print_help()
    exit()

if args.action == "dbf":
    records = get_streets_from_dbf(args.file)
    for record in records:
        print(record)

elif args.action == "candidates":
    print(f"candidates {args.streets}  {args.targets}")
    exit()
elif args.action == "scrape":
    print("ok" + str(args.file))
    exit()
elif args.action == "geographic.org":
    scrape_geographic(args.city, args.state)
    parse_streets("geographic.org/*")
    exit()
elif args.action == "deanon":
    target_file = args.file
    streets = args.streets
    suffix = None
    anonymized = list()
    searches = list()
    wp_queries = list()
    records = {}
    with open(streets, "r",) as f:
        for line in f:
            street, city, state = line.strip().lower().split(",")
            if  state not in records.keys():
                records[state] = {}
            if city not in records[state].keys():
                records[state][city] = list()
            records[state][city].append(street)
    with open(target_file, "r") as f:
        index =  0
        for line in f:
            index += 1
            try:
                pname, padd, city, state = line.strip().lower().split(",")
            except ValueError:
                print(f"Error: invalid target file. Expected 4 columns, found {len(line.strip().lower().split(','))} at line {index}")

            street_number, street_name = padd.split(" ")
            if not street_number.isnumeric(): continue
            candidates = get_candidate_addresses(padd, records[state][city])
            

            for c in candidates:
                cur_search = [street_number + " " + c, padd, pname,state,city]
                suffix = city.title() + "-" + state.upper()
                wp_query = street_number + " " + c.title() + "/" + suffix
                searches.append(cur_search)
                wp_queries.append(wp_query)
    if args.candidates:
        for search in searches:
            print(','.join(search))
        
        exit()
    for wpq in wp_queries:
        search_wp(wpq)
    addy_map = parse_all_html("html_files")
    
    de_anoned = correlate_partials(searches, addy_map)
    print("partialName,FullName,partialAddress,FullAddress,URL")
    for res in de_anoned:
        print(",".join(res))
    
    exit()

else:
    parser.print_help()
    exit()
