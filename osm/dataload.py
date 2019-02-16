from lxml import etree
import pandas as pd

with open('export2.xml') as overpass_fp:
    overpass_tree = etree.parse(overpass_fp)

route_nodes = overpass_tree.xpath("//relation[tag/@k = 'route_master']")
routes = []
trips = []
for rte in route_nodes:
    child_trip_nodes = rte.xpath("member")
    members = []
    for child in child_trip_nodes:
        members.append({
            "ref": child.xpath("@ref")[0],
            "role": child.xpath("@role")[0]
        })
        trips.extend(members)

    rte_spec = {
        "id": rte.xpath("@id")[0],
        "name": rte.xpath("tag[@k='name']/@v")[0],
        "operator": rte.xpath("tag[@k='operator']/@v")[0],
        "ref": rte.xpath("tag[@k='ref']/@v")[0]
    }
    routes.append(rte_spec)

refined_trips = []
stops = []
shapes = []
for trip in trips:
    trip_node = overpass_tree.xpath("//relation[@id=$trip_id]", trip_id=trip["ref"])[0]
    trip["origin"] = trip_node.xpath("tag[@k='from']/@v")[0]
    trip["destination"] = trip_node.xpath("tag[@k='to']/@v")[0]
    trip["name"] = trip_node.xpath("tag[@k='name']/@v")[0]
    refined_trips.append(trip)
    
    stop_nodes = trip_node.xpath("member[@type='node']")
    for stop_node in stop_nodes:
        stop = {
            "ref": stop_node.xpath("@ref")[0],
            "role": stop_node.xpath("@role")[0]
        }
        stops.append(stop)

    shape_nodes = trip_node.xpath("member[@type='way']")
    for shape_node in shape_nodes:
        shape = {
            "ref": shape_node.xpath("@ref")[0],
            "role": shape_node.xpath("@role")[0]
        }
        shapes.append(shape)

refined_stops = []
for stop in stops:
    stop_node = overpass_tree.xpath("//node[@id=$stop_id]", stop_id=stop["ref"])[0]
    names = stop_node.xpath("tag[@k='name']/@v")
    if (len(names) > 0):
        stop["name"] = names[0]
    else:
        stop["name"] = ''
    stop_numbers = stop_node.xpath("tag[@k='ref']/@v")
    if (len(stop_numbers) > 0):
        stop["number"] = stop_numbers[0]
    else:
        stop["number"] = ''
    stop["lat"] = stop_node.xpath("@lat")[0]
    stop["lon"] = stop_node.xpath("@lon")[0]
    refined_stops.append(stop)

refined_shapes = []
for shape in shapes:
    shape_node = overpass_tree.xpath("//way[@id=$way_id]", way_id=shape["ref"])[0]
    lat = [n.text for n in shape_node.xpath("@lat")]
    lon = [n.text for n in shape_node.xpath("@lon")]
    latlon = list(zip(lat, lon))
    for i in range(len(latlon)):
        shape["lat"] = latlon[i][0]
        shape["lon"] = latlon[i][1]
        shape["seq"] = i
        refined_shapes.append(shape)

df_stops = pd.DataFrame.from_records(refined_stops)
print(df_stops)

df_trips = pd.DataFrame.from_records(refined_trips)
print(df_trips)

df_routes = pd.DataFrame.from_records(routes)
print(df_routes)