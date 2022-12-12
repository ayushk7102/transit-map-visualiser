# transit-map-visualiser
Generate visualisations of **subway** and other **rapid transit maps** using ShapeLy, GeoPandas, and public data by Google GTFS.

In the context of public transit system, a **timetable** represents bus/train schedules and contains information related to a transit network and the movement of vehicles on routes. 


The most common way of representing timetable information is [General Transit Feed Specification (GTFS) reference guide](https://developers.google.com/transit/gtfs/reference) maintained by Google.

## Map generation
This script parses the GTFS data for a given city transit service (eg: New York Subway), tracking stations and their lat/long coordinates. It then draws out discrete routes (each one as a sequence of stops) on a blank shapefile of the given city.

The result is a visualisation of the spread and structure of a city's transit network, generated from GTFS.




eg: NYC Subway transit map (generated from nyc_gtfs.zip and a blank geoJSON file of NYC)

![nyc_subway](https://user-images.githubusercontent.com/65803868/206926321-57299459-2eb1-403a-aa2f-09142eb6c6aa.png)



Transports Metropolitans de Barcelona (TMB) transit map, showing metro and bus lines. The routes spread beyond the city boundaries (as per barcelona.geoJSON)
![barcelona](https://user-images.githubusercontent.com/65803868/206997180-e6fc474e-76d5-4efa-a685-3da207101ffa.png)
