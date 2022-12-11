import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString

from readGTFS import *

stops, routes, trips, stoptimes = read_data('nyc')

# path_to_data = gpd.datasets.get_path("naturalearth_lowres")
# print(gpd.datasets.available)
gdf = gpd.read_file('Borough Boundaries.geojson')
# print(gdf)

# exit()
# gdf["area"] = gdf.area
# gdf["centroid"] = gdf.centroid
# gdf.plot("area", legend=True)
# ax = gdf["geometry"].plot()
ax=gdf.plot()
# gdf["centroid"].plot(ax=ax, color="black")

stops_loc_dict = {} # key: stop_id, value: (slong, slat)
uniqstops = set()
uniq_s = []
for stop in stops:
	if stop.id not in uniqstops:
		uniq_s.append(stop)
		stops_loc_dict[stop.id] = (stop.long, stop.lat)
		# print(str(stop))
	
	uniqstops.add(stop.id)


stop_pts = [Point((p.long, p.lat)) for p in uniq_s]

for pt in stop_pts:
	gpt = gpd.GeoSeries(pt)
	gpt.plot(ax=ax, markersize=6,color='black')
	plt.draw()
# plt.show()



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


route_stops = {}         # dictionary with key: route_id, value: [stop1, stop2..])

for rt_k in route_trips.keys():
	print('ROUTE : ', rt_k)
	trip_0 = route_trips[rt_k][0]
	route_stops[rt_k] = trip_stops[trip_0].stops


ni = 0
n = len(route_stops)
for k in route_stops.keys():
	# print(k)
	rt_stps = route_stops[k]
	print("Trip {0}/{1}".format(ni, n))
	nstops = len(rt_stps)
	for i in range(len(rt_stps)-1):
		# print('here ', stops_loc_dict[rt_stps[i]])
		try:
			print("Stop {0}/{1}".format(i, nstops) , '\t',stops_loc_dict[rt_stps[i]],'--->',stops_loc_dict[rt_stps[i+1]])
			subway_link = LineString([stops_loc_dict[rt_stps[i]], stops_loc_dict[rt_stps[i+1]]])
			subway_link_gpd = gpd.GeoSeries(subway_link)
			subway_link_gpd.plot(ax=ax, color='red')
			plt.draw()
			# plt.pause(0.001)

		except KeyError:
			continue
	ni+=1
plt.show()
