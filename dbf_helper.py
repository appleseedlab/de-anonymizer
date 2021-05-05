from dbfread import DBF
import sys

def get_streets_from_dbf(dbf_file):
    records = list()
    for record in DBF(dbf_file, encoding="UTF-8"):
            r = record['FULLNAME']
            if len(r) > 2:
                records.append(r.lower())
    return records

if __name__ == '__main__':
    if(len(sys.argv) != 2 ):
        print("usage:")
        print("dbf_helper.py file.dbf")
        exit()
    records = get_streets_from_dbf(sys.argv[1])
    for record in records:
        print(record)