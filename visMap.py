import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from readGTFS import *
stops, routes, trips, stoptimes = read_data('nyc')

path_to_data = gpd.datasets.get_path("nybb")
gdf = gpd.read_file(path_to_data)
gdf["area"] = gdf.area
gdf["centroid"] = gdf.centroid
# gdf.plot("area", legend=True)
ax = gdf["geometry"].plot()
gdf["centroid"].plot(ax=ax, color="black")


uniqstops = set()
uniq_s = []
for stop in stops:
	if stop.name not in uniqstops:
		uniq_s.append(stop)
		print(str(stop))
	
	uniqstops.add(stop.name)


stop_pts = [Point((p.lat, p.long)) for p in uniq_s]

for pt in stop_pts:
	gpt = gpd.GeoSeries(pt)
	# gpt.plot(ax=ax)

plt.show()
