# transit-map-visualiser
Generate visualisations of **subway** and other **rapid transit maps** using Shapely, GeoPandas, and public transit timetable data by Google GTFS.

In the context of public transit system, a **timetable** represents bus/train schedules and contains information related to a transit network and the movement of vehicles on routes. 


The most common way of representing timetable information is [General Transit Feed Specification (GTFS) reference guide](https://developers.google.com/transit/gtfs/reference) maintained by Google.

## Map generation
This script parses the GTFS data for a given city transit service (eg: New York Subway), tracking stations and their lat/long coordinates. It then draws out discrete routes (each one as a sequence of stops) on a blank shapefile or geoJSON of the given city, acquired via an open source repository such as those on the city's public access site (eg: NYC Open Data), [India-Maps on GitHub](https://github.com/mickeykedia/India-Maps), or GIS databases.

The result is a visualisation of the spread and structure of a city's transit network, generated from GTFS.
 
GTFS data is pulled from public transit information repositories including [TransitFeeds](https://transitfeeds.com) and [The Mobility Database](https://database.mobilitydata.org/#h.iqo2575mk6q).



eg: NYC Subway transit map (generated from nyc_gtfs.zip and a blank geoJSON file of NYC). Dots represent stations.

![nyc_subway](https://user-images.githubusercontent.com/65803868/206926321-57299459-2eb1-403a-aa2f-09142eb6c6aa.png)



Transports Metropolitans de Barcelona (TMB) transit map, showing metro and bus lines. The routes spread beyond the city boundaries (as per barcelona.geoJSON).
![barcelona](https://user-images.githubusercontent.com/65803868/206997180-e6fc474e-76d5-4efa-a685-3da207101ffa.png)
