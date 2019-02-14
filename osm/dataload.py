from lxml import etree

with open('export2.xml') as overpass_fp:
    overpass_tree = etree.parse(overpass_fp)

routes = overpass_tree.xpath("//relation[tag/@k = 'route_master']")
trips = []
for rte in routes:
    child_trip_nodes = rte.xpath("member")
    members = []
    for child in child_trip_nodes:
        members.append({
            "ref": child.xpath("@ref")[0],
            "role": child.xpath("@role")[0]
        })
        trips += members

    rte_spec = {
        "id": rte.xpath("@id")[0],
        "name": rte.xpath("tag[@k='name']/@v")[0],
        "operator": rte.xpath("tag[@k='operator']/@v")[0],
        "ref": rte.xpath("tag[@k='ref']/@v")[0],
        "members": members
    }

refined_trips = []
for trip in trips:
    trip_node = overpass_tree.xpath("//relation[@id=$trip_id]", trip_id=trip["ref"])[0]
    trip["origin"] = trip_node.xpath("tag[@k='from']/@v")[0]
    trip["destination"] = trip_node.xpath("tag[@k='to']/@v")[0]
    
    stop_nodes = trip_node.xpath("member[@type='node']")
    stops = []
    for stop_node in stop_nodes:
        stop = {
            "ref": stop_node.xpath("@ref")[0],
            "role": stop_node.xpath("@role")[0]
        }
        stops.append(stop)

    shape_nodes = trip_node.xpath("member[@type='way']")
    shapes = []
    for shape_node in shape_nodes:
        shape = {
            "ref": shape_node.xpath("@ref")[0],
            "role": shape_node.xpath("@role")[0]
        }
        stops.append(stop)

refined_stops = []
for stop in stops:
    stop_node = overpass_tree.xpath("//node[@id=$stop_id]", stop_id=stop["ref"])[0]
    stop["lat"] = stop_node.xpath("@lat")[0]
    stop["lon"] = stop_node.xpath("@lon")[0]
    stop["name"] = stop_node.xpath("tag[@k='name']/@v")[0]
    stop["number"] = stop_node.xpath("tag[@k='ref']/@v")[0]
    refined_stops.append(stop)

refined_shapes = []
for shape in shapes:
    shape_node = overpass_tree.xpath("//way[@id=$way_id]", way_id=shape["ref"])[0]
    shape["lat"] = list([n.text for n in shape_node.xpath("@lat")])
    shape["lon"] = list([n.text for n in shape_node.xpath("@lon")])
    refined_shapes.append(shape)