from django.db import models

# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __unicode__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=60)
    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'

    def __unicode__(self):
        return self.name


class TrackType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    class Meta:
        verbose_name = 'TrackType'
        verbose_name_plural = 'TrackTypes'

    def __unicode__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=200)
    album = models.ForeignKey(Album)
    artist = models.ForeignKey(Artist)
    track_type = models.ForeignKey(TrackType)

    class Meta:
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'

    def __unicode__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=200)
    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __unicode__(self):
        return self.name


class Costumer(models.Model):
    name = models.CharField(max_length=200)
    class Meta:
        verbose_name = 'Costumer'
        verbose_name_plural = 'Costumers'

    def __unicode__(self):
        return self.name

class SaleType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    class Meta:
        verbose_name = 'SaleType'
        verbose_name_plural = 'SaleTypes'

    def __unicode__(self):
        return self.name

class SalePeriod(models.Model):
    date = models.DateField()
    class Meta:
        verbose_name = 'SalePeriod'
        verbose_name_plural = 'SalePeriods'

    def __unicode__(self):
        return unicode(self.date)

class Sale(models.Model):
    txId = models.CharField(max_length=200, blank=True, null=True, unique=True)
    soldOn = models.DateTimeField(blank=True, null=True)
    salePeriod = models.ForeignKey(SalePeriod)
    saleType = models.ForeignKey(SaleType)
    store = models.ForeignKey(Store)
    costumer = models.ForeignKey(Costumer, blank=True, null=True)
    track = models.ForeignKey(Track)
    sales = models.IntegerField()

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def __unicode__(self):
        return self.txId
