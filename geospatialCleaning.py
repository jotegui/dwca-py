## FLAGGERS ##

def flagNoCoords(rs, latitude_field = 'decimalLatitude', longitude_field = 'decimalLongitude'):
    """
Returns a list of indexes for the records that show no coordinates in the collection.
"""
    try:
        rs.checkTerms([latitude_field, longitude_field])
        return [True if getattr(rs, latitude_field)[x] == '' and getattr(rs, longitude_field)[x] == '' else False for x in range(rs.countRecords())]
    except:
        return []


def flagHalfCoords(rs, latitude_field = 'decimalLatitude', longitude_field = 'decimalLongitude'):
    """
Returns a list of indexes for the records that show only one coordinate in the collection.
"""
    try:
        rs.checkTerms([latitude_field, longitude_field])
        return [True if bool(getattr(rs, latitude_field)[x] == '') ^ bool(getattr(rs, longitude_field)[x] == '') else False for x in range(rs.countRecords())]
    except:
        return []
    

def flagNoCountry(rs, country_field = 'country'):
    """
Returns a list of indexes for the records that show no country in the collection.
"""
    try:
        rs.checkTerms([country_field])
        return [True if getattr(rs, country_field)[x] == '' else False for x in range(rs.countRecords())]
    except:
        return []


def flagZero(rs, latitude_field = 'decimalLatitude', longitude_field = 'decimalLongitude'):
    """
Returns a list of indexes for the records that have both coordinates equal to zero (0).
"""
    try:
        rs.checkTerms([latitude_field, longitude_field])
        return [True if getattr(rs, latitude_field)[x] == '0' and getattr(rs, longitude_field)[x] == '0' else False for x in range(rs.countRecords())]
    except:
        return []


def flagTransposed(rs, latitude_field = 'decimalLatitude', longitude_field = 'decimalLongitude'):
    """
Returns a list of indexes for the records that have swapped coordinates.
"""
    try:
        rs.checkTerms([latitude_field, longitude_field])
        return [True if getattr(rs, latitude_field)[x].isdigit() is True and getattr(rs, longitude_field)[x].isdigit() is True and abs(float(getattr(rs, latitude_field)[x]))>90 and abs(float(getattr(rs, longitude_field)[x]))<=90 else False for x in range(rs.countRecords())]
    except:
        return []


def addFlagField(rs, field, content):
    """
Creates the new flag fields in a collection.
"""
    setattr(rs, 'flag'+field, content)
    rs.populatedTerms.append('flag'+field)
    return



## SOLVERS ##

def solveTransposed(rs, latitude_field = 'decimalLatitude', longitude_field = 'decimalLongitude'):
    pass

def solveZero(rs, latitude_field = 'decimalLatitude', longitude_field = 'decimalLongitude'):
    pass



## RUN ALL ##

def geoCleaningFlagging(rs, field_names = {'latitude_field':'decimalLatitude', 'longitude_field':'decimalLongitude', 'country_field':'country'}):
    """
Runs all geospatial cleaning functions on the given collection.
"""
    import copy
    rs_copy = copy.deepcopy(rs)    

    # Coordinate check
    try:
        rs.checkTerms([field_names['latitude_field'], field_names['longitude_field']])

        noCoords = flagNoCoords(rs, field_names['latitude_field'], field_names['longitude_field'])
        addFlagField(rs_copy, 'NoCoordinates', noCoords)
        halfCoords = flagHalfCoords(rs, field_names['latitude_field'], field_names['longitude_field'])
        addFlagField(rs_copy, 'HalfCoordinates', halfCoords)
        zero = flagZero(rs, field_names['latitude_field'], field_names['longitude_field'])
        addFlagField(rs_copy, 'Zero', zero)
        transposed = flagTransposed(rs, field_names['latitude_field'], field_names['longitude_field'])
        addFlagField(rs_copy, 'Transposed', transposed)
    
    except:
        print "No coordinate fields found, skipping some tests"
    
    # Country check
    try:
        rs.checkTerms(field_names['country_field'])
    
        noCountry = flagNoCountry(rs, field_names['country_field'])
        addFlagField(rs_copy, 'NoCountry', noCountry)
    
    except:
        print "No country field found, skipping some tests"
    
    return rs_copy

def geoCleaningSolving(rs, field_names = {'latitude_field':'decimalLatitude', 'longitude_field':'decimalLongitude', 'country_field':'country'}):
    pass
