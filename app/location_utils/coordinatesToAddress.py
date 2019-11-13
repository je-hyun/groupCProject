from geopy.geocoders import Nominatim

def coordinatesToAddress(latitude, longitude):
    """
    Args:
        A 2-element-tuple with the strAddress's latitude and longitude

    Returns:
        strAddress (str): The string representation of the address
    """
    geolocator = Nominatim(user_agent="groupCProject")
    location = geolocator.reverse(latitude, longitude)
    return (location.address)
