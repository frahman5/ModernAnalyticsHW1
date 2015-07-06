#!/usr/bin/env python
__author__ = 'aub3'


# code taken from
import math
def get_distance(lat1, long1, lat2, long2):
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
        # we round because some numbers were coming out infinetially above 1
        # we round to 6 digits after the decimal because location data is
        # provided with 6 digits post-decimal accuracy
    arc = math.acos(cos)
    
    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    # MODIFIED TO return distance in miles
    return arc*3960.0

if __name__ == '__main__':
    import pandas as pd
    from pprint import pprint

    distances = []
    error_count  = 0
    
    # create a pandas dataframe with the location data
    df = pd.read_csv('example_data.csv')
    dfWithLocData = df[['pickup_longitude','pickup_latitude','dropoff_longitude', 'dropoff_latitude']]

    for index, plong, plat, dlong, dlat in dfWithLocData.itertuples():
        plong = float(plong)
        plat = float(plat)
        dlong = float(dlong)
        dlat = float(dlat)
        try:
            distances.append(get_distance(plat,plong,dlat,dlong))
        except:
            error_count += 1
            print plat, plong, dlat, dlong
            print error_count
    print "Num errors: {}".format(error_count)
    distances.sort(reverse=True)
    print "number of distances | maximum distance | minimum distance"
        # distance is measured in miles
    print "{} | {} | {}".format(len(distances),max(distances),min(distances))
    print "Top 50 distances, obvious outliers"
    pprint(distances[:50])

