from urllib2 import urlopen, HTTPError

"""
Common classes and functions
"""

class MetafileError(Exception):
    def __init__(self,value):
        core = "Metafile (meta.xml) might be corrupted: "
        self.value=core+value
    def __str__(self):
        return repr(self.value)

class MappingError(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

def _parseLocation(file_location, zip_file):
    """
Try to locate the given file in the contents of the DarwinCore-Archive or an external URL
"""
    if file_location.startswith('http') is True or file_location.startswith('ftp') is True:
        # File is external
        try:
            d = urlopen(file_location).getcode()
        except HTTPError:
            return False
        if d == 200:
            exists = True
        else:
            exists = False
    else:
        # File is local
        t = _locateFileInZip(zip_file, file_location)
        if t is None:
            exists = False
        else:
            exists = True
            t.close()

    return exists


def _locateFileInZip(compressed_file, file_name):
    """
Open a compressed file and extracts a file.
"""

    if str(type(compressed_file)) == "<class 'tarfile.TarFile'>":
        if file_name not in compressed_file.getnames():
            open_file = None
        else:
            open_file = compressed_file.extractfile(file_name)
    
    elif str(type(compressed_file)) == "<class 'zipfile.ZipFile'>":
        if file_name not in compressed_file.namelist():
            open_file = None
        else:
            open_file = compressed_file.open(file_name, 'r')
    
    return open_file
