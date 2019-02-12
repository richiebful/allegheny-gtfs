from lxml import etree

with open('export.xml') as overpass_fp:
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
    print(trip)
    exit(0)                                                                                                   
