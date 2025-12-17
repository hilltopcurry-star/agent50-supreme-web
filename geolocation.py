import math
from models import Driver

class GeoLocationService:
    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """
        Calculate the distance between two points on Earth using the Haversine formula.
        """
        R = 6371  # Radius of Earth in kilometers

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad

        a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    @staticmethod
    def calculate_delivery_fee(distance):
        """
        Calculate the delivery fee based on the distance.
        """
        base_fee = 5
        per_km_fee = 1.5
        delivery_fee = base_fee + (distance * per_km_fee)
        return round(delivery_fee, 2)

    @staticmethod
    def find_nearby_drivers(customer_lat, customer_lon, radius=5):
        """
        Find available drivers within a specified radius (in km).
        """
        nearby_drivers = []
        available_drivers = Driver.query.filter_by(is_available=True).all()

        for driver in available_drivers:
            if driver.latitude and driver.longitude: # check for None values
                distance = GeoLocationService.haversine_distance(
                    customer_lat, customer_lon, driver.latitude, driver.longitude
                )
                if distance <= radius:
                    nearby_drivers.append(driver)
        return nearby_drivers