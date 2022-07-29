from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from uszipcode import SearchEngine

search = SearchEngine(SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)

def get_zipcode(lat, lon):
    s_point = Point(lon, lat)
    r = 10 
    results = []
    while not len(results) and r < 100:
        results = search.by_coordinates(lat, lon, radius=r, returns=20)
        r += 5
    if not len(results):
        return ""

    for result in results:
        cur_zipcode = result.zipcode
        try:
            cur_polygon = Polygon(result.polygon)
            if cur_polygon.contains(s_point):
                return cur_zipcode
        except:
            continue
    
    return results[0].zipcode