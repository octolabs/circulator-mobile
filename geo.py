import math

nauticalMilePerLat = 60.00721
nauticalMilePerLongitude = 60.10793
rad = math.pi / 180.0
milesPerNauticalMile = 1.15077945

def distance(lat1, lon1, lat2, lon2):                      
    """
    Caclulate distance between two lat lons in NM
    """
    yDistance = (lat2 - lat1) * nauticalMilePerLat
    xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * (nauticalMilePerLongitude / 2)
    
    distance = math.sqrt( yDistance**2 + xDistance**2 )
    
    return distance * milesPerNauticalMile
    
    """
    =SQRT(
    ((F165-F164)*60.00721)^2
    
    +(
        (
        COS(F165*PI()*180)+
        COS(F164*PI()*180)
        )*(E164-E165)*60.10793/2
    )^2
    
    )
    
    *1.15077945
    """
    
def box(lat, lon, radius ):
    """
    Returns two lat/lon pairs as (lat1, lon2, lat2, lon2) which define a box that exactly surrounds
    a circle of radius of the given amount in miles.
    """
    latRange = radius / ( milesPerNauticalMile * 60.0 )
    lonRange = radius / ( math.cos(lat * rad) * milesPerNauticalMile * 60.0)
    
    return ( lat - latRange, lon - lonRange, lat + latRange, lon + lonRange )
    
def box_old (lat, lon, radius):
    """ Old box calculations """
    longitude = lon
    latitude = lat
    #radius = 0.06 #in miles - 0.02 mile = ~32 meters
        
    lng_min = longitude - radius / abs(math.cos(math.radians(latitude)) * 69)
    lng_max = longitude + radius / abs(math.cos(math.radians(latitude)) * 69)
    lat_min = latitude - (radius / 69)
    lat_max = latitude + (radius / 69)
    
    return ( lat_min, lng_min, lat_max, lng_max)
