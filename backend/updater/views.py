from collections import defaultdict

from django.views import View
from django.http import response
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
import time
from datetime import datetime
from rest_framework.decorators import api_view, authentication_classes,permission_classes

from .serializer import AlertSerializer, VehicleUpdateSerializer
from utils.common_permissions import IsOwner, IsSystemAdmin
from .models import Alert, VehicleUpdate, TripUpdate
from . import   gtfs_rt_pb2 as gg
from .serializer import AlertSerializer, TripUpdateSerializer
from django.shortcuts import get_object_or_404

cause_mapping = list({
    "UNKNOWN_CAUSE": gg.Alert.Cause.UNKNOWN_CAUSE,
    "OTHER_CAUSE": gg.Alert.Cause.OTHER_CAUSE,
    "TECHNICAL_PROBLEM": gg.Alert.Cause.TECHNICAL_PROBLEM,
    "STRIKE": gg.Alert.Cause.STRIKE,
    "DEMONSTRATION": gg.Alert.Cause.DEMONSTRATION,
    "ACCIDENT": gg.Alert.Cause.ACCIDENT,
    "HOLIDAY": gg.Alert.Cause.HOLIDAY,
    "WEATHER": gg.Alert.Cause.WEATHER,
    "MAINTENANCE": gg.Alert.Cause.MAINTENANCE,
    "CONSTRUCTION": gg.Alert.Cause.CONSTRUCTION,
    "POLICE_ACTIVITY": gg.Alert.Cause.POLICE_ACTIVITY,
    "MEDICAL_EMERGENCY": gg.Alert.Cause.MEDICAL_EMERGENCY,
}.values())
effect_mapping = list({
    "NO_SERVICE": gg.Alert.Effect.NO_SERVICE,
    "REDUCED_SERVICE": gg.Alert.Effect.REDUCED_SERVICE,
    "SIGNIFICANT_DELAYS": gg.Alert.Effect.SIGNIFICANT_DELAYS,
    "DETOUR": gg.Alert.Effect.DETOUR,
    "ADDITIONAL_SERVICE": gg.Alert.Effect.ADDITIONAL_SERVICE,
    "MODIFIED_SERVICE": gg.Alert.Effect.MODIFIED_SERVICE,
    "OTHER_EFFECT": gg.Alert.Effect.OTHER_EFFECT,
    "UNKNOWN_EFFECT": gg.Alert.Effect.UNKNOWN_EFFECT,
    "STOP_MOVED": gg.Alert.Effect.STOP_MOVED,
}.values())


@authentication_classes([])
@permission_classes([permissions.AllowAny])
class TripUpdateViewSet(viewsets.ModelViewSet):
    queryset = TripUpdate.objects.all()
    serializer_class = TripUpdateSerializer
    
    def list(self, request, *args, **kwargs):
        trip_updates = TripUpdate.objects.all()
        trips_updated = defaultdict(list)
        for trip_update in trip_updates:
            trips_updated[trip_update.trip_id.id].append(trip_update)
        data = gg.FeedMessage()
        header = data.header
        header.gtfs_realtime_version = "2.0"
        for trip_id, current_trip_updates in trips_updated.items():
            entity = data.entity.add()

            entity.id = str(current_trip_updates[0].trip_update_feed_id)
            trip_update = entity.trip_update
            trip = trip_update.trip
            # TripDescriptor
            trip.trip_id = trip_id 
            for update in current_trip_updates:
                stop_time_update = trip_update.stop_time_update.add()
                # StopTimeUpdate
                stop_time_update.stop_id = update.stop_time_id.stop.id 
                stop_time_update.stop_sequence = update.stop_time_id.stop_sequence
                arrival = stop_time_update.arrival
                # StopTimeEvent arrival
                arrival.delay = update.delay.seconds
                departure = stop_time_update.departure
                departure.delay = update.delay.seconds # seconds
            trip_update.timestamp = int(max(update.trip_update_timestamp.timestamp() for update in current_trip_updates)) # update_timestamp 
        # This shows a report for the agency at http://localhost:8082/otp/routers/default/index/agencies/1/AA/alerts
        # and for the route at http://localhost:8082/otp/routers/default/index/routes/1:1:10460407/alerts
        return response.HttpResponse(data.SerializeToString(), content_type="application/protobuf")


@authentication_classes([])
@permission_classes([permissions.AllowAny])
class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    
    def get(self, request, *args, **kwargs):
        querySet = Alert.objects.all()
        data = gg.FeedMessage()
        header = data.header      
        header.timestamp = int(time.time())
        header.gtfs_realtime_version = "2.0"
        for q_alert in querySet:
            entity = data.entity.add()
            entity.id = str(q_alert.alert_feed_id)
            alert = entity.alert
            entity_sel = alert.informed_entity.add()
            if q_alert.affected_entity == "route":
                entity_sel.route_id = str(q_alert.route_id)
            # entity_sel.route_id = "1:10460407"   
            entity_sel_2 = alert.informed_entity.add()
            if q_alert.affected_entity == "agency":
                entity_sel_2.agency_id = str(q_alert.agency_id)
            alert.cause = cause_mapping[q_alert.cause]
            alert.effect = effect_mapping[q_alert.effect]
            active = alert.active_period.add()
            active.start = datetime.timestamp(q_alert.start_timestamp)   
            active.end =  datetime.timestamp(q_alert.start_timestamp)  + q_alert.duration
            h = alert.header_text
            trans = h.translation.add()
            trans.text = q_alert.message
            trans.language = "en" 
        return response.HttpResponse(data.SerializeToString(), content_type="application/protobuf")

    def list(self, request, *args, **kwargs):
        querySet = Alert.objects.all()
        data = gg.FeedMessage()
        header = data.header      
        header.gtfs_realtime_version = "2.0"
        header.timestamp = int(time.time())
        for q_alert in querySet:
            entity = data.entity.add()
            entity.id = str(q_alert.alert_feed_id)
            alert = entity.alert
            if q_alert.affected_entity == "route":
                entity_sel = alert.informed_entity.add()
                entity_sel.route_id = str(q_alert.route_id.id)
            if q_alert.affected_entity == "agency":
                entity_sel_2 = alert.informed_entity.add()
                entity_sel_2.agency_id = str(q_alert.agency_id.id)
            alert.cause = cause_mapping[q_alert.cause]
            alert.effect = effect_mapping[q_alert.effect]
            active = alert.active_period.add()
            active.start = int(datetime.timestamp(q_alert.start_timestamp))
            active.end =  (int(datetime.timestamp(q_alert.start_timestamp)) + q_alert.duration.seconds)
            h = alert.header_text
            trans = h.translation.add()
            trans.text = q_alert.message
            trans.language = "en"
        return response.HttpResponse(data.SerializeToString(), content_type="application/protobuf")
