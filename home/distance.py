from math import cos, asin, sqrt, pi
#Just make sure that both passed in objects have lat/long models
def longlatdistance(obj1, obj2):
    try:
        lat1 = obj1.latitude
        lon1 = obj1.longitude
        lat2 = obj2.latitude
        lon2 = obj2.longitude
    except:
        return 67000
    r = 3959
    p = pi / 180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 2 * r * asin(sqrt(a))