import json
import sys



def correlate_partials(searches, addy_map):
    addys = list()
    results = list()
    used = set()
    count = 0
    for search in searches:
            full_addy, partial_addy, partial_name, state, city = search
            _id = f"{partial_name},{partial_addy}"
            if _id in used: continue
            if full_addy in addy_map.keys():
                for full_name in addy_map[full_addy]:
                    if full_name.lower().startswith(partial_name):
                        count += 1
                        used.add(_id)
                        address = full_addy.title().replace(" ", "-")
                        result = [partial_name, full_name, partial_addy, full_addy.title(),city.title(),state.upper(), f"https://www.whitepages.com/address/{address}/{city.title()}-{state.upper()}"]
                        results.append(result)
    return results
                       


if __name__ == "__main__":
    if(len(sys.argv) != 4 ):
        print("usage:")
        print("proc_wp map.json search.csv City-ST")
        print("map.json format: {\"123 main\": [name, name, ...]}")
        print("search.csv format address, name, address prefix")
        exit()
    fp = open(sys.argv[1])
    searches = list*()
    search = sys.argv[2]

    with open(search, "r") as fp:
        for line in fp:
            full_addy = line.strip().split(",")[0]
            partial_name = line.split(",")[1].strip().lower()
            partial_addy = line.split(",")[2].strip().lower()
            searches.append([full_addy, partial_name, partial_addy])
    city_state = sys.argv[3]
    addy_map = json.load(fp)
    fp.close()
    results = correlate_partials(searches, addy_map, city_state)
    for result in results:
         print(",".join(result))