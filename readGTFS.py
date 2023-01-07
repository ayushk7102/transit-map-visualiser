
import pandas as pd
import zipfile
import pickle
read_stoptimes = False

class stop:
    """
    Stop class
    Params -
    id: stop_id
    name: stop_name
    """
    def __init__(self, sid, sname, slat, slong):
        self.id = sid
        self.name = sname
        self.lat = slat
        self.long = slong

    def __str__(self):
        return self.name + '\nLat: '+ str(self.lat) +'\tLong: '+ str(self.long)
class route:
    """
    Route class
    Params -
    rid: route_id
    rname: route_long_name
    """    
    def __init__(self, rid, rname):
        self.id = rid
        self.name = rname


class trip:
    """
    Trip class
    Params -
    tid: trip_id
    route_id: route_id
    """    
    def __init__(self, tid, route_id):
        self.id = tid
        self.route_id = route_id

    def __str__(self):
        return 'TRIP: ' +self.id + '  ROUTE_ID: '+self.route_id

class stop_time:
    """
    Trip class
    Params -
    trip_id: trip_id
    stop_id: stop_id
    arrival, departure times
    stop_seq: stop_sequence
    """    
    def __init__(self, trip_id, stop_id, arrival_time, departure_time, stop_seq):
        self.trip_id = trip_id
        self.stop_id = stop_id
        self.arr_time = arrival_time
        self.dep_time = departure_time
        self.seq = stop_seq

    def __str__(self):
        return 'TRIP: '+ str(self.trip_id) + '   STOP: '+self.stop_id + '  arrival_time: '+self.arr_time + '  dep_time: '+self.dep_time + '  seq: '+str(self.seq)


class route_stops: #helper class containing route_id and array of stops
    def __init__(self, rid, stops):
        self.route_id = rid
        self.stops = stops


"""
stops.txt : stop_id,stop_code,stop_name,tts_stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station,stop_timezone,wheelchair_boarding,level_id,platform_code
routes.txt : route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color,route_sort_order,continuous_pickup,continuous_drop_off
trips.txt : trip_id,route_id,service_id,trip_headsign,trip_short_name,direction_id,block_id,shape_id,wheelchair_accessible,bikes_allowed
stop_times.txt : trip_id,stop_id,arrival_time,departure_time,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled,continuous_pickup,continuous_drop_off,timepoint
"""

def print_route_trips(route_trips):
    all_trips = 0
    for k in route_trips.keys():
        print('ROUTE :', k)
        print('TRIPS: ', route_trips[k], '\n\n')
        all_trips += len(route_trips[k])

    print('Total number of routes: ', len(route_trips))
    print('Total number of trips: ', all_trips)

"""
Parses and reads the GTFS data
Returns: stops, routes, trips, stoptimes (lists)
"""
def read_data(city_name):
    # city_name = 'nyc'
    zip_path = city_name + '_gtfs.zip'
    dir_path = city_name + '_gtfs'

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dir_path)

    stops = []
    routes = []
    trips = []
    stoptimes = []

    stops_df = pd.read_csv(city_name + '_gtfs/stops.txt')
    for ix, s in stops_df.iterrows():
        stp = stop(s['stop_id'], s['stop_name'], s['stop_lat'], s['stop_lon'])
        stops.append(stp)
        # print(stp.name, stp.lat, stp.long)
        # print
    print('Loaded stops.')
    routes_df = pd.read_csv(city_name + '_gtfs/routes.txt')
    for ix, s in routes_df.iterrows():
        routes.append(route(s['route_id'], s['route_long_name']))
    print('Loaded routes.')

    trips_df = pd.read_csv(city_name + '_gtfs/trips.txt')
    for ix, s in trips_df.iterrows():
        trips.append(trip(s['trip_id'], s['route_id']))
    print('Loaded trips.')

    if read_stoptimes:
        stoptimes_df = pd.read_csv(city_name + '_gtfs/stop_times.txt')
        i=0
        for ix, s in stoptimes_df.iterrows():
            print('Reading ', i)
            i+=1
            stoptimes.append(stop_time(s['trip_id'], s['stop_id'], s['arrival_time'], s['departure_time'], s['stop_sequence']))
        print('Loaded stoptimes.')
        
        with open(r"{}".format(city_name)+r"_stoptimes_list.pickle", "wb") as output_file:
            pickle.dump(stoptimes, output_file)


    else:
        stoptimes = []
        with open(r"pickles/{}".format(city_name) + r"_stoptimes_list.pickle", "rb") as input_file:
            stoptimes = pickle.load(input_file)
            print('Loaded stoptimes from cache.')

    return stops, routes, trips, stoptimes






def get_unique_routes(src, dest, stops, routes, trips, stoptimes):

    route_trips = {}        # dictionary with key: route-id, value is a list of trip-ids
    trip_routes = {}        # dictionary with key: trip-id, value is a the mapped route-id

    for t in trips:
        if route_trips.get(t.route_id, 'nf') == 'nf':
            route_trips[t.route_id] = [t.id]
        else:
            route_trips[t.route_id].append(t.id)

        trip_routes[t.id] = t.route_id


    trip_stops = {}         # dictionary with key: trip_id, value: (route_id, [stop1, stop2..])
    nf = 'nf'
    for s in stoptimes:

        route_id = trip_routes[s.trip_id]

        if trip_stops.get(s.trip_id,  nf) == nf:
            trip_stops[s.trip_id] = route_stops(route_id, ([s.stop_id]))

        else:
            trip_stops[s.trip_id].stops.append(s.stop_id)


    uniq_routes = set()     # a set to store unique routes    
    
    for k in trip_stops.keys():
        stops_k = trip_stops[k]
        stops_arr = trip_stops[k].stops
        if src in stops_arr and dest in stops_arr: #both the source and destination are in the list of stops
            if stops_arr.index(src) < stops_arr.index(dest): #the source comes before the destination
                uniq_routes.add(stops_k.route_id)

    # print(uniq_routes)

    return uniq_routes

def number_of_routes(source_stopid: str, destination_stopid: str) -> int:
    """
    Find the number of routes going from source stop id to destination stop id.

    Args:
        source_stopid (str): Source Stop Id
        destination_stopid (str): Destination Stop Id

    Returns:
        final_count (int): Number of routes going from source to destination.
    """

    final_count = -1
    try:
        # Enter your code here
        src = source_stopid
        dest = destination_stopid

        # stops, routes, trips, stoptimes = read_data()
        uniq_routes = get_unique_routes(src, dest, stops, routes, trips, stoptimes)

        final_count = len(uniq_routes)

        return final_count
    except:
        return final_count
