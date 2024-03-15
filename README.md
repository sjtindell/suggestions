# Getting Started

### Suggestions App
The goal of this app is to serve an API endpoint that provides autocomplete suggestions for large cities.

### Examples
Search for a city using its name.

```
curl "http://127.0.0.1:5000/suggestions?q=London"
```

and add on the Latitude/Longitude to search closer to a particular location

```
curl "http://127.0.0.1:5000/suggestions?q=London&latitude=43.70011&longitude=-79.4163"
```

or test the current remote instance at 

```
curl -v "http://35.86.250.20/suggestions?q=London"
```

## Development

### Install dependencies

Tested using Python 3.10.6

```
python --version
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

then start the webserver for debug

```
python run.py
```

or for production

```
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

### Run the tests
In another terminal

```
source venv/bin/activate
python -m unittest discover tests
```

### Build for Docker

```
docker build -t suggestions .
```

## Deployment
To deploy to AWS Lightsail, configure your aws config and credentials files for your aws account. Then

```
cd deployment
terraform init
terraform plan
terraform apply
```

Your instance is now reachable at its public IP. For example we are running a test instance at

```
curl -v "http://35.86.250.20/suggestions?q=London"
```

When you are done, tear it down

```
cd deployment
terraform destroy
```

## Tables

The main `geoname` table from [geonames.org](https://download.geonames.org/export/dump/) has the following fields :

```
geonameid         : integer id of record in geonames database
name              : name of geographical point (utf8) varchar(200)
asciiname         : name of geographical point in plain ascii characters, varchar(200)
alternatenames    : alternatenames, comma separated varchar(5000)
latitude          : latitude in decimal degrees (wgs84)
longitude         : longitude in decimal degrees (wgs84)
feature class     : see http://www.geonames.org/export/codes.html, char(1)
feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
country code      : ISO-3166 2-letter country code, 2 characters
cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display
                    names of this code; varchar(20)
admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
admin3 code       : code for third level administrative division, varchar(20)
admin4 code       : code for fourth level administrative division, varchar(20)
population        : bigint (8 byte int)
elevation         : in meters, integer
dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30''
                    (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
timezone          : the timezone id (see file timeZone.txt) varchar(40)
modification date : date of last modification in yyyy-MM-dd format
```

todo: generate our tsv table markdown example to stash here

