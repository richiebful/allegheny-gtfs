from lxml import etree
import pandas as pd
import sqlalchemy
import psycopg2
from os import environ

def first_value_if_key(context, key):
    expr = "tag[@k='{0}']/@v".format(key)
    res = context.xpath(expr)
    return res[0] if len(res) > 0 else None

myuser = environ["PGSQL_USER"]
mypassword = environ["PGSQL_PASSWORD"]
conn_string = "postgresql+psycopg2://{0}:{1}@localhost:5432/alleghenytransit".format(myuser, mypassword)
print(conn_string)
engine = sqlalchemy.create_engine(conn_string, client_encoding='utf8')
conn = engine.connect()

with open('export2.xml') as overpass_fp:
    overpass_tree = etree.parse(overpass_fp)

route_nodes = overpass_tree.xpath("//relation[tag/@k = 'route_master']")
routes = []
trips = []
for rte in route_nodes:
    child_trip_nodes = rte.xpath("member[@type='relation']")
    route_id = rte.xpath("@id")[0]
    for child in child_trip_nodes:
        trips.append({
            "ref": child.xpath("@ref")[0],
            "role": child.xpath("@role")[0],
            "parent": route_id
        })

    rte_spec = {
        "id": route_id,
        "name": rte.xpath("tag[@k='name']/@v")[0],
        "operator": first_value_if_key(rte, 'operator'),
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
            "role": stop_node.xpath("@role")[0],
            "parent": trip["ref"]
        }
        stops.append(stop)

    shape_nodes = trip_node.xpath("member[@type='way']")
    for shape_node in shape_nodes:
        shape = {
            "ref": shape_node.xpath("@ref")[0],
            "role": shape_node.xpath("@role")[0],
            "parent": trip["ref"]
        }
        shapes.append(shape)

refined_stops = []
for stop in stops:
    stop_node = overpass_tree.xpath("//node[@id=$stop_id]", stop_id=stop["ref"])[0]
    #grab name, platform number, network and operator if they exist
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
    network = stop_node.xpath("tag[@k='network']/@v")
    stop["network"] = network[0] if (len(network) > 0) else ''
    operator = stop_node.xpath("tag[@k='operator']/@v")
    stop["operator"] = operator[0] if (len(operator) > 0) else ''
    stop["lat"] = stop_node.xpath("@lat")[0]
    stop["lon"] = stop_node.xpath("@lon")[0]
    refined_stops.append(stop)

refined_shapes = []
for shape in shapes:
    shape_node = overpass_tree.xpath("//way[@id=$way_id]", way_id=shape["ref"])[0]
    lat = shape_node.xpath("nd/@lat")
    lon = shape_node.xpath("nd/@lon")
    latlon = list(zip(lat, lon))
    for i in range(len(latlon)):
        shape["lat"] = latlon[i][0]
        shape["lon"] = latlon[i][1]
        shape["seq"] = i
        refined_shapes.append(shape)

def truncate_if_exists(conn, schema, table):
    query = """SELECT *
    FROM   pg_tables
    WHERE  schemaname = '{0}'
    AND    tablename = '{1}'""".format(schema, table)

    print(conn.execute(query).fetchall())
    if len(conn.execute(query).fetchall()) > 0:
        conn.execute("drop table {0}.{1}".format(schema, table))
    else:
        return None    
    

df_stops = pd.DataFrame.from_records(refined_stops)
df_stops.to_sql('stops', con=engine, schema='osm', if_exists="replace")

df_trips = pd.DataFrame.from_records(refined_trips)
df_trips.to_sql('trips', con=engine, schema='osm', if_exists="replace")

df_routes = pd.DataFrame.from_records(routes)
df_routes.to_sql('routes', con=engine, schema='osm', if_exists="replace")

df_shapes = pd.DataFrame.from_records(refined_shapes)
df_shapes.to_sql('shapes', con=engine, schema='osm', if_exists="replace")
