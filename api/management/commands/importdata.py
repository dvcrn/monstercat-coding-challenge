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

    def get_and_check(self, dictionary, name):
        try:
            return dictionary[name]
        except KeyError:
            return False

    def create_or_get_album(self, album_name):
        album = self.get_and_check(self.albums_list, album_name)
        if album is not False:
            return album

        album = Album(name=album_name)
        album.save()

        self.albums_list[album_name] = album

        return album

    def create_or_get_track_type(self, type_name):
        ttype = self.get_and_check(self.track_type_list, type_name)
        if ttype is not False:
            return ttype

        ttype = TrackType(name=type_name)
        ttype.save()

        self.track_type_list[type_name] = ttype

        return ttype

    def create_or_get_song(self, song_name, artist, album, song_type):
        if song_type is 'Track':
            song_list = self.single_track_list
        else:
            song_list = self.album_track_list

        song = self.get_and_check(song_list, song_name)
        if song is not False:
            return song

        ttype = self.create_or_get_track_type(song_type)
        track = Track(name=song_name, album=album, artist=artist, track_type=ttype)
        track.save()

        song_list[song_name] = track

        return track

    def create_or_get_artist(self, artist_name):
        artist = self.get_and_check(self.artist_list, artist_name)
        if artist is not False:
            return artist

        artist = Artist(name=artist_name)
        artist.save()

        self.artist_list[artist_name] = artist

        return artist

    def create_or_get_store(self, store_name):
        store = self.get_and_check(self.store_list, store_name)
        if store is not False:
            return store

        store = Store(name=store_name)
        store.save()

        self.store_list[store_name] = store

        return store

    def create_or_get_costumer(self, costumer_name):
        if not costumer_name:
            return None

        costumer = self.get_and_check(self.costumer_list, costumer_name)
        if costumer is not False:
            return costumer

        costumer = Costumer(name=costumer_name)
        costumer.save()

        self.costumer_list[costumer_name] = costumer

        return costumer

    def create_or_get_sale_type(self, type_name):
        stype = self.get_and_check(self.sale_type_list, type_name)
        if stype is not False:
            return stype

        stype = SaleType(name=type_name)
        stype.save()

        self.sale_type_list[type_name] = stype

        return stype

    def create_or_get_sale_period(self, period_date):
        speriod = self.get_and_check(self.sale_type_list, period_date)
        if speriod is not False:
            return speriod

        speriod = SalePeriod(date=period_date)
        speriod.save()

        self.sale_type_list[period_date] = speriod

        return speriod


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

