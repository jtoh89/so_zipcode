


def create_polygon_lat_lng_values(polygon_x_y):
    polygon_lat_lng = []

    for latlng in polygon_x_y:
        polygon_lat_lng.append({
            "lng": latlng[0],
            "lat": latlng[1],
        })

    return polygon_lat_lng