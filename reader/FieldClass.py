import dwc.common as common

class Field():
    """
A representation of a field in a DarwinCore-Archive data file.
"""
    # TODO:
    # Build a parser for term and vocabulary. Dilemma, both should be URLs, not local files, but zip_file has not been passed to Field initializer...
    
    def __init__(self, field):
        
        # Add common values: type (<id> or <field>) and index
        self.type = field.nodeName
        
        # Create container for values
        self.values = []
        
        # If <id> or <coreid>, just add index attribute or 0 if absent
        if self.type == 'id' or self.type == 'coreid':
            try:
                self.index = int(field.attributes['index'].value)
            except KeyError:
                self.index = 0
        
        # Parse all attributes for <field> elements
        elif self.type == 'field':
            
            # Term attribute is mandatory
            try:
                self.term = field.attributes['term'].value
            except KeyError:
                raise common.MetafileError('\'term\' attribute not found for <field> in position {0}. \'term\' is mandatory'.format(listpos))
            
            # The rest are optional
            try:
                self.default = field.attributes['default'].value
            except KeyError:
                self.default = None
            try:
                self.vocabulary = field.attributes['vocabulary'].value
            except KeyError:
                self.vocabulary = None
            
            # If index is not present, it is a default attribute
            try:
                self.index = int(field.attributes['index'].value)
            except KeyError:
                self.index = None
    
    def completeness(self):
        return len([i for i in self.values if i != ""])
