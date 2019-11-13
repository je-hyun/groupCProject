from geopy.geocoders import Nominatim

def addressToCoordinates(strAddress):
    """
    Args:
        strAddress (str): The string representation of the address

    Returns:
        A 2-element-tuple with the strAddress's latitude and longitude
    """
    geolocator = Nominatim(user_agent="groupCProject")
    location = geolocator.geocode(strAddress)
    return (location.latitude, location.longitude)
