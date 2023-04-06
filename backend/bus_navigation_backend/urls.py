"""bus_navigation_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from admins import views as admin_views
from rest_framework.authtoken import views as auth_views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from agencies import views as agency_views
from routes import views as route_views
from stops import views as stop_views
from transfers import views as transfer_views
from calendars import views as calendar_views
from calendar_dates import views as calendar_date_views
from fares import views as fare_views
from stop_times import views as stop_time_views
from trips import views as trip_views
from plan import views as plan_views

router = DefaultRouter()
router.register(r'admins/create', admin_views.AdminsCreateViewSet, basename='admins_create')
router.register(r'admins', admin_views.AdminsViewSet, basename='admins')
router.register(r'agencies', agency_views.AgencyViewSet, basename='agencies')
router.register(r'routes', route_views.RouteViewSet, basename='routes')
router.register(r'stops', stop_views.StopViewSet, basename='stops')
router.register(r'transfers', transfer_views.TransferViewSet, basename='transfers')
router.register(r'calendars', calendar_views.CalendarViewSet, basename='calendars')
router.register(r'calendar_dates', calendar_date_views.CalendarDateViewSet , basename='calendar_dates')
router.register(r'fares', fare_views.FareViewSet, basename='fares')
router.register(r'stop_times', stop_time_views.StopTimeViewSet, basename='stop_times')
router.register(r'trips', trip_views.TripViewSet, basename='trips')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('plan/', plan_views.UserView.as_view()),
    # path('', include(router.urls)),
    path('api-token-auth/', auth_views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

