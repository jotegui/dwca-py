from dwc.reader.BaseFileClass import BaseFile

class Core(BaseFile):
    """
A Class for the <core> file methods and attributes in a DarwinCore Archive's
metafile, according to http://rs.tdwg.org/dwc/text/tdwg_dwc_text.xsd and
http://rs.tdwg.org/dwc/terms/guides/text/index.htm#metafile
"""
    
    def __init__(self, core, zip_file):
        
        BaseFile.__init__(self, core, 'core', zip_file)
