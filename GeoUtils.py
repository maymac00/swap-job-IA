import numpy as np
import pgeocode
import haversine as hs
# from math import abs


class GeoUtils:

    @staticmethod
    def get_distance(lat1, lon1, lat2, lon2):
        return hs.haversine((lat1, lon1), (lat2, lon2))

    @staticmethod
    def get_distance_from_postal_code(postal_code1, postal_code2):
        data = pgeocode.GeoDistance('es')
        return data.query_postal_code(postal_code1, postal_code2)

    @staticmethod
    def get_coords_from_postal_code(postal_code):
        data = pgeocode.Nominatim('ES')
        city = data.query_postal_code(postal_code)
        return city.latitude, city.longitude