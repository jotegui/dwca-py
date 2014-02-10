import dwc.common as common
from dwc.reader.FieldClass import Field

class BaseFile():
    """
A base class for all types of files, core or extensions. Extended by CoreFile and ExtensionFile classes.
"""
    # TODO:
    # Build a block to check duplicates in indexes (except id / coreid, which might be duplicated)
    # Build a parser for rowType
    # Build a parser for defaults with variable values
    
    def __init__(self, baseElement, elementType, zip_file):
        
        # Identification elements
        if elementType == 'core':
            idElementName = 'id'
        elif elementType == 'extension':
            idElementName = 'coreid'
            
        # Since atributes are optional, try detecting them and, if not present, store default value
        try:
            self.linesTerminatedBy = str(baseElement.attributes['linesTerminatedBy'].value).decode('string-escape')
        except KeyError:
            self.linesTerminatedBy = "\n"
        try:
            self.fieldsTerminatedBy = str(baseElement.attributes['fieldsTerminatedBy'].value).decode('string-escape')
        except KeyError:
            self.fieldsTerminatedBy = ","
        try:
            self.fieldsEnclosedBy = str(baseElement.attributes['fieldsEnclosedBy'].value).decode('string-escape')
        except KeyError:
            self.fieldsEnclosedBy = "\""
        try:
            self.ignoreHeaderLines = int(baseElement.attributes['ignoreHeaderLines'].value)
        except KeyError:
            self.ignoreHeaderLines = 0
        try:
            self.rowType = str(baseElement.attributes['rowType'].value).decode('string-escape')
        except KeyError:
            self.rowType = "http://rs.tdwg.org/dwc/xsd/simpledarwincore/SimpleDarwinRecord"
        try:
            self.encoding = str(baseElement.attributes['encoding'].value).decode('string-escape')
        except KeyError:
            self.encoding = "UTF-8"
        try:
            self.dateFormat = str(baseElement.attributes['dateFormat'].value).decode('string-escape')
        except KeyError:
            self.dateFormat = "YYYY-MM-DD"
        
        
        # Parse the <files> element in the base element
        files = baseElement.getElementsByTagName('files')
        
        # Make sure there is one and only one <files> element in <core>
        if len(files) > 1:
            raise common.MetafileError('More than one <files> elements. There should be only one.')
        if len(files) < 1:
            raise common.MetafileError('No <files> element was found. There should be one <files> element.')
        
        # Extract the location/s of the core files
        locations = files[0].getElementsByTagName('location')
        
        # Check that at least one exists
        if len(locations) == 0:
            raise common.MetafileError('No <location> element found in <{0}> element\'s <files> element. There shouold be at least one.'.format(elementType))
        
        self.locations = []
        for location in locations:
            if common._parseLocation(location.firstChild.nodeValue, zip_file) is False:
                raise common.MetafileError('Could not find {1} file {0}.'.format(location.firstChild.nodeValue, elementType))
            self.locations.append(location.firstChild.nodeValue)
        
        # Parse the <id> or <coreid> and <field> elements
        self.fields = {}
        # If a <field> does not have an index attribute, it is a default value for the whole DwC-A
        self.defaults = []
        
        # Check that there is no more than one <id> or <coreid>
        idFields = baseElement.getElementsByTagName('{0}'.format(idElementName))        
        if len(idFields) > 1:
            raise common.MetafileError('More than one <{0}> elements found in <{1}> element. There should be one or none.'.format(idElementName, elementType))

        # Parse the <id> or <coreid>
        elif len(idFields) == 1:
            setattr(self, idElementName, Field(idFields[0]))
        else:
            setattr(self, idElementName, None)
        
        # Get the <field> elements
        fields = [i for i in baseElement.childNodes if i.nodeType == 1 and i.nodeName != 'files' and i.nodeName != idElementName]
        # and parse them
        for field in fields:
            elementField = Field(field)
            if elementField.index:
                if elementField.index in self.fields.keys() and elementField.index != idFields[0].index:
                    raise common.MetafileError("Duplicated index number found in {0} element: {1}".format(elementType, elementField.index))
                self.fields[elementField.index] = elementField
            else:
                self.defaults.append(elementField)
