# TODO:
# Find better resolution maps

import osgeo.ogr
import shapely.wkt

borders_shp = '/home/jotegui/Desktop/TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp'

def checkPointCountryIntersection(decimalLatitudes, decimalLongitudes, countries):
    flagOutside = []
    flagTranspose = []
    flagNegatedLat = []
    flagNegatedLon = []
    flags = {'outsideCountryCoordinates':flagOutside, 'transposedCoordinates':flagTranspose, 'negatedLatitude':flagNegatedLat, 'negatedLongitude':flagNegatedLon}
    countryFeatures = {}
    
    # Load Shapefile
    shapefile = osgeo.ogr.Open(borders_shp)
    # Load country border layer
    layer = shapefile.GetLayer(0)
    
    for i in range(len(decimalLatitudes)):
        
        # Extract values
        country = countries[i]
        decimalLatitude = decimalLatitudes[i]
        decimalLongitude = decimalLongitudes[i]
        if len(country) < 2:
            for i in flags.keys():
                flags[i].append(None)
            continue
        elif len(country) == 2:
            countryField = "ISO2"
        elif len(country) == 3:
            countryField = "ISO3"
        else:
            countryField = "NAME"
        
        # Load current country feature
        if country not in countryFeatures.keys():
            for i in range(layer.GetFeatureCount()):
                if layer.GetFeature(i).GetField(countryField) == country:
                    feature = layer.GetFeature(i)
            countryFeatures[country] = feature
        else:
            feature = countryFeatures[country]
        
        # Extract geometry for current country
        geometry = feature.GetGeometryRef()
        # Build WKT for current country
        polywkt = geometry.ExportToWkt()
        # Build polygon
        polygon = shapely.wkt.loads(polywkt)

        # Build WKT for current point
        pointwkt = "POINT({0} {1})".format(decimalLongitude, decimalLatitude)
        # Build point
        try:
            point = shapely.wkt.loads(pointwkt)
        except:
            for i in flags.keys():
                flags[i].append(None)
            continue
        
        # Try to intersect
        goodpoint = polygon.contains(point)
        # Check if successful
        if goodpoint is True:
            for i in flags.keys():
                flags[i].append(0)
        else:
            flags['outsideCountryCoordinates'].append(1)
            
            # Check transpose
            pointwkt = "POINT({0} {1})".format(float(decimalLatitude), float(decimalLongitude))
            point = shapely.wkt.loads(pointwkt)
            goodpoint = polygon.contains(point)
            if goodpoint is True:
                flags['transposedCoordinates'].append(1)
                flags['negatedLatitude'].append(0)
                flags['negatedLongitude'].append(0)
            else:
            
                # Check negatedLat
                pointwkt = "POINT({0} {1})".format(float(decimalLongitude), -float(decimalLatitude))
                point = shapely.wkt.loads(pointwkt)
                goodpoint = polygon.contains(point)
                if goodpoint is True:
                    flags['transposedCoordinates'].append(0)
                    flags['negatedLatitude'].append(1)
                    flags['negatedLongitude'].append(0)
                else:
                
                    # Check negatedLon
                    pointwkt = "POINT({0} {1})".format(-float(decimalLongitude), float(decimalLatitude))
                    point = shapely.wkt.loads(pointwkt)
                    goodpoint = polygon.contains(point)
                    if goodpoint is True:
                        flags['transposedCoordinates'].append(0)
                        flags['negatedLatitude'].append(0)
                        flags['negatedLongitude'].append(1)
                    else:
                
                        # Check negatedLatLon
                        pointwkt = "POINT({0} {1})".format(-float(decimalLongitude), -float(decimalLatitude))
                        point = shapely.wkt.loads(pointwkt)
                        goodpoint = polygon.contains(point)
                        if goodpoint is True:
                            flags['transposedCoordinates'].append(0)
                            flags['negatedLatitude'].append(1)
                            flags['negatedLongitude'].append(1)
                        else:
                
                            # Check transposed + negatedLat
                            pointwkt = "POINT({0} {1})".format(-float(decimalLatitude), float(decimalLongitude))
                            point = shapely.wkt.loads(pointwkt)
                            goodpoint = polygon.contains(point)
                            if goodpoint is True:
                                flags['transposedCoordinates'].append(1)
                                flags['negatedLatitude'].append(1)
                                flags['negatedLongitude'].append(0)
                            else:
                
                                # Check transposed + negatedLon
                                pointwkt = "POINT({0} {1})".format(float(decimalLatitude), -float(decimalLongitude))
                                point = shapely.wkt.loads(pointwkt)
                                goodpoint = polygon.contains(point)
                                if goodpoint is True:
                                    flags['transposedCoordinates'].append(1)
                                    flags['negatedLatitude'].append(0)
                                    flags['negatedLongitude'].append(1)
                                else:
                
                                    # Check transposed + negatedLatLon
                                    pointwkt = "POINT({0} {1})".format(-float(decimalLatitude), -float(decimalLongitude))
                                    point = shapely.wkt.loads(pointwkt)
                                    goodpoint = polygon.contains(point)
                                    if goodpoint is True:
                                        flags['transposedCoordinates'].append(1)
                                        flags['negatedLatitude'].append(1)
                                        flags['negatedLongitude'].append(1)
                                    else:
                                        flags['transposedCoordinates'].append(0)
                                        flags['negatedLatitude'].append(0)
                                        flags['negatedLongitude'].append(0)
    
    return flags

if __name__ == "__main__":
    decimalLatitudes = [40.0678, 40.0678]
    decimalLongitudes = [-105.244, 105.244]
    countries = ["US","US"]
    countryFields = ["ISO2","ISO2"]
    flag = checkPointCountryIntersection(decimalLatitudes, decimalLongitudes, countries, countryFields)
    print flag
