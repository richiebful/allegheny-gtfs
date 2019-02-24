--manually insert Agency

--INSERT INTO Agencies (
--       ShortName,
--       LongName,
--       URL
--)
--VALUES (
--       'BCTA',
--       'Beaver County Transit Authority',
--       'http://bcta.org/'
--)

insert into routes (
       agencyid
       ,shortname
       ,longname
)
select a.agencyid
       ,r.ref
       ,r.name
from osm.routes as r
join agencies as a
on r.operator = a.longname;

--manually add url, route color, etc

insert into stops (
       code,
       name,
       location 
)                  
select number,
       name,
       location 
from (             
     select ref,   
            regexp_split_to_table(number, ';') as number,
            regexp_split_to_table(name, ';') as name,
            regexp_split_to_table(operator, ';') as operator,
            ST_Point(lat::float, lon::float) as location
      from osm.stops                                    
      ) as Stops                                    
where Operator = '' OR Operator LIKE 'Beaver%';


