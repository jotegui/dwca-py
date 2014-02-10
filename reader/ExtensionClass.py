import dwc.common as common
from dwc.reader.BaseFileClass import BaseFile

class Extension(BaseFile):
    """
A Class for the <extension> file methods and attributes in a DarwinCore Archive's
metafile, according to http://rs.tdwg.org/dwc/text/tdwg_dwc_text.xsd and
http://rs.tdwg.org/dwc/terms/guides/text/index.htm#metafile
"""
    # TODO:
    #
    # - Think on the use of 'coreid' or 'id' as a name for the <coreid> field
    
    def __init__(self, extension, zip_file):
        
        # Load the metadata
        BaseFile.__init__(self, extension, 'extension', zip_file)
        
        # Load the data
        self.warnings = []
        
        # Data in single file
        if len(self.locations) == 1:
            
            # Open file
            content = common._locateFileInZip(zip_file, self.locations[0]).read().split(self.linesTerminatedBy)[self.ignoreHeaderLines:]
            
            # Remove last newline
            if content[-1] == '':
                content = content[:-1]
            
            # Build populatedTerms and main infrastructure
            self.populatedTerms = []
            if self.coreid.index not in self.fields.keys():
                self.populatedTerms.append('coreid')
            for i in sorted(self.fields.keys()):
                term = self.fields[i].term.split("/")[-1].encode(self.encoding)
                self.populatedTerms.append(term)
            for term in self.populatedTerms:
                setattr(self, term, [])
            
            # Load the content
            for line in content:
                # Remove trailing newline
                if line[-1] == "\n":
                    line = line[:-1]
                splitline = line.split(self.fieldsTerminatedBy)
                for pos in range(len(self.populatedTerms)):
                    thiskey = self.populatedTerms[pos]
                    thisvalue = splitline[pos]
                    # Remove field enclosing character, if present
                    if self.fieldsEnclosedBy != '' and thisvalue[0] == self.fieldsEnclosedBy and thisvalue[-1] == self.fieldsEnclosedBy:
                        thisvalue = thisvalue[1:-1]
                    getattr(self, thiskey).append(thisvalue)
        
        # Data in more than one file
        else:
            #TODO
            self.warnings.append("Sorry, multi-file loading of extension data is not yet supported. Basic metadata has been parsed but no actual record has been processed.")
        
        # Load the defaults
        if len(self.defaults) > 0:
            for i in self.defaults:
                term = i.term.split("/")[-1].encode(self.encoding)
                value = i.default.encode(self.encoding)
                if term in self.populatedTerms:
                    self.warnings.append("'{0}' appears in the core file and as a default field in the metafile. Ignoring the default value.".format(term))
                    continue
                else:
                    setattr(self, term, [])
                    self.populatedTerms.append(term)
                    for i in list(range(self.countRecords())):
                        getattr(self, term).append(value)

       
