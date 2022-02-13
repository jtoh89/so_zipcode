from esri import esri_auth, esri_standard_geography_api
from pymongo import MongoClient
import os
from shapely.geometry import shape, Point, Polygon, mapping, MultiPolygon
import db


auth_token = esri_auth()
cbsa_list = ["31080"]
for cbsacode in cbsa_list:

    geo_features = esri_standard_geography_api(geoid=cbsacode, auth_token=auth_token, geo_level=GeoLevels.ZIPCODE)


    zipcode_list = []

    for geo_dict in geo_features:
        zipcode_test = geo_dict['attributes']['AreaID']
        if zipcode_test != "92683":
            continue

        geometry = []
        if len(geo_dict['geometry']['rings']) > 1 and (zipcode_test == "92683"):
            parentPolygon = ""
            diff_poly = ""
            subPolygonList = []
            for i, lat_lng_array in enumerate(geo_dict['geometry']['rings']):
                if parentPolygon == "":
                    parentPolygon = Polygon(lat_lng_array)
                    continue

                subPolygon = Polygon(lat_lng_array)

                if (parentPolygon.intersects(subPolygon) is True):
                    subPolygonList.append(subPolygon)
                else:
                    subPolygonList.append(parentPolygon)


            # difference_poly = parentPolygon.difference(MultiPolygon(subPolygonList))
            # poly_mapped = mapping(difference_poly)
            # geo_list = []
            # for i, polyTupleList in enumerate(poly_mapped['coordinates']):
            #     for polytuple in polyTupleList:
            #         geo_list.append(polytuple)
            # geometry.append(geo_list)

        ### ADD AFTER TESTING
        # else:
        #     geometry = geo_dict['geometry']['rings']



            poly_mapped = mapping(diff_poly[0])

            geo_list = []
            for i, polyTupleList in enumerate(poly_mapped['coordinates']):
                for polytuple in polyTupleList:
                    geo_list.append(polytuple)
            geometry.append(geo_list)

        zipcode_list.append(
            {
                "zipcode":geo_dict['attributes']['AreaID'],
                # "geometry": geo_dict['geometry']['rings']
                "geometry": geometry
            }
        )

    cbsa_ziplist = {
        "cbsacode": cbsacode,
        "zipcodes": zipcode_list
    }

    db.insert_list_mongo(list_data=[cbsa_ziplist],
                                  dbname='Geographies',
                                  collection_name='EsriZipcodes',
                                  collection_update_existing={"cbsacode": cbsacode})


