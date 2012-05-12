Raw data, scripts and viz for [San Francisco Crime
Dataset](http://datahub.io/dataset/crime-data-sf). 


## Run the queries

Find incidents with {distance} miles of 9th and Mission ({distance} is optional
and will default to 0.5 miles):

    python process.py {distance}

Output will be total and first 2 results.


## Load Data into the DataHub

Run the script:

    python process.py load

