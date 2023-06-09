from django.views import View
from django.http import response
from rest_framework import viewsets, permissions
import time

from .serializer import AlertSerializer, VehicleUpdateSerializer
from utils.common_permissions import IsOwner, IsSystemAdmin
from .models import Alert, VehicleUpdate
from . import gtfs_rt_pb2 as gg

cause_mapping = {
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
}
effect_mapping = {
    "NO_SERVICE": gg.Alert.Effect.NO_SERVICE,
    "REDUCED_SERVICE": gg.Alert.Effect.REDUCED_SERVICE,
    "SIGNIFICANT_DELAYS": gg.Alert.Effect.SIGNIFICANT_DELAYS,
    "DETOUR": gg.Alert.Effect.DETOUR,
    "ADDITIONAL_SERVICE": gg.Alert.Effect.ADDITIONAL_SERVICE,
    "MODIFIED_SERVICE": gg.Alert.Effect.MODIFIED_SERVICE,
    "OTHER_EFFECT": gg.Alert.Effect.OTHER_EFFECT,
    "UNKNOWN_EFFECT": gg.Alert.Effect.UNKNOWN_EFFECT,
    "STOP_MOVED": gg.Alert.Effect.STOP_MOVED,
}

class AlertView(View):
    def get(self, request):
        all_alerts = Alert.objects.all()
        data = gg.FeedMessage()
        header = data.header      
        header.gtfs_realtime_version = "2.0"
        for alert in all_alerts:
            entity = data.entity.add()
            generateFeedMessage(alert, entity)
        return response.HttpResponse(data.SerializeToString(), content_type="application/protobuf")

        

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            permission_classes = [permissions.IsAuthenticated & IsOwner]
        elif self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated & (IsOwner | IsSystemAdmin)]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
class VehicleUpdateViewSet(viewsets.ModelViewSet):
    queryset = VehicleUpdate.objects.all()
    serializer_class = VehicleUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            permission_classes = [permissions.IsAuthenticated & IsOwner]
        elif self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated & (IsOwner | IsSystemAdmin)]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
def generateFeedMessage(sent_alert: Alert, entity):
    entity.id = str(sent_alert.alert_feed_id)
    alert = entity.alert
    entity_sel = alert.informed_entity.add()
    if sent_alert.affected_entity == "route":
        entity_sel.route_id = sent_alert.entity_id
    elif sent_alert.affected_entity == 'agency':
        entity_sel.agency_id = sent_alert.entity_id
    elif sent_alert.affected_entity == 'trip':
        trip = entity_sel.trip
        trip.trip_id = sent_alert.trip_id

        print("We don't support trip_ids yet")
        entity_sel.trip_id = sent_alert.entity_id
    
    alert.cause = gg.Alert.Cause.STRIKE
    alert.effect = gg.Alert.Effect.REDUCED_SERVICE
    active = alert.active_period.add()
    active.start = time.mktime(sent_alert.start_timestamp)
    active.end = time.mktime(sent_alert.start_timestamp) + sent_alert.duration.seconds
    h = alert.header_text
    trans = h.translation.add()
    trans.text = f"We have an {sent_alert.effect} at {sent_alert.affected_entity} {sent_alert.entity_id} caused by {sent_alert.cause}"
    trans.language = "en" 