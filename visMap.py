import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from readGTFS import *
stops, routes, trips, stoptimes = read_data('nyc')

# path_to_data = gpd.datasets.get_path("naturalearth_lowres")
# print(gpd.datasets.available)
gdf = gpd.read_file('Borough Boundaries.geojson')
print(gdf)

# exit()
# gdf["area"] = gdf.area
# gdf["centroid"] = gdf.centroid
# gdf.plot("area", legend=True)
# ax = gdf["geometry"].plot()
ax=gdf.plot()
# gdf["centroid"].plot(ax=ax, color="black")


uniqstops = set()
uniq_s = []
for stop in stops:
	if stop.name not in uniqstops:
		uniq_s.append(stop)
		print(str(stop))
	
	uniqstops.add(stop.name)


stop_pts = [Point((p.long, p.lat)) for p in uniq_s]

for pt in stop_pts:
	gpt = gpd.GeoSeries(pt)
	gpt.plot(ax=ax)
	plt.draw()
plt.show()
