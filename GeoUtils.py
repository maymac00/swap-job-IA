import haversine as hs
import pgeocode


class GeoUtils:
    data = pgeocode.Nominatim('ES')
    distance = pgeocode.GeoDistance('es')
    pc2coords = {}
    @staticmethod
    def get_distance(lat1, lon1, lat2, lon2):
        return hs.haversine((lat1, lon1), (lat2, lon2))

    @staticmethod
    def get_distance_from_postal_code(postal_code1, postal_code2):

        return GeoUtils.distance.query_postal_code(postal_code1, postal_code2)

    @staticmethod
    def get_coords_from_postal_code(postal_code):

        if postal_code not in GeoUtils.pc2coords.keys():
            city = GeoUtils.data.query_postal_code(postal_code)
            GeoUtils.pc2coords[postal_code] = (city.latitude, city.longitude)
            return city.latitude, city.longitude
        else:
            t = GeoUtils.pc2coords[postal_code]
            return t[0], t[1]