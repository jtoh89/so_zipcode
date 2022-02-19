from esri import esri_auth, esri_standard_geography_api
from pymongo import MongoClient
import os
from shapely.geometry import shape, Point, Polygon, mapping, MultiPolygon
import db


auth_token = esri_auth()
cbsa_list = ["31080"]
for cbsacode in cbsa_list:

    # get lat/lon values for zipcode polygons
    geo_features = esri_standard_geography_api(geoid=cbsacode, auth_token=auth_token)

    zipcode_list = []

    # get lat/lon values for zipcode polygons
    for geo_dict in geo_features:
        zipcode_test = geo_dict['attributes']['AreaID']
        if zipcode_test != "92683":
            continue

        geometry = []
        if len(geo_dict['geometry']['rings']) > 1 and (zipcode_test == "92683"):
            parentPolygon = ""
            subPolygonList = []
            for i, lat_lng_array in enumerate(geo_dict['geometry']['rings']):
                if parentPolygon == "":
                    parentPolygon = Polygon(lat_lng_array)
                    continue

                subPolygon = Polygon(lat_lng_array)

                subPolygonList.append(subPolygon)
                # if (parentPolygon.intersects(subPolygon) is True):
                #     subPolygonList.append(subPolygon)
                # else:
                #     subPolygonList.append(parentPolygon)

            # difference_poly = parentPolygon.difference(MultiPolygon(subPolygonList))
            # poly_mapped = mapping(difference_poly)

            geo_list = []
            for i, poly_tuple_list in enumerate(poly_mapped['coordinates']):
                for poly_tuple in poly_tuple_list:
                    geo_list.append({
                        "lng": poly_tuple[0],
                        "lat": poly_tuple[1],
                    })
            geometry.append(geo_list)

        zipcode_list.append(
            {
                "zipcode":geo_dict['attributes']['AreaID'],
                "geometry": geometry
            }
        )




    cbsa_ziplist = {
        "cbsacode": cbsacode,
        "zipcodes": zipcode_list
    }

    db.insert_list_mongo(list_data=[cbsa_ziplist],
                                  dbname='ScopeOutMaps',
                                  collection_name='MarketMapsTest',
                                  collection_update_existing={"cbsacode": cbsacode})


