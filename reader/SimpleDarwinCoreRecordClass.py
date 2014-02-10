class SimpleDarwinCoreRecord(object):
	"""
Class definition for a DarwinCore record, following the SimpleDarwinCore schema.
Provides an attribute for each of the Simple DarwinCore terms.
Besides, this class has two methods:
	- getTerms: returns a list of all the DarwinCore Terms
	- getPopulatedTerms: returns a list of all the DarwinCore Terms that contain
	any information

INITIALIZATION:
New records can be initialized passing a dictionary with the terms and values as
an argument. Also, empty records can be created to be populated with python
property setters.

IMPORTANT: Due to python keyword conflict, the setter for the class term is
inactive. This doesn't affect the dictionary or the automatic imports (see
next). If needed, class value can be added to the _class variable name.

Note: the DarwinCoreArchive class implements a method for importing Simple
DarwinCore records automatically from a DarwinCore archive.See module
DarwinCoreArchiveClass for more information.

Example:
# Create an empty record:
dwcr = SimpleDarwinCoreRecord()
# Populate basisOfRecord term
dwcr.basisOfRecord = 'PreservedSpecimen'
# Populate class term
dwcr._class = 'Aves'
# Create a dictionary with values for the terms
record_values = {
	'basisOfRecord': 'PreservedSpecimen',
	'class' : 'Aves'
}
# Create a new record with given values
dwcr2 = SimpleDarwinCoreRecord(record_values)
"""

	# Initialization function

	def __init__(self, record_dict = {}):
		"""
Initialization function for the SimpleDarwinCoreRecord class. Can be called
without argument to create an empty record. Argument, if passed, must be a
dictionary with the values for the terms.

Example:
record_values = {'basisOfRecord': 'PreservedSpecimen', 'class': 'Aves'}
dwcr = SimpleDarwinCoreRecord(record_values)
"""
	
	# DARWINCORE TERMS (as appear in http://rs.tdwg.org/dwc/terms/index.htm)

	# RECORD-LEVEL TERMS

		self._type = None
		self._modified = None
		self._language = None
		self._rights = None
		self._rightsHolder = None
		self._accessRights = None
		self._bibliographicCitation = None
		self._references = None
		
		self._institutionID = None
		self._collectionID = None
		self._datasetID = None
		self._institutionCode = None
		self._collectionCode = None
		self._datasetName = None
		self._ownerInstitutionCode = None
		self._basisOfRecord = None
		self._informationWithheld = None
		self._dataGeneralizations = None
		self._dynamicProperties = None
		
		# Occurrence Terms
		self._occurrenceID = None
		self._catalogNumber = None
		self._occurrenceRemarks = None
		self._recordNumber = None
		self._recordedBy = None
		self._individualID = None
		self._individualCount = None
		self._sex = None
		self._lifeStage = None
		self._reproductiveCondition = None
		self._behavior = None
		self._establishmentMeans = None
		self._occurrenceStatus = None
		self._preparations = None
		self._disposition = None
		self._otherCatalogNumbers = None
		self._previousIdentifications = None
		self._associatedMedia = None
		self._associatedReferences = None
		self._associatedOccurrences = None
		self._associatedSequences = None
		self._associatedTaxa = None
				
		# Event Terms
		self._eventID = None
		self._samplingProtocol = None
		self._samplingEffort = None
		self._eventDate = None
		self._eventTime = None
		self._startDayOfYear = None
		self._endDayOfYear = None
		self._year = None
		self._month = None
		self._day = None
		self._verbatimEventDate = None
		self._habitat = None
		self._fieldNumber = None
		self._fieldNotes = None
		self._eventRemarks = None
		
		# Location Terms
		self._locationID = None
		self._higherGeographyID = None
		self._higherGeography = None
		self._continent = None
		self._waterBody = None
		self._islandGroup = None
		self._island = None
		self._country = None
		self._countryCode = None
		self._stateProvince = None
		self._county = None
		self._municipality = None
		self._locality = None
		self._verbatimLocality = None
		self._verbatimElevation = None
		self._minimumElevationInMeters = None
		self._maximumElevationInMeters = None
		self._verbatimDepth = None
		self._minimumDepthInMeters = None
		self._maximumDepthInMeters = None
		self._minimumDistanceAboveSurfaceInMeters = None
		self._maximumDistanceAboveSurfaceInMeters = None
		self._locationAccordingTo = None
		self._locationRemarks = None
		self._verbatimCoordinates = None
		self._verbatimLatitude = None
		self._verbatimLongitude = None
		self._verbatimCoordinateSystem = None
		self._verbatimSRS = None
		self._decimalLatitude = None
		self._decimalLongitude = None
		self._geodeticDatum = None
		self._coordinateUncertaintyInMeters = None
		self._coordinatePrecision = None
		self._pointRadiusSpatialFit = None
		self._footprintWKT = None
		self._footprintSRS = None
		self._footprintSpatialFit = None
		self._georeferencedBy = None
		self._georeferencedDate = None
		self._georeferenceProtocol = None
		self._georeferenceSources = None
		self._georeferenceVerificationStatus = None
		self._georeferenceRemarks = None
		
		# GeologicalContext Terms
		self._geologicalContextID = None
		self._earliestEonOrLowestEonothem = None
		self._latestEonOrHighestEonothem = None
		self._earliestEraOrLowestErathem = None
		self._latestEraOrHighestErathem = None
		self._earliestPeriodOrLowestSystem = None
		self._latestPeriodOrHighestSystem = None
		self._earliestEpochOrLowestSeries = None
		self._latestEpochOrHighestSeries = None
		self._earliestAgeOrLowestStage = None
		self._latestAgeOrHighestStage = None
		self._lowestBiostratigraphicZone = None
		self._highestBiostratigraphicZone = None
		self._lithostratigraphicTerms = None
		self._group = None
		self._formation = None
		self._member = None
		self._bed = None
		
		# Identification Terms
		self._identificationID = None
		self._identifiedBy = None
		self._dateIdentified = None
		self._identificationReferences = None
		self._identificationVerificationStatus = None
		self._identificationRemarks = None
		self._identificationQualifier = None
		self._typeStatus = None
		
		# Taxon Terms
		self._taxonID = None
		self._scientificNameID = None
		self._acceptedNameUsageID = None
		self._parentNameUsageID = None
		self._originalNameUsageID = None
		self._nameAccordingToID = None
		self._namePublishedInID = None
		self._taxonConceptID = None
		self._scientificName = None
		self._acceptedNameUsage = None
		self._parentNameUsage = None
		self._originalNameUsage = None
		self._nameAccordingTo = None
		self._namePublishedIn = None
		self._namePublishedInYear = None
		self._higherClassification = None
		self._kingdom = None
		self._phylum = None
		self._class = None
		self._order = None
		self._family = None
		self._genus = None
		self._subgenus = None
		self._specificEpithet = None
		self._infraspecificEpithet = None
		self._taxonRank = None
		self._verbatimTaxonRank = None
		self._scientificNameAuthorship = None
		self._vernacularName = None
		self._nomenclaturalCode = None
		self._taxonomicStatus = None
		self._nomenclaturalStatus = None
		self._taxonRemarks = None

		# Data loading function
		for term in record_dict.keys():
			setattr(self, "_"+term, record_dict[term])

	# Common functions

	def getTerms(self):
		"""Returns a list with all the available DarwinCore terms.
"""
		terms = sorted(self.__dict__)
		for i in range(len(terms)):
			terms[i] = terms[i][1:]
		return terms
	
	def getPopulatedTerms(self):
		""" Returns a list with all the DarwinCore terms that contain any information.
"""
		terms = sorted(self.__dict__)
		final = []
		for i in terms:
			if getattr(self, i) != None:
				final.append(i[1:])
		return final
	
	# PYTHONIC GETTERS AND SETTERS

	@property
	def type(self):
		return self._type
	@type.setter
	def type(self, value):
		self._type = value

	@property
	def modified(self):
		return self._modified
	@modified.setter
	def modified(self, value):
		self._modified = value

	@property
	def language(self):
		return self._language
	@language.setter
	def language(self, value):
		self._language = value

	@property
	def rights(self):
		return self._rights
	@rights.setter
	def rights(self, value):
		self._rights = value

	@property
	def rightsHolder(self):
		return self._rightsHolder
	@rightsHolder.setter
	def rightsHolder(self, value):
		self._rightsHolder = value

	@property
	def accessRights(self):
		return self._accessRights
	@accessRights.setter
	def accessRights(self, value):
		self._accessRights = value

	@property
	def bibliographicCitation(self):
		return self._bibliographicCitation
	@bibliographicCitation.setter
	def bibliographicCitation(self, value):
		self._bibliographicCitation = value

	@property
	def references(self):
		return self._references
	@references.setter
	def references(self, value):
		self._references = value

	@property
	def institutionID(self):
		return self._institutionID
	@institutionID.setter
	def institutionID(self, value):
		self._institutionID = value

	@property
	def collectionID(self):
		return self._collectionID
	@collectionID.setter
	def collectionID(self, value):
		self._collectionID = value

	@property
	def datasetID(self):
		return self._datasetID
	@datasetID.setter
	def datasetID(self, value):
		self._datasetID = value

	@property
	def institutionCode(self):
		return self._institutionCode
	@institutionCode.setter
	def institutionCode(self, value):
		self._institutionCode = value

	@property
	def collectionCode(self):
		return self._collectionCode
	@collectionCode.setter
	def collectionCode(self, value):
		self._collectionCode = value

	@property
	def datasetName(self):
		return self._datasetName
	@datasetName.setter
	def datasetName(self, value):
		self._datasetName = value

	@property
	def ownerInstitutionCode(self):
		return self._ownerInstitutionCode
	@ownerInstitutionCode.setter
	def ownerInstitutionCode(self, value):
		self._ownerInstitutionCode = value

	@property
	def basisOfRecord(self):
		return self._basisOfRecord
	@basisOfRecord.setter
	def basisOfRecord(self, value):
		self._basisOfRecord = value

	@property
	def informationWithheld(self):
		return self._informationWithheld
	@informationWithheld.setter
	def informationWithheld(self, value):
		self._informationWithheld = value

	@property
	def dataGeneralizations(self):
		return self._dataGeneralizations
	@dataGeneralizations.setter
	def dataGeneralizations(self, value):
		self._dataGeneralizations = value

	@property
	def dynamicProperties(self):
		return self._dynamicProperties
	@dynamicProperties.setter
	def dynamicProperties(self, value):
		self._dynamicProperties = value

# Occurrence Terms

	@property
	def occurrenceID(self):
		return self._occurrenceID
	@occurrenceID.setter
	def occurrenceID(self, value):
		self._occurrenceID = value

	@property
	def catalogNumber(self):
		return self._catalogNumber
	@catalogNumber.setter
	def catalogNumber(self, value):
		self._catalogNumber = value

	@property
	def occurrenceRemarks(self):
		return self._occurrenceRemarks
	@occurrenceRemarks.setter
	def occurrenceRemarks(self, value):
		self._occurrenceRemarks = value

	@property
	def recordNumber(self):
		return self._recordNumber
	@recordNumber.setter
	def recordNumber(self, value):
		self._recordNumber = value

	@property
	def recordedBy(self):
		return self._recordedBy
	@recordedBy.setter
	def recordedBy(self, value):
		self._recordedBy = value

	@property
	def individualID(self):
		return self._individualID
	@individualID.setter
	def individualID(self, value):
		self._individualID = value

	@property
	def individualCount(self):
		return self._individualCount
	@individualCount.setter
	def individualCount(self, value):
		self._individualCount = value

	@property
	def sex(self):
		return self._sex
	@sex.setter
	def sex(self, value):
		self._sex = value

	@property
	def lifeStage(self):
		return self._lifeStage
	@lifeStage.setter
	def lifeStage(self, value):
		self._lifeStage = value

	@property
	def reproductiveCondition(self):
		return self._reproductiveCondition
	@reproductiveCondition.setter
	def reproductiveCondition(self, value):
		self._reproductiveCondition = value

	@property
	def behavior(self):
		return self._behavior
	@behavior.setter
	def behavior(self, value):
		self._behavior = value

	@property
	def establishmentMeans(self):
		return self._establishmentMeans
	@establishmentMeans.setter
	def establishmentMeans(self, value):
		self._establishmentMeans = value

	@property
	def occurrenceStatus(self):
		return self._occurrenceStatus
	@occurrenceStatus.setter
	def occurrenceStatus(self, value):
		self._occurrenceStatus = value

	@property
	def preparations(self):
		return self._preparations
	@preparations.setter
	def preparations(self, value):
		self._preparations = value

	@property
	def disposition(self):
		return self._disposition
	@disposition.setter
	def disposition(self, value):
		self._disposition = value

	@property
	def otherCatalogNumbers(self):
		return self._otherCatalogNumbers
	@otherCatalogNumbers.setter
	def otherCatalogNumbers(self, value):
		self._otherCatalogNumbers = value

	@property
	def previousIdentifications(self):
		return self._previousIdentifications
	@previousIdentifications.setter
	def previousIdentifications(self, value):
		self._previousIdentifications = value

	@property
	def associatedMedia(self):
		return self._associatedMedia
	@associatedMedia.setter
	def associatedMedia(self, value):
		self._associatedMedia = value

	@property
	def associatedReferences(self):
		return self._associatedReferences
	@associatedReferences.setter
	def associatedReferences(self, value):
		self._associatedReferences = value

	@property
	def associatedOccurrences(self):
		return self._associatedOccurrences
	@associatedOccurrences.setter
	def associatedOccurrences(self, value):
		self._associatedOccurrences = value

	@property
	def associatedSequences(self):
		return self._associatedSequences
	@associatedSequences.setter
	def associatedSequences(self, value):
		self._associatedSequences = value

	@property
	def associatedTaxa(self):
		return self._associatedTaxa
	@associatedTaxa.setter
	def associatedTaxa(self, value):
		self._associatedTaxa = value

# Event Terms

	@property
	def eventID(self):
		return self._eventID
	@eventID.setter
	def eventID(self, value):
		self._eventID = value

	@property
	def samplingProtocol(self):
		return self._samplingProtocol
	@samplingProtocol.setter
	def samplingProtocol(self, value):
		self._samplingProtocol = value

	@property
	def samplingEffort(self):
		return self._samplingEffort
	@samplingEffort.setter
	def samplingEffort(self, value):
		self._samplingEffort = value

	@property
	def eventDate(self):
		return self._eventDate
	@eventDate.setter
	def eventDate(self, value):
		self._eventDate = value

	@property
	def eventTime(self):
		return self._eventTime
	@eventTime.setter
	def eventTime(self, value):
		self._eventTime = value

	@property
	def startDayOfYear(self):
		return self._startDayOfYear
	@startDayOfYear.setter
	def startDayOfYear(self, value):
		self._startDayOfYear = value

	@property
	def endDayOfYear(self):
		return self._endDayOfYear
	@endDayOfYear.setter
	def endDayOfYear(self, value):
		self._endDayOfYear = value

	@property
	def year(self):
		return self._year
	@year.setter
	def year(self, value):
		self._year = value

	@property
	def month(self):
		return self._month
	@month.setter
	def month(self, value):
		self._month = value

	@property
	def day(self):
		return self._day
	@day.setter
	def day(self, value):
		self._day = value

	@property
	def verbatimEventDate(self):
		return self._verbatimEventDate
	@verbatimEventDate.setter
	def verbatimEventDate(self, value):
		self._verbatimEventDate = value

	@property
	def habitat(self):
		return self._habitat
	@habitat.setter
	def habitat(self, value):
		self._habitat = value

	@property
	def fieldNumber(self):
		return self._fieldNumber
	@fieldNumber.setter
	def fieldNumber(self, value):
		self._fieldNumber = value

	@property
	def fieldNotes(self):
		return self._fieldNotes
	@fieldNotes.setter
	def fieldNotes(self, value):
		self._fieldNotes = value

	@property
	def eventRemarks(self):
		return self._eventRemarks
	@eventRemarks.setter
	def eventRemarks(self, value):
		self._eventRemarks = value

# Location Terms

	@property
	def locationID(self):
		return self._locationID
	@locationID.setter
	def locationID(self, value):
		self._locationID = value

	@property
	def higherGeographyID(self):
		return self._higherGeographyID
	@higherGeographyID.setter
	def higherGeographyID(self, value):
		self._higherGeographyID = value

	@property
	def higherGeography(self):
		return self._higherGeography
	@higherGeography.setter
	def higherGeography(self, value):
		self._higherGeography = value

	@property
	def continent(self):
		return self._continent
	@continent.setter
	def continent(self, value):
		self._continent = value

	@property
	def waterBody(self):
		return self._waterBody
	@waterBody.setter
	def waterBody(self, value):
		self._waterBody = value

	@property
	def islandGroup(self):
		return self._islandGroup
	@islandGroup.setter
	def islandGroup(self, value):
		self._islandGroup = value

	@property
	def island(self):
		return self._island
	@island.setter
	def island(self, value):
		self._island = value

	@property
	def country(self):
		return self._country
	@country.setter
	def country(self, value):
		self._country = value

	@property
	def countryCode(self):
		return self._countryCode
	@countryCode.setter
	def countryCode(self, value):
		self._countryCode = value

	@property
	def stateProvince(self):
		return self._stateProvince
	@stateProvince.setter
	def stateProvince(self, value):
		self._stateProvince = value

	@property
	def county(self):
		return self._county
	@county.setter
	def county(self, value):
		self._county = value

	@property
	def municipality(self):
		return self._municipality
	@municipality.setter
	def municipality(self, value):
		self._municipality = value

	@property
	def locality(self):
		return self._locality
	@locality.setter
	def locality(self, value):
		self._locality = value

	@property
	def verbatimLocality(self):
		return self._verbatimLocality
	@verbatimLocality.setter
	def verbatimLocality(self, value):
		self._verbatimLocality = value

	@property
	def verbatimElevation(self):
		return self._verbatimElevation
	@verbatimElevation.setter
	def verbatimElevation(self, value):
		self._verbatimElevation = value

	@property
	def minimumElevationInMeters(self):
		return self._minimumElevationInMeters
	@minimumElevationInMeters.setter
	def minimumElevationInMeters(self, value):
		self._minimumElevationInMeters = value

	@property
	def maximumElevationInMeters(self):
		return self._maximumElevationInMeters
	@maximumElevationInMeters.setter
	def maximumElevationInMeters(self, value):
		self._maximumElevationInMeters = value

	@property
	def verbatimDepth(self):
		return self._verbatimDepth
	@verbatimDepth.setter
	def verbatimDepth(self, value):
		self._verbatimDepth = value

	@property
	def minimumDepthInMeters(self):
		return self._minimumDepthInMeters
	@minimumDepthInMeters.setter
	def minimumDepthInMeters(self, value):
		self._minimumDepthInMeters = value

	@property
	def maximumDepthInMeters(self):
		return self._maximumDepthInMeters
	@maximumDepthInMeters.setter
	def maximumDepthInMeters(self, value):
		self._maximumDepthInMeters = value

	@property
	def minimumDistanceAboveSurfaceInMeters(self):
		return self._minimumDistanceAboveSurfaceInMeters
	@minimumDistanceAboveSurfaceInMeters.setter
	def minimumDistanceAboveSurfaceInMeters(self, value):
		self._minimumDistanceAboveSurfaceInMeters = value

	@property
	def maximumDistanceAboveSurfaceInMeters(self):
		return self._maximumDistanceAboveSurfaceInMeters
	@maximumDistanceAboveSurfaceInMeters.setter
	def maximumDistanceAboveSurfaceInMeters(self, value):
		self._maximumDistanceAboveSurfaceInMeters = value

	@property
	def locationAccordingTo(self):
		return self._locationAccordingTo
	@locationAccordingTo.setter
	def locationAccordingTo(self, value):
		self._locationAccordingTo = value

	@property
	def locationRemarks(self):
		return self._locationRemarks
	@locationRemarks.setter
	def locationRemarks(self, value):
		self._locationRemarks = value

	@property
	def verbatimCoordinates(self):
		return self._verbatimCoordinates
	@verbatimCoordinates.setter
	def verbatimCoordinates(self, value):
		self._verbatimCoordinates = value

	@property
	def verbatimLatitude(self):
		return self._verbatimLatitude
	@verbatimLatitude.setter
	def verbatimLatitude(self, value):
		self._verbatimLatitude = value

	@property
	def verbatimLongitude(self):
		return self._verbatimLongitude
	@verbatimLongitude.setter
	def verbatimLongitude(self, value):
		self._verbatimLongitude = value

	@property
	def verbatimCoordinateSystem(self):
		return self._verbatimCoordinateSystem
	@verbatimCoordinateSystem.setter
	def verbatimCoordinateSystem(self, value):
		self._verbatimCoordinateSystem = value

	@property
	def verbatimSRS(self):
		return self._verbatimSRS
	@verbatimSRS.setter
	def verbatimSRS(self, value):
		self._verbatimSRS = value

	@property
	def decimalLatitude(self):
		return self._decimalLatitude
	@decimalLatitude.setter
	def decimalLatitude(self, value):
		self._decimalLatitude = value

	@property
	def decimalLongitude(self):
		return self._decimalLongitude
	@decimalLongitude.setter
	def decimalLongitude(self, value):
		self._decimalLongitude = value

	@property
	def geodeticDatum(self):
		return self._geodeticDatum
	@geodeticDatum.setter
	def geodeticDatum(self, value):
		self._geodeticDatum = value

	@property
	def coordinateUncertaintyInMeters(self):
		return self._coordinateUncertaintyInMeters
	@coordinateUncertaintyInMeters.setter
	def coordinateUncertaintyInMeters(self, value):
		self._coordinateUncertaintyInMeters = value

	@property
	def coordinatePrecision(self):
		return self._coordinatePrecision
	@coordinatePrecision.setter
	def coordinatePrecision(self, value):
		self._coordinatePrecision = value

	@property
	def pointRadiusSpatialFit(self):
		return self._pointRadiusSpatialFit
	@pointRadiusSpatialFit.setter
	def pointRadiusSpatialFit(self, value):
		self._pointRadiusSpatialFit = value

	@property
	def footprintWKT(self):
		return self._footprintWKT
	@footprintWKT.setter
	def footprintWKT(self, value):
		self._footprintWKT = value

	@property
	def footprintSRS(self):
		return self._footprintSRS
	@footprintSRS.setter
	def footprintSRS(self, value):
		self._footprintSRS = value

	@property
	def footprintSpatialFit(self):
		return self._footprintSpatialFit
	@footprintSpatialFit.setter
	def footprintSpatialFit(self, value):
		self._footprintSpatialFit = value

	@property
	def georeferencedBy(self):
		return self._georeferencedBy
	@georeferencedBy.setter
	def georeferencedBy(self, value):
		self._georeferencedBy = value

	@property
	def georeferencedDate(self):
		return self._georeferencedDate
	@georeferencedDate.setter
	def georeferencedDate(self, value):
		self._georeferencedDate = value

	@property
	def georeferenceProtocol(self):
		return self._georeferenceProtocol
	@georeferenceProtocol.setter
	def georeferenceProtocol(self, value):
		self._georeferenceProtocol = value

	@property
	def georeferenceSources(self):
		return self._georeferenceSources
	@georeferenceSources.setter
	def georeferenceSources(self, value):
		self._georeferenceSources = value

	@property
	def georeferenceVerificationStatus(self):
		return self._georeferenceVerificationStatus
	@georeferenceVerificationStatus.setter
	def georeferenceVerificationStatus(self, value):
		self._georeferenceVerificationStatus = value

	@property
	def georeferenceRemarks(self):
		return self._georeferenceRemarks
	@georeferenceRemarks.setter
	def georeferenceRemarks(self, value):
		self._georeferenceRemarks = value

# GeologicalContext Terms

	@property
	def geologicalContextID(self):
		return self._geologicalContextID
	@geologicalContextID.setter
	def geologicalContextID(self, value):
		self._geologicalContextID = value

	@property
	def earliestEonOrLowestEonothem(self):
		return self._earliestEonOrLowestEonothem
	@earliestEonOrLowestEonothem.setter
	def earliestEonOrLowestEonothem(self, value):
		self._earliestEonOrLowestEonothem = value

	@property
	def latestEonOrHighestEonothem(self):
		return self._latestEonOrHighestEonothem
	@latestEonOrHighestEonothem.setter
	def latestEonOrHighestEonothem(self, value):
		self._latestEonOrHighestEonothem = value

	@property
	def earliestEraOrLowestErathem(self):
		return self._earliestEraOrLowestErathem
	@earliestEraOrLowestErathem.setter
	def earliestEraOrLowestErathem(self, value):
		self._earliestEraOrLowestErathem = value

	@property
	def latestEraOrHighestErathem(self):
		return self._latestEraOrHighestErathem
	@latestEraOrHighestErathem.setter
	def latestEraOrHighestErathem(self, value):
		self._latestEraOrHighestErathem = value

	@property
	def earliestPeriodOrLowestSystem(self):
		return self._earliestPeriodOrLowestSystem
	@earliestPeriodOrLowestSystem.setter
	def earliestPeriodOrLowestSystem(self, value):
		self._earliestPeriodOrLowestSystem = value

	@property
	def latestPeriodOrHighestSystem(self):
		return self._latestPeriodOrHighestSystem
	@latestPeriodOrHighestSystem.setter
	def latestPeriodOrHighestSystem(self, value):
		self._latestPeriodOrHighestSystem = value

	@property
	def earliestEpochOrLowestSeries(self):
		return self._earliestEpochOrLowestSeries
	@earliestEpochOrLowestSeries.setter
	def earliestEpochOrLowestSeries(self, value):
		self._earliestEpochOrLowestSeries = value

	@property
	def latestEpochOrHighestSeries(self):
		return self._latestEpochOrHighestSeries
	@latestEpochOrHighestSeries.setter
	def latestEpochOrHighestSeries(self, value):
		self._latestEpochOrHighestSeries = value

	@property
	def earliestAgeOrLowestStage(self):
		return self._earliestAgeOrLowestStage
	@earliestAgeOrLowestStage.setter
	def earliestAgeOrLowestStage(self, value):
		self._earliestAgeOrLowestStage = value

	@property
	def latestAgeOrHighestStage(self):
		return self._latestAgeOrHighestStage
	@latestAgeOrHighestStage.setter
	def latestAgeOrHighestStage(self, value):
		self._latestAgeOrHighestStage = value

	@property
	def lowestBiostratigraphicZone(self):
		return self._lowestBiostratigraphicZone
	@lowestBiostratigraphicZone.setter
	def lowestBiostratigraphicZone(self, value):
		self._lowestBiostratigraphicZone = value

	@property
	def highestBiostratigraphicZone(self):
		return self._highestBiostratigraphicZone
	@highestBiostratigraphicZone.setter
	def highestBiostratigraphicZone(self, value):
		self._highestBiostratigraphicZone = value

	@property
	def lithostratigraphicTerms(self):
		return self._lithostratigraphicTerms
	@lithostratigraphicTerms.setter
	def lithostratigraphicTerms(self, value):
		self._lithostratigraphicTerms = value

	@property
	def group(self):
		return self._group
	@group.setter
	def group(self, value):
		self._group = value

	@property
	def formation(self):
		return self._formation
	@formation.setter
	def formation(self, value):
		self._formation = value

	@property
	def member(self):
		return self._member
	@member.setter
	def member(self, value):
		self._member = value

	@property
	def bed(self):
		return self._bed
	@bed.setter
	def bed(self, value):
		self._bed = value

# Identification Terms

	@property
	def identificationID(self):
		return self._identificationID
	@identificationID.setter
	def identificationID(self, value):
		self._identificationID = value

	@property
	def identifiedBy(self):
		return self._identifiedBy
	@identifiedBy.setter
	def identifiedBy(self, value):
		self._identifiedBy = value

	@property
	def dateIdentified(self):
		return self._dateIdentified
	@dateIdentified.setter
	def dateIdentified(self, value):
		self._dateIdentified = value

	@property
	def identificationReferences(self):
		return self._identificationReferences
	@identificationReferences.setter
	def identificationReferences(self, value):
		self._identificationReferences = value

	@property
	def identificationVerificationStatus(self):
		return self._identificationVerificationStatus
	@identificationVerificationStatus.setter
	def identificationVerificationStatus(self, value):
		self._identificationVerificationStatus = value

	@property
	def identificationRemarks(self):
		return self._identificationRemarks
	@identificationRemarks.setter
	def identificationRemarks(self, value):
		self._identificationRemarks = value

	@property
	def identificationQualifier(self):
		return self._identificationQualifier
	@identificationQualifier.setter
	def identificationQualifier(self, value):
		self._identificationQualifier = value

	@property
	def typeStatus(self):
		return self._typeStatus
	@typeStatus.setter
	def typeStatus(self, value):
		self._typeStatus = value

# Taxon Terms

	@property
	def taxonID(self):
		return self._taxonID
	@taxonID.setter
	def taxonID(self, value):
		self._taxonID = value

	@property
	def scientificNameID(self):
		return self._scientificNameID
	@scientificNameID.setter
	def scientificNameID(self, value):
		self._scientificNameID = value

	@property
	def acceptedNameUsageID(self):
		return self._acceptedNameUsageID
	@acceptedNameUsageID.setter
	def acceptedNameUsageID(self, value):
		self._acceptedNameUsageID = value

	@property
	def parentNameUsageID(self):
		return self._parentNameUsageID
	@parentNameUsageID.setter
	def parentNameUsageID(self, value):
		self._parentNameUsageID = value

	@property
	def originalNameUsageID(self):
		return self._originalNameUsageID
	@originalNameUsageID.setter
	def originalNameUsageID(self, value):
		self._originalNameUsageID = value

	@property
	def nameAccordingToID(self):
		return self._nameAccordingToID
	@nameAccordingToID.setter
	def nameAccordingToID(self, value):
		self._nameAccordingToID = value

	@property
	def namePublishedInID(self):
		return self._namePublishedInID
	@namePublishedInID.setter
	def namePublishedInID(self, value):
		self._namePublishedInID = value

	@property
	def taxonConceptID(self):
		return self._taxonConceptID
	@taxonConceptID.setter
	def taxonConceptID(self, value):
		self._taxonConceptID = value

	@property
	def scientificName(self):
		return self._scientificName
	@scientificName.setter
	def scientificName(self, value):
		self._scientificName = value

	@property
	def acceptedNameUsage(self):
		return self._acceptedNameUsage
	@acceptedNameUsage.setter
	def acceptedNameUsage(self, value):
		self._acceptedNameUsage = value

	@property
	def parentNameUsage(self):
		return self._parentNameUsage
	@parentNameUsage.setter
	def parentNameUsage(self, value):
		self._parentNameUsage = value

	@property
	def originalNameUsage(self):
		return self._originalNameUsage
	@originalNameUsage.setter
	def originalNameUsage(self, value):
		self._originalNameUsage = value

	@property
	def nameAccordingTo(self):
		return self._nameAccordingTo
	@nameAccordingTo.setter
	def nameAccordingTo(self, value):
		self._nameAccordingTo = value

	@property
	def namePublishedIn(self):
		return self._namePublishedIn
	@namePublishedIn.setter
	def namePublishedIn(self, value):
		self._namePublishedIn = value

	@property
	def namePublishedInYear(self):
		return self._namePublishedInYear
	@namePublishedInYear.setter
	def namePublishedInYear(self, value):
		self._namePublishedInYear = value

	@property
	def higherClassification(self):
		return self._higherClassification
	@higherClassification.setter
	def higherClassification(self, value):
		self._higherClassification = value

	@property
	def kingdom(self):
		return self._kingdom
	@kingdom.setter
	def kingdom(self, value):
		self._kingdom = value

	@property
	def phylum(self):
		return self._phylum
	@phylum.setter
	def phylum(self, value):
		self._phylum = value

	# @property
	# def class(self):
	# 	return self._class
	# @class.setter
	# def class(self, value):
	# 	self._class = value

	@property
	def order(self):
		return self._order
	@order.setter
	def order(self, value):
		self._order = value

	@property
	def family(self):
		return self._family
	@family.setter
	def family(self, value):
		self._family = value

	@property
	def genus(self):
		return self._genus
	@genus.setter
	def genus(self, value):
		self._genus = value

	@property
	def subgenus(self):
		return self._subgenus
	@subgenus.setter
	def subgenus(self, value):
		self._subgenus = value

	@property
	def specificEpithet(self):
		return self._specificEpithet
	@specificEpithet.setter
	def specificEpithet(self, value):
		self._specificEpithet = value

	@property
	def infraspecificEpithet(self):
		return self._infraspecificEpithet
	@infraspecificEpithet.setter
	def infraspecificEpithet(self, value):
		self._infraspecificEpithet = value

	@property
	def taxonRank(self):
		return self._taxonRank
	@taxonRank.setter
	def taxonRank(self, value):
		self._taxonRank = value

	@property
	def verbatimTaxonRank(self):
		return self._verbatimTaxonRank
	@verbatimTaxonRank.setter
	def verbatimTaxonRank(self, value):
		self._verbatimTaxonRank = value

	@property
	def scientificNameAuthorship(self):
		return self._scientificNameAuthorship
	@scientificNameAuthorship.setter
	def scientificNameAuthorship(self, value):
		self._scientificNameAuthorship = value

	@property
	def vernacularName(self):
		return self._vernacularName
	@vernacularName.setter
	def vernacularName(self, value):
		self._vernacularName = value

	@property
	def nomenclaturalCode(self):
		return self._nomenclaturalCode
	@nomenclaturalCode.setter
	def nomenclaturalCode(self, value):
		self._nomenclaturalCode = value

	@property
	def taxonomicStatus(self):
		return self._taxonomicStatus
	@taxonomicStatus.setter
	def taxonomicStatus(self, value):
		self._taxonomicStatus = value

	@property
	def nomenclaturalStatus(self):
		return self._nomenclaturalStatus
	@nomenclaturalStatus.setter
	def nomenclaturalStatus(self, value):
		self._nomenclaturalStatus = value

	@property
	def taxonRemarks(self):
		return self._taxonRemarks
	@taxonRemarks.setter
	def taxonRemarks(self, value):
		self._taxonRemarks = value
