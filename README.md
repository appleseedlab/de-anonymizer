# de-anonymizer

This tool assists with automating discovering the true identities of people by using publicly available data.

It uses partial (name,address) tuples and attempts to unmask them.

## Requirements:

Beautiful Soup 4 and requests

`pip install beautifulsoup4 requests`

## Set-up:

You need:

1. A CSV file with the people you wish to de-anonymize. This file should have the following columns: `partialName,partialAddress,City,State`

	```

	josep,720 Gree,Wilmington,DE
	ron,700 Ad,Tallahassee,FL

	```
2. A CSV file with the addresses you wish to search over. This file should have the following columns: `streetName,City,State`

	    Alan-a-dale Trail,Tallahassee,FL
	    Alanthus Ct,Tallahassee,FL
	    Alban Ave,Tallahassee,FL
	    Greenbriar Dr,Wilmington,DE
	    Greendale Rd,Wilmington,DE


5. You can generate a list for a city using data from geographic.org with: `deanon.py geographic.org --state FL --city Orlando`.

6. You can also obtain a list of all the roads in a county from the Census Bureau at: https://www.census.gov/cgi-bin/geo/shapefiles/index.php. After downloading the roads shape-file, you can parse using `deanon.py dbf -f file.dbf -code Orlando-FL`

  

# Usage:

  

1. de-anonymize: `deanon.py deanon -t examples/targets -s examples/streets`
    1. output: 
        ```
        partialName,FullName,partialAddress,FullAddress,URL
        joseph,Joseph R Biden,720 gree,720 Greenhill Ave,Wilmington,DE,https://www.whitepages.com/address/720-Greenhill-Ave/Wilmington-DE
        ron,Ronald Desantis,700 ad,700 Adams St,Tallahassee,FL,https://www.whitepages.com/address/700-Adams-St/Tallahassee-FL
        ```
    2. If you have an account with scraperapi.com, you can pass your API key in with `-scraper-api-key xxx`. This will help mitigate 403s and 401s.
2. Help: `deanon.py --help`

3. Modules: most of the source files can be ran as stand-alone scripts. See the usage prompt after running as main for details.