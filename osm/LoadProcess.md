1. Run the OverpassQL query to grab the data from overpass-turbo.eu.
2. Download the XML extract
3. Run the extract through osmium with ```osmium add-locations-to-ways -o export2.osm ./export.xml```
4. Run the python script over the data.
