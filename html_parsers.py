import glob, os
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import sys

def ts():
  curr = datetime.now()
  curr = curr.strftime("%d_%H:%M")
  return f"{curr}"

def ws_punc(s):
  return re.sub(r'[^\w\s]',' ',s)

def rm_punc(s):
  return re.sub(r'[^\w\s]', '', s)
  
  
def parse_streets(html_dir):
    files = glob.glob(html_dir)
    for file in files:
        basename = os.path.basename(file)
        city, state = basename.split("-")

        with open(file) as f:
            s = f.read()
            from bs4 import BeautifulSoup
            import json
            html = s

            soup = BeautifulSoup(html, features="html5lib")
            for li_tag in soup.find_all('ul'):
                
                for span_tag in li_tag.find_all('li'):
                    try:
                        field = span_tag.text
                        print(f"{field},{city},{state}")
                    except AttributeError:
                        continue

def parse_all_html(html_dir):
    names = set()
    all_names = list()
    addy_map = {}

    count = 0
    for file in glob.glob(html_dir + "/*.html"):
        s = ""
        with open(file) as f:
            s = f.read()
            if "Sorry, we couldn't find that address. Please confirm" in s:
                continue
            if "You're sending requests a bit too fast!" in s:
                continue
            basename = os.path.basename(file)
            fname = basename.split("-")[0]
            html = s
            count += 1
            soup = BeautifulSoup(html, "html5lib")
            names = set()
            resi = soup.find("div", {"id": "residents"})
            if not resi: continue
            for div in resi.find_all("div"):
                search_res = div.text.strip()
                rr = search_res.split()
                _j = " ".join(rr)
                # names_ = get_names(_j)
                # for n in names_:
                #     names.add(n.replace(" Age", "" ))

            links= soup.find_all('script')
            for script in links:
                if '@type":"ItemList"' in script.text:
                    jsonStr = script.string
                    jsonObj = json.loads(jsonStr)
                    try:
                        list_ = jsonObj['itemListElement']
                        for e in list_:
                            person_name = e['item']['name']
                            names.add(person_name)
                            
                    except:
                        pass
        addy_map[ws_punc(fname).lower().strip()] = list(names)
    return addy_map
if __name__ == "__main__":
    if(len(sys.argv) != 2 ):
        print("usage:")
        print("parse_wp path/to/dir/")
        print("dir must have html files from whitepages")
        exit()
    results = parse_all_html(sys.argv[1])
    out = ts() + ".json"
    with open(out, "w") as f:
        json.dump(results, f)
    print(os.getcwd() + "/" + out, end="")