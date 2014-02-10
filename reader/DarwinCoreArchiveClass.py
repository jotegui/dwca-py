from dwc.reader.RecordSetClass import RecordSet
from dwc.common import MappingError
from dwc.reader.MetafileClass import Metafile
#from xml.dom import minidom
import dwc.common as common
import zipfile
import tarfile

#    TODO:
#    
#    MAIN FUNCTIONALITY
#
#    - Functions for extensions
#    - RecordSet functions for extensions
#    - Improve the warning system. Make extensions warnings append to regular warnings. Add an identification of source of warning (core-loading, extension-loading...)
#    - Unicode
#    - In RecordSet class, when using rename, new term should be added to populatedTerms in the same position
#
#    ADD-ONS FOR SPECIAL CASES
#
#    - Implement multi-location reading of main files
#    - Metafile: Implement variables in default fields
#
#    DOCUMENTATION
#
#    - Update all docstrings
#
#    CONSIDERATIONS (a.k.a. THINGS TO THINK ABOUT)
#
#    - Right now, attributes of dwca instance will be standard terms. What if the <core>.txt has headers in specific language? Do we want to be able to call dwca.localidad instead of (or added to) dwca.locality?
#
#
#    EXTRA
#    
#    - Implement the extraction of metadata (eml.xml or ~) (In extra because of difficulty)
#    - Definir __str__ y/o __repr__ para que devuelvan los metadatos
#    - donde haya problemas de encoding, probar a usar decode("string-escape")
#    	y/o decode("unicode-escape"). Check:
#   		http://stackoverflow.com/questions/14820429/how-do-i-decodestring-escape-in-python3
#   		http://code.activestate.com/recipes/466293-efficient-character-escapes-decoding/
#   		http://mail.python.org/pipermail/python-list/2012-April/622471.html
#   	- explorar la posibilidad de usar with, __enter__ y __exit__ como sustituto
#   		a abrir y cerrar archivos. Check
#   		http://effbot.org/zone/python-with-statement.htm
#   		http://preshing.com/20110920/the-python-with-statement-by-example
#   		www.python.org/dev/peps/pep-0343/ (con muchas ganas...)
#   	- explorar la posibilidad de overridear los __*__ donde * puede ser
#   		cualquiera de los operadores de comparacion, subsets... vamos, facilitar
#   		un poco las cosas para no tener que llamar a las funciones definidas.
#    - explorar la implementacion de archivos de resultados de descargas de GBIF
#    - explorar BeautifulSoup
#    - testear, testear, testear hasta que encontremos fallos


class DarwinCoreArchive(RecordSet):
    """
Class definition for a DarwinCore Archive. The class has an attribute for each
Darwin Core term. Each attribute is a list of the term's value in the records,
stored as text. The idea is to have an easy and fast access to all the
different values of a term among the records, instead of having access to all
the terms of a record. When loading, the initializer may show a warning
reporting non-matching terms. The list values for each term can be accessed by
calling the respective term as an attribute.

WARNING: due to python keyword conflict, the term 'class' cannot be accessed
calling for the 'class' attribute. Instead, call the '_class' attribute. See
examples in the end of this docstring.

Apart from these attributes, the class currently has two special attributes and
four methods: 

    - terms: a list of all the Darwin Core terms.
    - populatedTerms: a list of all the Darwin Core terms which have any
    information.
    - countRecords: a method to count the number of records in the archive.
    - countTerm: a method to extract the frequencies of different values
    in a term. By default returns a dict.
    - countTermCSV: a shortcut for countTerm that returns a
    string ready to be stored in CSV format.
    - countTermTAB: a shortcut for countTerm that returns a
    string ready to be stored in tab-delimited format.
    - countTermValue: a method to count the number of times a given value is in
    the archive.
    - countTermMultiValue: a method to sum the frequencies of different values
    for a given term.

New archives must be initialized passing the path to a valid DarwinCore archive
or an open instance of a file with the file content as argument See docstring in
initialization function. New instances cannot be created without the path to a
valid DarwinCore archive or a reference to a valid DarwinCore file instance.

Examples:

# Load a DarwinCore Archive
dwca = DarwinCoreArchive2('/path/to/DarwinCore/archive.zip')

# See the records' values for the field 'basisOfRecord'
dwca.basisOfRecord # Returns:
['PreservedSpecimen', 'PreservedSpecimen', 'PreservedSpecimen',
'PreservedSpecimen', 'PreservedSpecimen', 'PreservedSpecimen',...]

# See the records' values for the field 'class'
dwca._class # Returns:
['Mammalia', 'Mammalia', 'Mammalia', 'Mammalia', 'Mammalia', 'Mammalia',
'Mammalia', 'Mammalia', 'Mammalia', 'Mammalia', 'Mammalia', 'Mammalia',...]

# Get the number of records:
dwca.countRecords() # 1157

# Get the frequencies of the different values for the term 'order' in CSV format
dwca.countTermCSV('order') # Returns:
order,count
'Rodentia',738
'Carnivora',133
'Sociomorpha',131
'Chiroptera',47
'',27
...

# Get the frequency of a value in a term:
dwca.countTermValue('order','Rodentia') # Returns 738

# Get the sum of the frequencies of a list of values in a term:
dwca.countTermMultiValue('order',['Rodentia','Sociomorpha']) # Returns 869
"""

    def __init__(self, dwca_path):
        """
Initialization function for the DarwinCoreArchive class.
Argument must be the path to a valid DarwinCore archive.

Example:
dwca = DarwinCoreArchive('/path/to/DarwinCore/archive.zip')
"""
#------------------------------------------------------------------------------#
    ##################
    # INITIALIZATION #
    ##################
    
        # Create a container for loading warnings
        self.warnings = []
        
        # Create container for flags
        self.flags = {}
        
        # All DarwinCore Terms and URIs
        self.dwcTerms = {'identificationRemarks': 'http://rs.tdwg.org/dwc/terms/identificationRemarks', 'minimumDepthInMeters': 'http://rs.tdwg.org/dwc/terms/minimumDepthInMeters', 'footprintSRS': 'http://rs.tdwg.org/dwc/terms/footprintSRS', 'verbatimLatitude': 'http://rs.tdwg.org/dwc/terms/verbatimLatitude', 'month': 'http://rs.tdwg.org/dwc/terms/month', 'measurementDeterminedDate': 'http://rs.tdwg.org/dwc/terms/measurementDeterminedDate', 'informationWithheld': 'http://rs.tdwg.org/dwc/terms/informationWithheld', 'lithostratigraphicTerms': 'http://rs.tdwg.org/dwc/terms/lithostratigraphicTerms', 'latestPeriodOrHighestSystem': 'http://rs.tdwg.org/dwc/terms/latestPeriodOrHighestSystem', 'reproductiveCondition': 'http://rs.tdwg.org/dwc/terms/reproductiveCondition', 'continent': 'http://rs.tdwg.org/dwc/terms/continent', 'endDayOfYear': 'http://rs.tdwg.org/dwc/terms/endDayOfYear', 'identificationID': 'http://rs.tdwg.org/dwc/terms/identificationID', 'latestEraOrHighestErathem': 'http://rs.tdwg.org/dwc/terms/latestEraOrHighestErathem', 'occurrenceID': 'http://rs.tdwg.org/dwc/terms/occurrenceID', 'locationAccordingTo': 'http://rs.tdwg.org/dwc/terms/locationAccordingTo', 'latestEpochOrHighestSeries': 'http://rs.tdwg.org/dwc/terms/latestEpochOrHighestSeries', 'coordinateUncertaintyInMeters': 'http://rs.tdwg.org/dwc/terms/coordinateUncertaintyInMeters', 'coordinatePrecision': 'http://rs.tdwg.org/dwc/terms/coordinatePrecision', 'maximumDepthInMeters': 'http://rs.tdwg.org/dwc/terms/maximumDepthInMeters', 'waterBody': 'http://rs.tdwg.org/dwc/terms/waterBody', 'resourceRelationshipID': 'http://rs.tdwg.org/dwc/terms/resourceRelationshipID', 'kingdom': 'http://rs.tdwg.org/dwc/terms/kingdom', 'decimalLatitude': 'http://rs.tdwg.org/dwc/terms/decimalLatitude', 'verbatimTaxonRank': 'http://rs.tdwg.org/dwc/terms/verbatimTaxonRank', 'earliestEraOrLowestErathem': 'http://rs.tdwg.org/dwc/terms/earliestEraOrLowestErathem', 'verbatimCoordinates': 'http://rs.tdwg.org/dwc/terms/verbatimCoordinates', 'acceptedNameUsageID': 'http://rs.tdwg.org/dwc/terms/acceptedNameUsageID', 'infraspecificEpithet': 'http://rs.tdwg.org/dwc/terms/infraspecificEpithet', 'namePublishedIn': 'http://rs.tdwg.org/dwc/terms/namePublishedIn', 'originalNameUsage': 'http://rs.tdwg.org/dwc/terms/originalNameUsage', 'nameAccordingToID': 'http://rs.tdwg.org/dwc/terms/nameAccordingToID', 'dataGeneralizations': 'http://rs.tdwg.org/dwc/terms/dataGeneralizations', 'nomenclaturalStatus': 'http://rs.tdwg.org/dwc/terms/nomenclaturalStatus', 'bibliographicCitation': 'http://purl.org/dc/terms/bibliographicCitation', 'recordNumber': 'http://rs.tdwg.org/dwc/terms/recordNumber', 'day': 'http://rs.tdwg.org/dwc/terms/day', 'individualCount': 'http://rs.tdwg.org/dwc/terms/individualCount', 'type': 'http://purl.org/dc/terms/type', 'measurementType': 'http://rs.tdwg.org/dwc/terms/measurementType', 'institutionID': 'http://rs.tdwg.org/dwc/terms/institutionID', 'georeferenceVerificationStatus': 'http://rs.tdwg.org/dwc/terms/georeferenceVerificationStatus', 'lifeStage': 'http://rs.tdwg.org/dwc/terms/lifeStage', 'measurementUnit': 'http://rs.tdwg.org/dwc/terms/measurementUnit', 'locationRemarks': 'http://rs.tdwg.org/dwc/terms/locationRemarks', 'scientificName': 'http://rs.tdwg.org/dwc/terms/scientificName', 'parentNameUsage': 'http://rs.tdwg.org/dwc/terms/parentNameUsage', 'datasetID': 'http://rs.tdwg.org/dwc/terms/datasetID', 'eventID': 'http://rs.tdwg.org/dwc/terms/eventID', 'lowestBiostratigraphicZone': 'http://rs.tdwg.org/dwc/terms/lowestBiostratigraphicZone', 'habitat': 'http://rs.tdwg.org/dwc/terms/habitat', 'higherGeographyID': 'http://rs.tdwg.org/dwc/terms/higherGeographyID', 'references': 'http://purl.org/dc/terms/references', 'sex': 'http://rs.tdwg.org/dwc/terms/sex', 'accessRights': 'http://purl.org/dc/terms/accessRights', 'scientificNameAuthorship': 'http://rs.tdwg.org/dwc/terms/scientificNameAuthorship', 'associatedTaxa': 'http://rs.tdwg.org/dwc/terms/associatedTaxa', 'year': 'http://rs.tdwg.org/dwc/terms/year', 'taxonRemarks': 'http://rs.tdwg.org/dwc/terms/taxonRemarks', 'rightsHolder': 'http://purl.org/dc/terms/rightsHolder', 'namePublishedInYear': 'http://rs.tdwg.org/dwc/terms/namePublishedInYear', 'identificationVerificationStatus': 'http://rs.tdwg.org/dwc/terms/identificationVerificationStatus', 'eventTime': 'http://rs.tdwg.org/dwc/terms/eventTime', 'basisOfRecord': 'http://rs.tdwg.org/dwc/terms/basisOfRecord', 'latestEonOrHighestEonothem': 'http://rs.tdwg.org/dwc/terms/latestEonOrHighestEonothem', 'otherCatalogNumbers': 'http://rs.tdwg.org/dwc/terms/otherCatalogNumbers', 'georeferenceRemarks': 'http://rs.tdwg.org/dwc/terms/georeferenceRemarks', 'acceptedNameUsage': 'http://rs.tdwg.org/dwc/terms/acceptedNameUsage', 'georeferenceSources': 'http://rs.tdwg.org/dwc/terms/georeferenceSources', 'specificEpithet': 'http://rs.tdwg.org/dwc/terms/specificEpithet', 'verbatimLocality': 'http://rs.tdwg.org/dwc/terms/verbatimLocality', 'identificationReferences': 'http://rs.tdwg.org/dwc/terms/identificationReferences', 'measurementRemarks': 'http://rs.tdwg.org/dwc/terms/measurementRemarks', 'georeferencedBy': 'http://rs.tdwg.org/dwc/terms/georeferencedBy', 'geodeticDatum': 'http://rs.tdwg.org/dwc/terms/geodeticDatum', 'occurrenceRemarks': 'http://rs.tdwg.org/dwc/terms/occurrenceRemarks', 'collectionCode': 'http://rs.tdwg.org/dwc/terms/collectionCode', 'higherGeography': 'http://rs.tdwg.org/dwc/terms/higherGeography', 'nameAccordingTo': 'http://rs.tdwg.org/dwc/terms/nameAccordingTo', 'latestAgeOrHighestStage': 'http://rs.tdwg.org/dwc/terms/latestAgeOrHighestStage', 'fieldNumber': 'http://rs.tdwg.org/dwc/terms/fieldNumber', 'measurementMethod': 'http://rs.tdwg.org/dwc/terms/measurementMethod', 'disposition': 'http://rs.tdwg.org/dwc/terms/disposition', 'earliestEpochOrLowestSeries': 'http://rs.tdwg.org/dwc/terms/earliestEpochOrLowestSeries', 'group': 'http://rs.tdwg.org/dwc/terms/group', 'highestBiostratigraphicZone': 'http://rs.tdwg.org/dwc/terms/highestBiostratigraphicZone', 'ownerInstitutionCode': 'http://rs.tdwg.org/dwc/terms/ownerInstitutionCode', 'scientificNameID': 'http://rs.tdwg.org/dwc/terms/scientificNameID', 'relationshipEstablishedDate': 'http://rs.tdwg.org/dwc/terms/relationshipEstablishedDate', 'earliestAgeOrLowestStage': 'http://rs.tdwg.org/dwc/terms/earliestAgeOrLowestStage', 'country': 'http://rs.tdwg.org/dwc/terms/country', 'measurementDeterminedBy': 'http://rs.tdwg.org/dwc/terms/measurementDeterminedBy', 'decimalLongitude': 'http://rs.tdwg.org/dwc/terms/decimalLongitude', 'locationID': 'http://rs.tdwg.org/dwc/terms/locationID', 'rights': 'http://purl.org/dc/terms/rights', 'relationshipRemarks': 'http://rs.tdwg.org/dwc/terms/relationshipRemarks', 'startDayOfYear': 'http://rs.tdwg.org/dwc/terms/startDayOfYear', 'formation': 'http://rs.tdwg.org/dwc/terms/formation', 'genus': 'http://rs.tdwg.org/dwc/terms/genus', 'family': 'http://rs.tdwg.org/dwc/terms/family', 'collectionID': 'http://rs.tdwg.org/dwc/terms/collectionID', 'dynamicProperties': 'http://rs.tdwg.org/dwc/terms/dynamicProperties', 'eventRemarks': 'http://rs.tdwg.org/dwc/terms/eventRemarks', 'municipality': 'http://rs.tdwg.org/dwc/terms/municipality', 'individualID': 'http://rs.tdwg.org/dwc/terms/individualID', 'footprintWKT': 'http://rs.tdwg.org/dwc/terms/footprintWKT', 'county': 'http://rs.tdwg.org/dwc/terms/county', 'associatedMedia': 'http://rs.tdwg.org/dwc/terms/associatedMedia', 'associatedSequences': 'http://rs.tdwg.org/dwc/terms/associatedSequences', 'subgenus': 'http://rs.tdwg.org/dwc/terms/subgenus', 'footprintSpatialFit': 'http://rs.tdwg.org/dwc/terms/footprintSpatialFit', 'measurementValue': 'http://rs.tdwg.org/dwc/terms/measurementValue', 'higherClassification': 'http://rs.tdwg.org/dwc/terms/higherClassification', 'islandGroup': 'http://rs.tdwg.org/dwc/terms/islandGroup', 'resourceID': 'http://rs.tdwg.org/dwc/terms/resourceID', 'class': 'http://rs.tdwg.org/dwc/terms/class', 'verbatimSRS': 'http://rs.tdwg.org/dwc/terms/verbatimSRS', 'associatedOccurrences': 'http://rs.tdwg.org/dwc/terms/associatedOccurrences', 'catalogNumber': 'http://rs.tdwg.org/dwc/terms/catalogNumber', 'verbatimLongitude': 'http://rs.tdwg.org/dwc/terms/verbatimLongitude', 'preparations': 'http://rs.tdwg.org/dwc/terms/preparations', 'taxonID': 'http://rs.tdwg.org/dwc/terms/taxonID', 'nomenclaturalCode': 'http://rs.tdwg.org/dwc/terms/nomenclaturalCode', 'maximumElevationInMeters': 'http://rs.tdwg.org/dwc/terms/maximumElevationInMeters', 'verbatimCoordinateSystem': 'http://rs.tdwg.org/dwc/terms/verbatimCoordinateSystem', 'measurementID': 'http://rs.tdwg.org/dwc/terms/measurementID', 'relatedResourceID': 'http://rs.tdwg.org/dwc/terms/relatedResourceID', 'datasetName': 'http://rs.tdwg.org/dwc/terms/datasetName', 'earliestEonOrLowestEonothem': 'http://rs.tdwg.org/dwc/terms/earliestEonOrLowestEonothem', 'measurementAccuracy': 'http://rs.tdwg.org/dwc/terms/measurementAccuracy', 'verbatimDepth': 'http://rs.tdwg.org/dwc/terms/verbatimDepth', 'bed': 'http://rs.tdwg.org/dwc/terms/bed', 'georeferencedDate': 'http://rs.tdwg.org/dwc/terms/georeferencedDate', 'behavior': 'http://rs.tdwg.org/dwc/terms/behavior', 'island': 'http://rs.tdwg.org/dwc/terms/island', 'parentNameUsageID': 'http://rs.tdwg.org/dwc/terms/parentNameUsageID', 'minimumElevationInMeters': 'http://rs.tdwg.org/dwc/terms/minimumElevationInMeters', 'occurrenceStatus': 'http://rs.tdwg.org/dwc/terms/occurrenceStatus', 'vernacularName': 'http://rs.tdwg.org/dwc/terms/vernacularName', 'pointRadiusSpatialFit': 'http://rs.tdwg.org/dwc/terms/pointRadiusSpatialFit', 'countryCode': 'http://rs.tdwg.org/dwc/terms/countryCode', 'phylum': 'http://rs.tdwg.org/dwc/terms/phylum', 'institutionCode': 'http://rs.tdwg.org/dwc/terms/institutionCode', 'identificationQualifier': 'http://rs.tdwg.org/dwc/terms/identificationQualifier', 'namePublishedInID': 'http://rs.tdwg.org/dwc/terms/namePublishedInID', 'identifiedBy': 'http://rs.tdwg.org/dwc/terms/identifiedBy', 'earliestPeriodOrLowestSystem': 'http://rs.tdwg.org/dwc/terms/earliestPeriodOrLowestSystem', 'minimumDistanceAboveSurfaceInMeters': 'http://rs.tdwg.org/dwc/terms/minimumDistanceAboveSurfaceInMeters', 'language': 'http://purl.org/dc/terms/language', 'maximumDistanceAboveSurfaceInMeters': 'http://rs.tdwg.org/dwc/terms/maximumDistanceAboveSurfaceInMeters', 'taxonConceptID': 'http://rs.tdwg.org/dwc/terms/taxonConceptID', 'georeferenceProtocol': 'http://rs.tdwg.org/dwc/terms/georeferenceProtocol', 'locality': 'http://rs.tdwg.org/dwc/terms/locality', 'associatedReferences': 'http://rs.tdwg.org/dwc/terms/associatedReferences', 'stateProvince': 'http://rs.tdwg.org/dwc/terms/stateProvince', 'taxonomicStatus': 'http://rs.tdwg.org/dwc/terms/taxonomicStatus', 'relationshipAccordingTo': 'http://rs.tdwg.org/dwc/terms/relationshipAccordingTo', 'member': 'http://rs.tdwg.org/dwc/terms/member', 'relationshipOfResource': 'http://rs.tdwg.org/dwc/terms/relationshipOfResource', 'taxonRank': 'http://rs.tdwg.org/dwc/terms/taxonRank', 'previousIdentifications': 'http://rs.tdwg.org/dwc/terms/previousIdentifications', 'samplingEffort': 'http://rs.tdwg.org/dwc/terms/samplingEffort', 'verbatimElevation': 'http://rs.tdwg.org/dwc/terms/verbatimElevation', 'establishmentMeans': 'http://rs.tdwg.org/dwc/terms/establishmentMeans', 'typeStatus': 'http://rs.tdwg.org/dwc/terms/typeStatus', 'samplingProtocol': 'http://rs.tdwg.org/dwc/terms/samplingProtocol', 'originalNameUsageID': 'http://rs.tdwg.org/dwc/terms/originalNameUsageID', 'eventDate': 'http://rs.tdwg.org/dwc/terms/eventDate', 'geologicalContextID': 'http://rs.tdwg.org/dwc/terms/geologicalContextID', 'fieldNotes': 'http://rs.tdwg.org/dwc/terms/fieldNotes', 'dateIdentified': 'http://rs.tdwg.org/dwc/terms/dateIdentified', 'verbatimEventDate': 'http://rs.tdwg.org/dwc/terms/verbatimEventDate', 'recordedBy': 'http://rs.tdwg.org/dwc/terms/recordedBy', 'modified': 'http://purl.org/dc/terms/modified', 'order': 'http://rs.tdwg.org/dwc/terms/order'}
        
        # Parse and load the compressed file, either a .zip or a .tar.gz
        z = self._loadCompressedFile(dwca_path)            
        
        # Parse the need for a meta.xml
        needsMetafile, list_of_files, headers = self._needsMetafile(z, dwca_path)
        
#------------------------------------------------------------------------------#
    ############
    # METAFILE #
    ############
        
        # Even if there is no need for a metafile, if there IS a metafile, take advantage of it
        if needsMetafile or common._locateFileInZip(z, 'meta.xml'):
            self.metafile = Metafile(z)
            
            # Wrapper for certain key attributes
            self.core = self.metafile.core
            self.extensions = self.metafile.extensions
            self.locations = self.core.locations
            
            # Core field parsing elements
            self.linesTerminatedBy = self.core.linesTerminatedBy
            self.fieldsTerminatedBy = self.core.fieldsTerminatedBy
            self.fieldsEnclosedBy = self.core.fieldsEnclosedBy
            self.ignoreHeaderLines = self.core.ignoreHeaderLines
            self.rowType = self.core.rowType
            self.encoding = self.core.encoding
            self.dateFormat = self.core.dateFormat
        
        else:
            self.metafile = None
            self.extensions = []
            self.locations = list_of_files
            
            # Load defaults except fieldsTerminatedBy and fieldsEnclosedBy, which depends on the file type
            self.linesTerminatedBy = "\n"
            self.ignoreHeaderLines = 1
            self.rowType = "http://rs.tdwg.org/dwc/xsd/simpledarwincore/SimpleDarwinRecord"
            self.encoding = "UTF-8"
            self.dateFormat = "YYYY-MM-DD"
        
        
        # Build populatedTerms
        
        # Container
        self.populatedTerms = []
        
        # If metafile is present, take values from it
        if self.metafile:
            # If field with index = 0 exists, don't add id; else, add id
            if 0 not in self.metafile.core.fields.keys() and self.metafile.core.id.index == 0:
                self.populatedTerms.append('id')
            for index in sorted(self.metafile.core.fields.keys()):
                uri = self.metafile.core.fields[index].term
                for term in self.dwcTerms.keys():
                    if self.dwcTerms[term] == uri:
                        self.populatedTerms.append(str(term))
        
        # If not, build populatedTerms from first row
        else:
            # If meta.xml is not needed, headers are already parsed in the needsMetafile section
            for i in headers:
                self.populatedTerms.append(i.rstrip())
        
        
#------------------------------------------------------------------------------#
    ############
    # METADATA #
    ############
        
        #TODO
        
        
#------------------------------------------------------------------------------#
    ###########
    # CONTENT #
    ###########
        

        # Open the main content file and load the records
        
        # If locations contains only one file
        if len(self.locations) == 1:
            occfile = self.locations[0]
            # Assessment of the core file is made when loading metafile
            content = common._locateFileInZip(z, occfile)
            
            occlines = content.read().split(self.linesTerminatedBy)[self.ignoreHeaderLines:]
            # Remove last newline
            if occlines[-1] == '':
                occlines = occlines[:-1]
            
            # Trying to store values in Field elements and reference them after the import
            # Build main infrastructure
            #for term in self.dwcTerms.keys():
            #    setattr(self, term, [])

            # Main process
            colnames = self.populatedTerms
            warnings = []
            for line in occlines:
                if line[-1] == "\n":
                    line = line[:-1]
                splitline = line.split(self.fieldsTerminatedBy)
                for pos in range(len(colnames)):
                    thiskey = colnames[pos]
                    thisvalue = splitline[pos]
                    # Remove the enclosing characters if present
                    if self.fieldsEnclosedBy != '' and thisvalue[0] == self.fieldsEnclosedBy and thisvalue[-1] == self.fieldsEnclosedBy:
                        thisvalue = thisvalue[1:-1]
                    try:
                        #getattr(self, thiskey).append(thisvalue)
                        self.metafile.core.fields[pos].values.append(thisvalue)
                    except KeyError:
                        self.metafile.core.id.values.append(thisvalue)
                        #if thiskey not in warnings:
                        #    warnings.append(thiskey)
                        #    setattr(self, thiskey, [])
                        #getattr(self, thiskey).append(thisvalue)
                        #self.metafile.core.fields[pos].values.append(thisvalue)

            # Shortcut to the values
            for i in list(range(len(self.populatedTerms))):
                if i == 0:
                    setattr(self, self.populatedTerms[i], self.metafile.core.id)
                else:
                    setattr(self, self.populatedTerms[i], self.metafile.core.fields[i])

        # If locations contains more than one file
        else:
            #TODO
            self.warnings.append("Sorry, multi-file loading of core data is not yet supported. Basic metadata has been parsed but no actual record has been processed.")
        
        # Defaults
        if self.metafile:
            if len(self.metafile.core.defaults) > 0:
                for i in self.metafile.core.defaults:
                    term = str(i.term.split("/")[-1])
                    value = str(i.default)
                    if term in self.populatedTerms:
                        self.warnings.append("'{0}' appears in the core file and as a default field in the metafile. Ignoring the default value.".format(term))
                        continue
                    else:
                        #setattr(self, term, [])
                        self.populatedTerms.append(term)
                        #for i in list(range(self.countRecords())):
                        #    getattr(self, term).append(value)
                        i.values = [value]*len(getattr(self, self.populatedTerms[0]).values)
                        setattr(self, term, i)

        
        # Print warnings
        if len(warnings) > 0:
            for i in warnings:
                self.warnings.append("'{0}' cannot be found in the list of DarwinCore terms. The use of rename or batchRename functions is suggested.".format(i))

        
#------------------------------------------------------------------------------#
    #######
    # END #
    #######
        
        # Print stats from the import
        
        # Total number of records imported
        print "{0} records imported from main file/s".format(len(getattr(self, self.populatedTerms[0]).values))
        
        # Extensions loaded
        if len(self.extensions.keys()) > 0:
            print "{0} extensions loaded: {1}".format(len(self.extensions), ", ".join(self.extensions.keys()))
        
        # Heads up for warnings
        if len(self.warnings) > 0:
            print "IMPORTANT: some warning messages have been stored. To see them, call the function showWarnings()"
            
    
#------------------------------------------------------------------------------#
    ###########
    # METHODS #
    ###########
    
    # BASIC METHODS ARE INHERITED FROM DWC.RECORDSET
    
    # SPECIFIC METHODS

    def _loadCompressedFile(self, dwca_path):
        
        # Check if valid DWCA
        if isinstance(dwca_path, str):
            try:
                f = open(dwca_path,'r')
                f.close()
            except IOError as e:
                raise MappingError('File does not exist')
        else:
            raise MappingError('Argument should be a path to a valid DarwinCore Archive')
        
        # Parse if correct format (zip or gzip) and build tar/zip file
        if dwca_path.endswith('.zip'):
            try:
                z = zipfile.ZipFile(dwca_path)
            except zipfile.BadZipfile as e:
                raise MappingError('Not a valid zip file.')
        elif dwca_path.endswith('.tar.gz'):
            try:
                z = tarfile.open(dwca_path, 'r:gz')
            except tarfile.ReadError:
                raise MappingError('Not a valid tar.gz file.')
        else:
            raise MappingError('Not a valid file type. DarwinCore Archives should be .zip or .tar.gz compressed files')
        
        return z


    def _needsMetafile(self, z, dwca_path):
        """
Checks if the DarwinCore Archive should have a meta.xml file. Cases when meta.xml is NOT needed:
 - One and only one core file, with first row containing headers that correspond to DarwinCore terms, without extensions or metadata file
 - Same as above, but with metadata file called EML.xml. If name is other than EML.xml, metafile is needed
"""
        needsMetafile = False
        headers = None
        
        # List of files other than 'eml.xml' and 'meta.xml'
        list_of_files = [z.namelist()[i] for i in list(range(len(z.namelist()))) if z.namelist()[i] != 'meta.xml' and z.namelist()[i] != 'eml.xml'] if dwca_path.endswith('.zip') else [z.getnames()[i] for i in list(range(len(z.getnames()))) if z.getnames()[i] != 'meta.xml' and z.getnames()[i] != 'eml.xml']

        # If there is more than one file left, metafile is needed        
        if len(list_of_files) > 1:
            needsMetafile = True
        
        # If there is another .xml file, metafile is needed
        elif list_of_files[0].endswith('.xml'):
            needsMetafile = True

        # If first column in single file has terms different than DarwinCore Terms, metafile is needed
        else:
            # Extract first line
            o = common._locateFileInZip(z, list_of_files[0])
            headers_unparsed = o.readline()
            o.close()
            headers = None
            # Split by tabs if txt file
            if list_of_files[0].endswith('.txt'):
                self.fieldsTerminatedBy = "\t"
                self.fieldsEnclosedBy = ""
                headers = headers_unparsed.split("\t")
            else:
                # Split by comma if comma present and semicolon not present
                if "," in headers_unparsed and not ";" in headers_unparsed:
                    self.fieldsTerminatedBy = ","
                    self.fieldsEnclosedBy = "\""
                    headers = headers_unparsed.split(",")
                # Split by semicolon if semicolon present and comma not present
                elif ";" in headers_unparsed and not "," in headers_unparsed:
                    self.fieldsTerminatedBy = ";"
                    self.fieldsEnclosedBy = "\""
                    headers = headers_unparsed.split(";")
            # If separator is not tab, comma or semicolon, metafile is needed
            if headers is None or len (headers) == 1:
                needsMetafile = True
            else:
                # If a single term is not a DarwinCore Term, metafile is needed
                for i in headers:
                    if i.rstrip() not in self.dwcTerms:
                        needsMetafile = True
                        break
        
        return needsMetafile, list_of_files, headers
    
    def showWarnings(self):
        for i in self.warnings:
            print "-",i
        return
    
    def exportContentToCoreFile(self):
        filename = self.rowType.split("/")[-1].lower()+".txt"
        
        newfile = open('./'+filename,'w')
        newfile.write("\t".join(self.populatedTerms))
        newfile.write("\n")
        
        for row in list(range(self.countRecords())):
            line = []
            for col in list(range(len(self.populatedTerms))):
                val = getattr(self, self.populatedTerms[col]).values[row]
                line.append(val)
            newfile.write("\t".join(line))
            newfile.write("\n")

        newfile.close()
        print 'Content exported to {0}'.format(filename)
        return

#------------------------------------------------------------------------------#
    # EXTENSION METHODS
    # TODO
