from django.views import View
from django.http import response
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework import permissions
from updater import gtfs_rt_pb2 as pb
@authentication_classes([])
@permission_classes([permissions.AllowAny])
class TestView(View):
    def get(self, request):
        # data = pb.FeedMessage()
        data = pb.FeedMessage()
        header = data.header      
        header.gtfs_realtime_version = "2.0"
        entity = data.entity.add()
        entity.id = "0"
        trip_update = entity.trip_update
        trip_descriptor = trip_update.trip
        trip_descriptor.trip_id = "1:10460407"
        trip_descriptor.start_time = "14:05:00"
        trip_descriptor.start_date = "20220628"
        trip_descriptor.schedule_relationship = pb.TripDescriptor.ScheduleRelationship.CANCELED
        # trip_descriptor.route_id = "1:10460407"
        # trip_descriptor.direction_id = 0


        # alert = entity.alert
        # entity_sel = alert.informed_entity.add()
        # entity_sel.route_id = "1:10460407"   
        # entity_sel_2 = alert.informed_entity.add()
        # entity_sel_2.agency_id = "AA"     
        # alert.cause = gg.Alert.Cause.STRIKE
        # alert.effect = gg.Alert.Effect.REDUCED_SERVICE
        # active = alert.active_period.add()
        # active.start = 1658283241          
        # active.end = 1686956849
        # h = alert.header_text
        # trans = h.translation.add()
        # trans.text = "This is a Test Alert"
        # trans.language = "en" 

        # This shows a report for the agency at http://localhost:8082/otp/routers/default/index/agencies/1/AA/alerts
        # and for the route at http://localhost:8082/otp/routers/default/index/routes/1:1:10460407/alerts
        return response.HttpResponse(data.SerializeToString(), content_type="application/protobuf")