dwca-py
=======

Python implementation of DarwinCore Archives

*Usage:*

- Create folder somewhere in PYTHONPATH, or add new folder to PYTHONPATH. Say we name it dwc
- Import DarwinCoreArchiveClass from dwc.reader:
	``from dwc.reader.DarwinCoreArchiveClass import DarwinCoreArchive as DWCA``
- Load the DarwinCore content by supplying the path to a DwC-A file
	``path='path/to/Darwin_core_archive.zip'``
	``dwca = DWCA(path)``
- Voilà
