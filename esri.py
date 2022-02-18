import os
from dotenv import load_dotenv
import requests as r

def esri_standard_geography_api(geoid, auth_token):
    url = "https://geoenrich.arcgis.com/arcgis/rest/services/World/geoenrichmentserver/StandardGeographyQuery/execute"

    params = {
        "sourceCountry": "US",
        "geographylayers": ["US.CBSA"],
        "geographyids": [geoid],
        "returnGeometry": True,
        "returnSubGeographyLayer": True,
        "subGeographyLayer": "US.ZIP5",
        "generalizationLevel": 0,
        "f": "pjson",
        "token": auth_token,
    }

    response = r.get(url=url, params=params)
    response = response.json()

    geo_features = response['results'][0]['value']['features']

    return geo_features



def esri_auth():
    load_dotenv()

    arcgis_clientid = os.getenv("ESRI_OAUTH_CLIENT_ID_JAYLEEONG0913")
    arcgis_clientsecret = os.getenv("ESRI_OAUTH_CLIENT_SECRET_JAYLEEONG0913")
    url = "https://www.arcgis.com/sharing/rest/oauth2/token"

    params = {
        "client_id":arcgis_clientid,
        "client_secret":arcgis_clientsecret,
        "grant_type":"client_credentials"
    }

    response = r.get(url=url, params=params)
    response = response.json()

    return response['access_token']

