import math
# import MySQLdb
# import MySQLdb.cursors
# import config
# from pymongo import MongoClient

class GeoLocation:
    '''
    Class representing a coordinate on a sphere, most likely Earth.
    
    This class is based from the code sample in this paper:
        http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
        
    The owner of that website, Jan Philip Matuschek, is the full owner of 
    his intellectual property. This class is simply a Python port of his very
    useful Java code. All code written by Jan Philip Matuschek and ported by me 
    (which is all of this class) is owned by Jan Philip Matuschek.
    '''
 
 
    MIN_LAT = math.radians(-90)
    MAX_LAT = math.radians(90)
    MIN_LON = math.radians(-180)
    MAX_LON = math.radians(180)
    
    EARTH_RADIUS = 6378.1  # kilometers
    
    
    @classmethod
    def from_degrees(cls, deg_lat, deg_lon):
        rad_lat = math.radians(deg_lat)
        rad_lon = math.radians(deg_lon)
        return GeoLocation(rad_lat, rad_lon, deg_lat, deg_lon)
        
    @classmethod
    def from_radians(cls, rad_lat, rad_lon):
        deg_lat = math.degrees(rad_lat)
        deg_lon = math.degrees(rad_lon)
        return GeoLocation(rad_lat, rad_lon, deg_lat, deg_lon)
    
    
    def __init__(
            self,
            rad_lat,
            rad_lon,
            deg_lat,
            deg_lon
    ):
        self.rad_lat = float(rad_lat)
        self.rad_lon = float(rad_lon)
        self.deg_lat = float(deg_lat)
        self.deg_lon = float(deg_lon)
        self._check_bounds()
        
    def __str__(self):
        degree_sign= u'\N{DEGREE SIGN}'
        return ("({0:.4f}deg, {1:.4f}deg) = ({2:.6f}rad, {3:.6f}rad)").format(
            self.deg_lat, self.deg_lon, self.rad_lat, self.rad_lon)
        
    def _check_bounds(self):
        if (self.rad_lat < GeoLocation.MIN_LAT 
                or self.rad_lat > GeoLocation.MAX_LAT 
                or self.rad_lon < GeoLocation.MIN_LON 
                or self.rad_lon > GeoLocation.MAX_LON):
            raise Exception("Illegal arguments")
            
    def distance_to(self, other, radius=EARTH_RADIUS):
        '''
        Computes the great circle distance between this GeoLocation instance
        and the other.
        '''
        if self.rad_lon - other.rad_lon == 0:
            return 10000
        else:
            return radius * math.acos(
                    math.sin(self.rad_lat) * math.sin(other.rad_lat) +
                    math.cos(self.rad_lat) * 
                    math.cos(other.rad_lat) * 
                    math.cos(self.rad_lon - other.rad_lon)
                )
            
    def bounding_locations(self, distance, radius=EARTH_RADIUS):
        '''
        Computes the bounding coordinates of all points on the surface
        of a sphere that has a great circle distance to the point represented
        by this GeoLocation instance that is less or equal to the distance argument.
        
        Param:
            distance - the distance from the point represented by this GeoLocation
                       instance. Must be measured in the same unit as the radius
                       argument (which is kilometers by default)
            
            radius   - the radius of the sphere. defaults to Earth's radius.
            
        Returns a list of two GeoLoations - the SW corner and the NE corner - that
        represents the bounding box.
        '''
        
        if radius < 0 or distance < 0:
            raise Exception("Illegal arguments")
            
        # angular distance in radians on a great circle
        rad_dist = distance / radius
        
        min_lat = self.rad_lat - rad_dist
        max_lat = self.rad_lat + rad_dist
        
        if min_lat > GeoLocation.MIN_LAT and max_lat < GeoLocation.MAX_LAT:
            delta_lon = math.asin(math.sin(rad_dist) / math.cos(self.rad_lat))
            
            min_lon = self.rad_lon - delta_lon
            if min_lon < GeoLocation.MIN_LON:
                min_lon += 2 * math.pi
                
            max_lon = self.rad_lon + delta_lon
            if max_lon > GeoLocation.MAX_LON:
                max_lon -= 2 * math.pi
        # a pole is within the distance
        else:
            min_lat = max(min_lat, GeoLocation.MIN_LAT)
            max_lat = min(max_lat, GeoLocation.MAX_LAT)
            min_lon = GeoLocation.MIN_LON
            max_lon = GeoLocation.MAX_LON
        
        return [ GeoLocation.from_radians(min_lat, min_lon) , 
            GeoLocation.from_radians(max_lat, max_lon) ]


            
if __name__ == '__main__':
    
    # Lat, Lng    
    start = GeoLocation.from_degrees(1.428963, 103.775117)
    stop = GeoLocation.from_degrees(1.429118, 103.775062)
    # result is in km ( perhaps check < 0.020)
    print start.distance_to(stop)
    
    
    
    
#     mongo_client = MongoClient(config.MONGO_DATABASE_HOST, config.MONGO_DATABASE_PORT)
#     mongo_db_onespace = mongo_client[config.MONGO_DATABASE_NAME_ONESPACE]
#     mongo_collection_googleplaces = mongo_db_onespace['googleplaces']
#     
#     con1=MySQLdb.connect(host=config.MYSQL_DATABASE_HOST,user=config.MYSQL_DATABASE_USER, passwd=config.MYSQL_DATABASE_PASSWD, port=int(config.MYSQL_DATABASE_PORT),db=config.MYSQL_DATABASE_NAME_FOURSQUARE,cursorclass=MySQLdb.cursors.SSCursor)
#     c1 = con1.cursor()
#     uncrawledVenues = "SELECT mongo_id, venue_id, name_simplified,lat,lng, (LOG(tip_count+1) * LOG(checkins_count+1) * LOG(users_count+1)) AS score \
#                       FROM fsVenues WHERE checkins_count > 10 AND users_count > 10 ORDER BY score DESC  LIMIT 100"
#     c1.execute(uncrawledVenues)
#     row = c1.fetchone()
#     while row is not None:
#         loc = GeoLocation.from_degrees(row[3], row[4])
#         distance = 1  # 1 kilometer
#         SW_loc, NE_loc = loc.bounding_locations(distance)
#         print row[2],SW_loc,NE_loc
#         row = c1.fetchone()
#     c1.close() 
#     con1.close()

