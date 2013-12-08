import csv
import sys
import json
import os
import urllib2
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError

ES_HOSTS = [{"host":'localhost', "port": 9200}]
ES_INDEX = 'monstercat'

es = Elasticsearch(ES_HOSTS)

# Read the testdata
filehandle = open('testdata.csv', 'rb')
csvreader = csv.reader(filehandle)

# Split headers from the rest of the data
headers = csvreader.next()

# Parse rows and post them to es
for csvindex, row in enumerate(csvreader):
    column = {}
    for index, header in enumerate(headers):
        if len(row[index]) == 0:
            row[index] = 0

        column[header] = row[index]


    # Send data to elasticsearch API
    try:
        print "[%d] Sending to ES index '%s'" % (csvindex, column['saleType'])
        es.index(index=ES_INDEX, doc_type=column['saleType'], body=json.dumps(column))
    except TransportError:
        print 'Exception occured in row [%d]' % csvindex
