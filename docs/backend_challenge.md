Challenge #1
Design an API endpoint that provides autocomplete suggestions for large cities.
The suggestions should be restricted to cities in the USA and Canada with a population
above 5000 people.
- the endpoint is exposed at `/suggestions`
- the partial (or complete) search term is passed as a query string parameter `q`
- the callers location can optionally be supplied via query string parameters `latitude`
and `longitude` to help improve relative scores
- the endpoint returns a JSON response with an array of scored suggested matches
- the suggestions are sorted by descending score
- each suggestion has a score between 0 and 1 (inclusive) indicating confidence in
the suggestion (1 is most confident)
- each suggestion has a name which can be used to disambiguate between similarly
named locations
- each suggestion has a latitude and longitude
- all functional tests should pass (additional tests may be implemented as necessary).
#### Sample responses
These responses are meant to provide guidance. The exact values can vary based on
the data source and scoring algorithm.
**Near match**
GET /suggestions?q=London;latitude=43.70011;longitude=-79.4163
```json
{
suggestions: [
{
name: London, ON, Canada,
latitude: 42.98339,
longitude: -81.23304,
score: 0.9
},
{
name: London, OH, USA,
latitude: 39.88645,
longitude: -83.44825,
score: 0.5
},
{
name: London, KY, USA,

latitude: 37.12898,
longitude: -84.08326,
score: 0.5
},
{
name: Londontowne, MD, USA,
latitude: 38.93345,
longitude: -76.54941,
score: 0.3
}
]
}
```
**No match**
GET /suggestions?q=SomeRandomCityInTheMiddleOfNowhere
```json
{
suggestions: []
}
```

### Non-functional
- Mitigations to handle high levels of traffic should be implemented.
- Challenge is submitted with all the necessary files (code, scripts, dataset, readme,
etc.) in a .zip folder
- Documentation and maintainability is a plus.
## Dataset
You can find the necessary dataset along with its description in the files attached.
Data - cities_canada-usa.tsv
Description – README.md

## Evaluation
We will use the following criteria to evaluate your solution:
- Capacity to follow instructions
- Developer Experience (how easy it is to run your solution locally, how clear your
documentation is, etc.)
- Solution correctness
- Performance
- Tests (quality and coverage)
- Code style and cleanliness
- Attention to detail
- Ability to make sensible assumptions

it should produce an output similar to:
```
Server running at http://127.0.0.1:2345/suggestions
```
## Deployment (Optional):
Deploy the above application and share the hosted URL with Buzz.

Challenge #2:
Write a query/program to scrape images from Google Images for the label specified and
the number of images to be scrapped and downloaded specified.

Inputs: 
1. Label of the type of images to be scrapped (example power lines, dogs, cats, etc.).
Also, the label string should have the capability of having multiple words (for example,
power line or cats)
2. Number of images to be scraped and downloaded onto the local machine

The program should be able to scrap the images and store those images in a folder (on
our local machine) with the name of the label (example if we are scraping images of
;dogs; then the label is ;dogs; and hence the folder where all the scraped images should
be download should also be named ;dogs;).

Points would be awarded on coding style, commenting and documentation of executing
the program.
