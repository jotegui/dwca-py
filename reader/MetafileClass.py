from xml.dom import minidom
#from urllib2 import urlopen, HTTPError
from dwc.reader.CoreClass import Core
from dwc.reader.ExtensionClass import Extension
import dwc.common as common

class Metafile():
    """
A parser for the metafile meta.xml, according to http://rs.tdwg.org/dwc/text/tdwg_dwc_text.xsd
"""
    # TODO:
    # Implement understanding of variables in static fields (see BaseFile class)
    
    def __init__(self, zip_file):
        
        metafile_content = common._locateFileInZip(zip_file, 'meta.xml')
        if metafile_content is None:
            raise common.MetafileError('Could not find meta.xml.')
       
        metafile = minidom.parse(metafile_content)
        
        self._parseMain(metafile, zip_file)
        self.core = self._parseCore(metafile, zip_file)
        self._parseExtensions(metafile, zip_file)

    def _parseMain(self, metafile, zip_file):
        
        # Get root element
        archive = metafile.firstChild
        
        # Should be 'archive'
        if archive.nodeName != 'archive':
            raise common.MetafileError('First element is not called \'archive\'.')
        
        # Metadata attribute is optional
        try:
            metadata = archive.attributes['metadata'].value
        except KeyError:
            metadata = None
        
        # Check that metadata is a file name in the archive or a reachable URL
        if metadata and common._parseLocation(metadata, zip_file) is False:
            raise common.MetafileError('Metadata file, located in \'{0}\' cannot be reached.'.format(metadata))

        self.metadata = metadata
        
        return
    
    def _parseCore(self, metafile, zip_file):
        
        # Get <core> element
        core = metafile.getElementsByTagName('core')
        
        # Make sure there is one and only one <core> element
        if len(core) > 1:
            raise common.MetafileError('More than one <core> elements. There should be only one.')
        if len(core) < 1:
            raise common.MetafileError('No <core> element was found. There should be one <core> element.')
        
        # Create a Core object
        return Core(core[0], zip_file)

    def _parseExtensions(self, metafile, zip_file):
        
        # Create container for extensions
        self.extensions = {}
        
        # Get <extension> elements
        extensions = metafile.getElementsByTagName('extension')
        
        # For each extension
        for extension in extensions:
            # Create the Extension object
            thisextension = Extension(extension, zip_file)
            # Extract extension name from rowType
            thisname = thisextension.rowType.split("/")[-1]
            # Check if duplicated extensions
            if thisname in self.extensions.keys():
                raise common.MetafileError('More than one specification of the extension {0}'.format(thisname))
            else:
                self.extensions[thisname] = thisextension
        
        # Check if id field exists in <core> fields
        if len(self.extensions.keys()) > 0:
            if self.core.id.index is None:
                raise common.MetafileError('No <id> field found in <core> element, and extensions exist.')
        
        return
