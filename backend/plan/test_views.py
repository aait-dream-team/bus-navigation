from django.views import View
from django.http import response
from . import gtfs_rt_pb2 as gg

class TestView(View):
    def get(self, request):
        data = gg.FeedMessage()
        header = data.header      
        header.gtfs_realtime_version = "2.0"
        entity = data.entity.add()
        entity.id = "0"
        alert = entity.alert
        entity_sel = alert.informed_entity.add()
        entity_sel.route_id = "1:10460407"   
        entity_sel_2 = alert.informed_entity.add()
        entity_sel_2.agency_id = "AA"     
        alert.cause = gg.Alert.Cause.STRIKE
        alert.effect = gg.Alert.Effect.REDUCED_SERVICE
        active = alert.active_period.add()
        active.start = 1658283241          
        active.end = 1686956849
        h = alert.header_text
        trans = h.translation.add()
        trans.text = "This is a Test Alert"
        trans.language = "en" 

        # This shows a report for the agency at http://localhost:8082/otp/routers/default/index/agencies/1/AA/alerts
        # and for the route at http://localhost:8082/otp/routers/default/index/routes/1:1:10460407/alerts
        return response.HttpResponse(data.SerializeToString(), content_type="application/protobuf")