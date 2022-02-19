from esri import esri_auth, esri_standard_geography_api
from shapely.geometry import shape, Point, Polygon, mapping, MultiPolygon
import db
from utils import create_polygon_lat_lng_values

auth_token = esri_auth()


cbsa_url_slugs = {
    "31080": "los-angeles-long-beach-anaheim-real-estate-market-trends",
    "40140": "riverside-san-bernardino-ontario-real-estate-market-trends",
    "41740": "san-diego-carlsbad-real-estate-market-trends"
}

cbsa_list = ["31080", "40140", "41740"]
cbsa_zipcode_list = []
for cbsacode in cbsa_list:

    # get lat/lon values for zipcode polygons
    geo_features = esri_standard_geography_api(geoid=cbsacode, auth_token=auth_token)

    zipcode_list = []
    market_zipcode_list = []

    # iterate through results from esri standard geography api
    for geo_dict in geo_features:
        zipcode = geo_dict['attributes']['AreaID']

        geometry = []
        # if zipcode has multiple polygons
        if len(geo_dict['geometry']['rings']) > 1:
            multi_polygon_list = []
            for i, lat_lng_array in enumerate(geo_dict['geometry']['rings']):
                polygon_lat_lng = create_polygon_lat_lng_values(lat_lng_array)
                multi_polygon_list.append(polygon_lat_lng)

            zipcode_list.append({
                "zipcode": zipcode,
                "geometry": multi_polygon_list
            })
        # if zipcode has only one polygon
        else:
            polygon_lat_lng = create_polygon_lat_lng_values(geo_dict['geometry']['rings'][0])
            zipcode_list.append({
                "zipcode": zipcode,
                "geometry": [polygon_lat_lng]
            })

    # create mongo record for each cbsa
    cbsa_zipcode_list.append({
        "cbsacode": cbsacode,
        "urlslug": cbsa_url_slugs[cbsacode],
        "zipprofiles": zipcode_list,
    })

# insert all cbsa data into mongo
db.insert_list_mongo(list_data=cbsa_zipcode_list,
                     dbname='ScopeOutMaps',
                     collection_name='MarketMapsTest',
                     collection_update_existing={})

