from django.http import JsonResponse
from django.views import View
import requests

class UserView(View):
    def get(self, request):
        if "fromPlace" not in request.GET or "toPlace" not in request.GET or "time" not in request.GET or "date" not in request.GET or "mode" not in request.GET or "arriveBy" not in request.GET:
            return JsonResponse({'error': 'Missing required parameter'}, status=400)

        fromPlace = request.GET.get('fromPlace')
        toPlace = request.GET.get('toPlace')
        time = request.GET.get('time')
        date = request.GET.get('date')
        mode = request.GET.get('mode')
        arriveBy = request.GET.get('arriveBy')
        wheelchair = request.GET.get('wheelchair')
        showIntermediateStops = request.GET.get('showIntermediateStops')
        debugItineraryFilter = request.GET.get('debugItineraryFilter')
        locale = request.GET.get('locale')

        payload = {
            'fromPlace' : fromPlace,
            'toPlace' : toPlace,
            'time' : time,
            'date' : date,
            'mode' : mode,
            'arriveBy' : arriveBy,
            'wheelchair' : wheelchair,
            'showIntermediateStops' : showIntermediateStops,
            'debugItineraryFilter' : debugItineraryFilter,
            'locale' : locale
        }
        
        headers = {"Content-Type": "application/json"}

        r = requests.get("http://bus-navigation-otp-1:8080/otp/routers/default/plan", params=payload, headers=headers)

        return JsonResponse(r.json())