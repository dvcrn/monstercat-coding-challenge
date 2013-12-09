from django.core.management.base import BaseCommand, make_option
from datetime import datetime, timedelta
from api.models import *
import csv
import sys
from datetime import datetime

class Command(BaseCommand):
    help = "Imports test data"

    albums_list = {}
    album_track_list = {}
    single_track_list = {}
    artist_list = {}
    track_type_list = {}
    store_list = {}
    costumer_list = {}
    sale_type_list = {}
    sale_period_list = {}

    def get_and_check(self, dictionary, name, obj):
        try:
            return dictionary[name]
        except KeyError:
            obj.save()
            dictionary[name] = obj
            return obj

    def create_or_get_album(self, album_name):
        return self.get_and_check(self.albums_list, album_name, Album(name=album_name))

    def create_or_get_track_type(self, type_name):
        return self.get_and_check(self.track_type_list, type_name, TrackType(name=type_name))

    def create_or_get_song(self, song_name, artist, album, song_type):
        if song_type is 'Track':
            song_list = self.single_track_list
        else:
            song_list = self.album_track_list

        ttype = self.create_or_get_track_type(song_type)
        return self.get_and_check(song_list, song_name, Track(name=song_name, album=album, artist=artist, track_type=ttype))

    def create_or_get_artist(self, artist_name):
        return self.get_and_check(self.artist_list, artist_name, Artist(name=artist_name))

    def create_or_get_store(self, store_name):
        return self.get_and_check(self.store_list, store_name, Store(name=store_name))

    def create_or_get_costumer(self, costumer_name):
        if not costumer_name:
            return None

        return self.get_and_check(self.costumer_list, costumer_name, Costumer(name=costumer_name))

    def create_or_get_sale_type(self, type_name):
        return self.get_and_check(self.sale_type_list, type_name, SaleType(name=type_name))

    def create_or_get_sale_period(self, period_date):
        return self.get_and_check(self.sale_type_list, period_date, SalePeriod(date=period_date))


    def handle(self, *args, **options):
        path = args[0]
        print path

        filehandle = open(path, 'rb')
        csvreader = csv.reader(filehandle)

        # Split headers from the rest of the data
        headers = csvreader.next()

        # Parse rows
        for csvindex, row in enumerate(csvreader):
            print 'Parsing %s' % csvindex

            column = {}
            for index, header in enumerate(headers):
                column[header] = row[index]

            print column
            album = self.create_or_get_album(column['album'])
            artist = self.create_or_get_artist(column['artist'])
            song = self.create_or_get_song(column['title'], artist, album, column['itemType'])

            store = self.create_or_get_store(column['store'])
            costumer = self.create_or_get_costumer(column['buyer'])
            sale_type = self.create_or_get_sale_type(column['saleType'])

            if not column['salePeriod']:
                sale_period = None
            else:
                sale_period = datetime.strptime(column['salePeriod'], '%Y-%m-%dT%H:%M:%SZ').date()

            sale_period = self.create_or_get_sale_period(sale_period)

            if not column['soldOn']:
                sold_on = None
            else:
                sold_on = datetime.strptime(column['soldOn'], '%Y-%m-%dT%H:%M:%SZ').date()

            sale = Sale(txId=column['txId'], soldOn=sold_on, salePeriod=sale_period,
                saleType=sale_type, store=store, costumer=costumer, sales=int(column['sales']), track=song)
            sale.save()

