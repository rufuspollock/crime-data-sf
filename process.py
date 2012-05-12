'''Load data and demonstrate how to do geospatial queries.
'''
import logging
import json
import urllib
import urllib2

logging.basicConfig(level=logging.DEBUG)

# URL to Data API for this data resource on DataHub.io
datastore_url = 'http://datahub.io/api/data/897c3131-ff48-4281-ae0d-f65b6f3f9fe2'
# If you have ElasticSearch installed you could also run this against a local
# ES instance for testing or working offline
# datastore_url = 'http://localhost:9200/tmp/sfpd-last-month'

def load():
    # Use CKAN DataStore client library https://github.com/okfn/datastore-client
    # This is just for convenience (e.g. it does bulk inserting for us)
    # Data API is RESTful so really easy to do this by hand
    import datastore.client as c
    client = c.DataStoreClient(datastore_url)

    # specify that location field is of geo point type
    mapping = {
        'properties': {
            'Location': {
                'type': 'geo_point'
                }
        }
    }
    client.delete()
    client.mapping_update(mapping)
    client.upload('data/sfpd_incidents_march_2012.tidied.csv', refresh=True)

# this is exactly the same as DataStoreClient.query
# inlining to reduce dependencies and show how simple this is
def _query(query):
    url = datastore_url + '/_search'
    q = json.dumps(query)
    url += '?source=' + urllib.quote(q)
    req = urllib2.Request(url)
    out = urllib2.urlopen(req).read()
    return json.loads(out)

def queryall():
    query = {
        "query" : {
            "match_all" : {}
        }
    }
    out = _query(query)
    print('Total number of incidents: %s' % out['hits']['total'])

def geoquery(distance):
    distance = '%smiles' % distance
    query = {
        "query": {
            "filtered": {
                "query" : {
                    "match_all" : {}
                },
                "filter" : {
                    "geo_distance" : {
                        "distance" : distance,
                        "Location" : {
                            # 9th and Mission
                            "lat": "37.776",
                            "lon": "-122.415"
                        }
                    }
                }
            }
        }
    }
    out = _query(query)
    print('Total number of incidents within %s of 9th and Mission: %s' %
            (distance, out['hits']['total']))
    for result in out['hits']['hits'][:2]:
        print result['_source']


if __name__ == '__main__':
    import sys
    arg = ''
    if len(sys.argv) >= 2:
        arg = sys.argv[1]

    if arg == 'load':
        load()
    else:
        if not arg:
            arg = 0.5
        queryall()
        geoquery(arg)

