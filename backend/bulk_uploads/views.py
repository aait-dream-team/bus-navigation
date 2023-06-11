import csv
import os
import zipfile

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.db import transaction

from agencies.models import Agency
from admins.models import Admin
from stops.models import Stop
from routes.models import Route
from calendars.models import Calendar
from shapes.models import Shape
from trips.models import Trip
from stop_times.models import StopTime



# A view that handles the post request and calls a function for each file in the zip
@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def unzip_and_add(request):
    # check if there is a zip file in the request data
    if 'zip_file' in request.data:
        zip_file = request.data['zip_file']
        with zipfile.ZipFile(zip_file, "r") as z:
            with transaction.atomic():
                admin = Admin.objects.first()
                jobs = [
                    ['agency', 'agency.txt', add_agency_row_to_db, Agency],
                    ['stop', 'stops.txt', add_stop_row_to_db, Stop],
                    ['route', 'routes.txt', add_route_row_to_db, Route],
                    ['calendar', 'calendar.txt', add_calendar_row_to_db, Calendar],
                    ['shape', 'shapes.txt', add_shape_row_to_db, Shape],
                    ['trip', 'trips.txt', add_trip_row_to_db, Trip],
                    ['stoptime', 'stop_times.txt', add_stoptime_row_to_db, StopTime]
                ]
                for entity, filename, func, model in jobs:
                    new_instances = [] 
                    print("Got to", entity)
                    # get the list of rows from the csv file
                    z.extract(filename)
                    rows = read_csv_rows(filename)
                    os.remove(filename)

                    # loop through the rows and add them to the database
                    for row in rows:
                        entity_instance = func(row, admin)
                        new_instances.append(entity_instance)
                    
                    model.objects.bulk_create(new_instances, ignore_conflicts=True)
                    print(f"Updated {len(new_instances)} models")
                return Response({'message': 'Success'}, status=status.HTTP_200_OK)
            # get the zip file from request.data
            zip_file = request.data['zip_file']
            # open it with zipfile.ZipFile
            with zipfile.ZipFile(zip_file) as z:
                # loop through its namelist
                for file_name in z.namelist():
                    # read its content with zip_file.read
                    content = z.read(file_name)
                    # pass it to your function
                    your_function(content)
        # return a success response
        return Response({'message': 'Success'}, status=status.HTTP_200_OK)
    else:
        # return an error response
        return Response({'error': 'No zip file provided'}, status=status.HTTP_400_BAD_REQUEST)

# A function that reads the rows of the csv file and returns a list of dictionaries
def read_csv_rows(filename):
    rows = [] # an empty list to store the rows
    with open(filename, 'r') as file:
        reader = csv.DictReader(file) # create a csv reader object
        for row in reader: # loop through the rows
            rows.append(row) # append each row as a dictionary to the list
    return rows # return the list of rows

# A function that adds a single row to the database using get_or_create
def add_agency_row_to_db(row, admin):
    # extract the values of the fields from the row dictionary
    agency_id = row['agency_id']
    agency_name = row['agency_name']
    agency_url = row['agency_url']
    agency_timezone = row['agency_timezone']
    agency_lang = row['agency_lang']

    # provide some sensible defaults for the fields that are not in the csv file
    phone = '000-000-0000' # a dummy phone number

    # use get_or_create to create a new object or get an existing one based on agency_id
    agency = Agency(
        id=agency_id,
            name=agency_name,
            url=agency_url,
            time_zone=agency_timezone,
            lang=agency_lang,
            phone=phone,
            admin=admin
    )
    # return the agency object and the created boolean
    return agency

def add_stop_row_to_db(row, admin):
    # extract the values of the fields from the row dictionary
    stop_id = row['stop_id']
    stop_name = row['stop_name']
    stop_lat = row['stop_lat']
    stop_lon = row['stop_lon']

    # provide some sensible defaults for the fields that are not in the csv file
    stop_desc = 'No description available' # a dummy description
    stop_code = 'N/A' # a dummy code
    stop_url = 'https://example.com' # a dummy url
    parent_station = None # no parent station by default

    # use get_or_create to create a new object or get an existing one based on stop_id
    stop = Stop(
        id=stop_id,
        stop_name=stop_name,
        stop_desc=stop_desc,
        stop_code=stop_code,
        stop_lat=stop_lat,
        stop_long=stop_lon,
        stop_url=stop_url,
        parent_station=parent_station,
        admin=admin
    )
    # return the stop object and the created boolean
    return stop

def add_route_row_to_db(row, admin):
    # extract the values of the fields from the row dictionary
    route_id = row['route_id']
    agency_id = row['agency_id']
    route_short_name = row['route_short_name']
    route_long_name = row['route_long_name']
    route_type = row['route_type']
    route_color = row['route_color']

    # provide some sensible defaults for the fields that are not in the csv file
    route_desc = 'No description available' # a dummy description
    route_url = 'https://example.com' # a dummy url
    route_text_color = '#FFFFFF' # a default text color

    # get the agency object based on agency_id or raise an exception if not found
    agency = Agency.objects.get(id=agency_id)

    # use get_or_create to create a new object or get an existing one based on route_id
    route = Route(
        id=route_id,
        route_short_name=route_short_name,
        route_long_name=route_long_name,
        route_desc=route_desc,
        route_url=route_url,
        route_color=route_color,
        route_text_color=route_text_color,
        agency=agency
    )
    # return the route object and the created boolean
    return route

def add_calendar_row_to_db(row, admin):
    # extract the values of the fields from the row dictionary
    service_id = row['service_id']
    monday = row['monday']
    tuesday = row['tuesday']
    wednesday = row['wednesday']
    thursday = row['thursday']
    friday = row['friday']
    saturday = row['saturday']
    sunday = row['sunday']
    start_date = row['start_date']
    end_date = row['end_date']
    start_date = f'{start_date[:4]}-{start_date[4:6]}-{start_date[6:]}'
    end_date = f'{end_date[:4]}-{end_date[4:6]}-{end_date[6:]}'

    # convert the boolean values from strings to python booleans
    monday = True if monday == '1' else False
    tuesday = True if tuesday == '1' else False
    wednesday = True if wednesday == '1' else False
    thursday = True if thursday == '1' else False
    friday = True if friday == '1' else False
    saturday = True if saturday == '1' else False
    sunday = True if sunday == '1' else False

    # get the agency object based on service_id or raise an exception if not found
    agency = Agency.objects.first()

    # use get_or_create to create a new object or get an existing one based on service_id and start_date
    calendar = Calendar(
        service_id=service_id,
        start_date=start_date,
        monday=monday,
        tuesday=tuesday,
        wednesday=wednesday,
        thursday=thursday,
        friday=friday,
        saturday=saturday,
        sunday=sunday,
        end_date=end_date,
        agency=agency
    )
    # return the calendar object and the created boolean
    return calendar

def add_shape_row_to_db(row, admin):
    # extract the values of the fields from the row dictionary
    shape_id = row['shape_id']
    shape_pt_lat = row['shape_pt_lat']
    shape_pt_lon = row['shape_pt_lon']
    shape_pt_sequence = row['shape_pt_sequence']
    shape_dist_traveled = row['shape_dist_traveled']

    # use get_or_create to create a new object or get an existing one based on shape_id and shape_pt_sequence
    shape = Shape(
        id=shape_id,
        shape_pt_sequence=shape_pt_sequence,
        shape_pt_lat=shape_pt_lat,
        shape_pt_lon=shape_pt_lon,
        shape_dist_traveled=shape_dist_traveled,
    )
    # return the shape object and the created boolean
    return shape

def add_trip_row_to_db(row, admin):
    # extract the values of the fields from the row dictionary
    route_id = row['route_id']
    service_id = row['service_id']
    trip_headsign = row['trip_headsign']
    trip_id = row['trip_id']
    shape_id = row['shape_id']

    # provide some sensible defaults for the fields that are not in the txt file
    short_name = 'N/A' # a dummy short name
    direction = False # a default direction

    # get the agency object based on service_id or raise an exception if not found
    agency = Agency.objects.first()

    # get the shape object based on shape_id or raise an exception if not found
    shape = Shape.objects.get(id=shape_id)

    # get the route object based on route_id or raise an exception if not found
    route = Route.objects.get(id=route_id)

    # use get_or_create to create a new object or get an existing one based on trip_id
    trip = Trip(
        id=trip_id,
        headsign=trip_headsign,
        short_name=short_name,
        direction=direction,
        agency=agency,
        shape=shape,
        route=route
    )
    # return the trip object
    return trip

# A function that returns the object instead of saving it
def add_stoptime_row_to_db(row, admin):
    # extract the values of the fields from the row dictionary
    trip_id = row['trip_id']
    stop_id = row['stop_id']
    stop_sequence = row['stop_sequence']
    timepoint = row['timepoint']
    arrival_time = row['arrival_time']
    departure_time = row['departure_time']

    # provide some sensible defaults for the fields that are not in the txt file
    stop_headsign = 'N/A' # a dummy stop headsign

    # get the agency object based on admin or raise an exception if not found
    trip = Trip.objects.select_related('agency').get(id=trip_id)
    stop = Stop.objects.get(id=stop_id)

    # create a new StopTime object with the values from the row
    stoptime = StopTime(
        arrival_time=arrival_time,
        departure_time=departure_time,
        stop_sequence=stop_sequence,
        stop_headsign=stop_headsign,
        agency=trip.agency,
        trip=trip,
        stop=stop,
        timepoint=timepoint
    )
    # return the stoptime object
    return stoptime
