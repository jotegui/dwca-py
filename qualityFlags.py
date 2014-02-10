from dwc.FlagClass import Flag
from dwc.geospatialFlagging import checkPointCountryIntersection

#===========================#
# COMMON FLAGGING FUNCTIONS #
#===========================#

def addFlag(dwca, name, flag):
    dwca.flags[name] = Flag(name, flag)
    return

def flagRangedInteger(dwca, term, vals, minvalue, maxvalue):
    flagRangedNumeric(dwca, term, vals, minvalue, maxvalue, True)
    return

def flagRangedNumeric(dwca, term, vals, minvalue, maxvalue, checkInteger = False):

    valOutOfRange = []
    valNonNumeric = []
    valNonInteger = []
    valEmpty = []
    
    outOfRangeName = str(term)+'OutOfRange'
    nonNumericName = str(term)+'NonNumeric'
    nonIntegerName = str(term)+'NonInteger'
    emptyName = str(term)+'Empty'
    
    for val in vals:
        try:
            currval = int(val)
        except ValueError:
            if val=='':
                valEmpty.append(1)
                valOutOfRange.append(0)
                valNonNumeric.append(0)
                valNonInteger.append(0)
            else:
                valEmpty.append(0)
                valOutOfRange.append(0)
                valNonNumeric.append(1)
                valNonInteger.append(0)
            continue
        
        valEmpty.append(0)
        valNonNumeric.append(1)
        
        if checkInteger and int(val) != val:
            valNonInteger.append(1)
        else:
            valNonInteger.append(0)
        
        
        if currval > maxvalue or currval < minvalue:
            valOutOfRange.append(1)
        else:
            valOutOfRange.append(0)
    

    
    addFlag(dwca, outOfRangeName, valOutOfRange)
    addFlag(dwca, nonNumericName, valNonNumeric)
    addFlag(dwca, emptyName, valEmpty)
    
    if checkInteger:
        addFlag(dwca, nonIntegerName, valNonInteger)
    
    return

#===============#
# DATE ELEMENTS #
#===============#

def flagYear(dwca):
    from datetime import datetime
    
    try:
        vals = dwca.year.values
    except:
        return None
    
    minvalue = 1750
    maxvalue = datetime.now().year
    
    flagRangedInteger(dwca, 'year', vals, minvalue, maxvalue)

    return

def flagMonth(dwca):
    
    try:
        vals = dwca.month.values
    except:
        return None
    
    minvalue = 1
    maxvalue = 12
    
    flagRangedInteger(dwca, 'month', vals, minvalue, maxvalue)

    return

#=====================#
# GEOSPATIAL ELEMENTS #
#=====================#

def flagCoordinates(dwca):

    try:
        latitude = dwca.decimalLatitude.values
        longitude = dwca.decimalLongitude.values
    except:
        return None
    
    missingCoordinates = []
    nonNumericCoordinates = []
    zeroCoordinates = []
    transposedCoordinates = []
    
    for i in list(range(len(latitude))):
        
        lat = latitude[i]
        lon = longitude[i]
        
        # Missing coordinates
        if lat == "" or lon == "":
            missingCoordinates.append(1)
            continue
        else:
            missingCoordinates.append(0)
        
        # Coordinates not a number
        try:
            float(lat) and float(lon)
        except:
            nonNumericCoordinates.append(1)
            continue
        nonNumericCoordinates.append(0)
        
        lat = float(lat)
        lon = float(lon)
        
        # Zeroes
        if lat == 0 and lon == 0:
            zeroCoordinates.append(1)
        else:
            zeroCoordinates.append(0)
        
        # Transposed
        if abs(lat) > 90 and abs(lon) < 180:
            transposedCoordinates.append(1)
        else:
            transposedCoordinates.append(0)
        
    
    # Add flags
    addFlag(dwca, 'missingCoordinates', missingCoordinates)
    addFlag(dwca, 'nonNumericCoordinates', nonNumericCoordinates)
    addFlag(dwca, 'zeroCoordinates', zeroCoordinates)
    addFlag(dwca, 'outOfWorldCoordinates', transposedCoordinates)
    
    return

def flagCoordinatesCountry(dwca):
    lats = dwca.decimalLatitude.values
    lons = dwca.decimalLongitude.values
    countries = dwca.country.values
    
    flags = checkPointCountryIntersection(lats, lons, countries)
    
    for i in flags.keys():
        addFlag(dwca, i, flags[i])
    
    return
