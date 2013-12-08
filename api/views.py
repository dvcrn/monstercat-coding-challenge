from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from models import *
import json
import time

# Create your views here.

class GenericApiView(ListView):
    queryset = Sale.objects.all()
    ttype = None
    stype = None

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch
        :param request: Request
        :type request: HttpRequest
        """

        return super(GenericApiView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = {}
        sale_periods = SalePeriod.objects.all().distinct()

        for period in sale_periods:
            if self.stype is not None:
                self.queryset = self.queryset.filter(saleType=self.stype)

            if self.ttype is not None:
                self.queryset = self.queryset.filter(track__track_type=self.ttype)

            count = self.queryset.filter(salePeriod=period).count()

            # Using timestamps as keys
            data[int(time.mktime(period.date.timetuple()))] = count

        response = HttpResponse(json.dumps(data))
        response['Content-Type'] = 'application/json'
        return response


class AlbumsApiView(GenericApiView):
    queryset = Sale.objects.all()
    ttype = TrackType.objects.get(name='AlbumTrack')
    stype = None


class SinglesApiView(GenericApiView):
    queryset = Sale.objects.all()
    ttype = TrackType.objects.get(name='Track')
    stype = None


class StreamingApiView(GenericApiView):
    queryset = Sale.objects.all()
    ttype = None
    stype = SaleType.objects.get(name='Streaming')

