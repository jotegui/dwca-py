from dwc.common import MappingError
"""
@TODO
- update functions marked with # in col 1 to adapt to new style of dwca fields
- figure out what to do with non-standard terms when using subset to build SDwCR
- change arguments of certain functions to be dicts, not lists
"""

class RecordSet():
    """
Class definition for a Record Set, understood as a collection of records. Fields
are stored as attributes and are callable in a regular Object Oriented way. Each
attribute is a list of the term's value in the records, stored as text. The idea
is to have an easy and fast access to all the different values of a term among
the records, instead of having access to all the terms of a record. The list
values for each term can be accessed by calling the respective term as an
attribute.

WARNING: due to python keyword conflict, the term 'class' cannot be accessed
calling for the 'class' attribute. Instead, call the '_class' attribute. See
examples in the end of this docstring.

Apart from these attributes, the class currently has two special attributes and
twelve methods: 

    BASIC FUNCTIONS
    - terms and populatedTerms: a list of all the terms (fields) which have any
    information.
    - checkTerm: a method to check if a term exists in the recordset
    - show: a way of representing the content of the record set
    - buildRecord: a method to build a SimpleDarwinCore record from the record
    set, given the position of the record in the lists.
    - subset: a method to extract a subset of the records, based on a value from
    a term (field). If the subset has only one record, a SimpleDarwinCore record
    is created; else, a new recordset is created
    - rename: a method to rename a single field
    - batchRename: a method to rename a series of fields
    
    STAT FUNCTIONS
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
    - countMultiTermValueAND: a method to count the number of records with a
    given combination of values in different fields, using AND logic (records
    that meet all requirements)
    - countMultiTermValueOR: same as before, but using OR logic (records that
    meet any requirement)
    
    EXTENSION FUNCTIONS - TODO
    -blah

To initialize a new RecordSet, a dictionary must be built first with all the
terms, and the content of the terms must be a list of all the values from the
records.

See docstrings of individual methods for examples of usage.
"""



    # INITIALIZATION
    def __init__(self, occurrences):
        """
Initialization function for the RecordSet class.
Argument must be a dictionary containing the values in lists.

Example:
occurrences = {
    'country': ['US','US','ES','PT'],
    'year': [2002, 2000, 2012, ''],
    'basisOfRecord': ['Specimen', 'Specimen','Observation','Observation'],
    'class': ['Mammalia','Aves','Mammalia','Mammalia']
}

rs = RecordSet(occurrences)
"""

        self.populatedTerms = occurrences.keys()
        self.terms = self.populatedTerms
        self.flags = {}
        
        for term in self.terms:
            setattr(self, term, occurrences[term])



    # WRAPPER FOR THE 'CLASS' TERM.
    @property
    def _class(self):
        value = getattr(self, 'class') 
        return value



    # FUNCTION TO CHECK IF TERM EXISTS IN POPULATEDTERMS
    def checkTerms(self, terms_list):
        """
Checks if all the terms in the provided list of terms are present in the record
set. Raises MappingError otherwise.
"""
        if isinstance(terms_list, str):
            terms_list = [terms_list]
        for term in terms_list:
            if term not in self.populatedTerms:
                raise MappingError('The term \'{0}\' does not exist in this set of records. Check the spelling.'.format(term))
        return



#    # FUNCTION TO SHOW THE CONTENT
    # TO BE REPLACED BY AN OVERRIDE OF __repr__
    def show(self):
        """
Prints the contents of the record set.
"""
        for term in self.populatedTerms:
            print "{0}\n{1}".format(term, getattr(self, term))
        return



#    # FUNCTION TO EXTRACT A SINGLE RECORD IN SIMPLEDARWINCORE FORMAT
    def buildRecord(self, pos):
        """
Returns a SimpleDarwinCoreRecord instance with the content of a record. Argument
is the position in the terms list.

Example:
rs.buildRecord(0) # returns a SimpleDarwinCoreRecord instance with
the content of the first record in the record set.
"""
        from dwc.SimpleDarwinCoreRecordClass import SimpleDarwinCoreRecord
        
        data = {}
        for term in self.populatedTerms:
            data[term] = getattr(self,term)[pos]

        sdwcr = SimpleDarwinCoreRecord(data)

        return sdwcr



#    # FUNCTION TO EXTRACT A SUBSET OF THE RECORDS GIVEN A VALUE
    def subset(self, term, value):
        """
Returns a new instance of RecordSet with the records that meet the given
condition. If successful, the function prints the number of records of the new
RecordSet. Raises MappingError if term does not exist.

Example:
rs.subset('country','US')
New recordset created with 2 records
"""
        self.checkTerms(term)
        
        # Build the container of the new records
        occurrences = {}
        for i in self.populatedTerms:
            occurrences[i] = []
        
        # Iterate through the records to populate the container
        for i in range(self.countRecords()):
            if getattr(self, term)[i] == value:
                for j in self.populatedTerms:
                    occurrences[j].append(getattr(self, j)[i])
        
        # Instantiate a new RecordSet
        rs = RecordSet(occurrences)
        rs.dwcTerms = self.dwcTerms
        if rs.countRecords() == 1:
            sdwcr = rs.buildRecord(0)
            del rs
            print "Subset returned single record. Instance of SimpleDarwinCoreRecord created"
            return sdwcr
       	else:
            print "New recordset created with {0} records".format(rs.countRecords())
            return rs



#    # FUNCTION TO RENAME A FIELD
    def rename(self, old, new):
        """
Renames a field. The original field will not exist anymore. Raises MappingError
if original field does not exist.

Example:
rs.rename('id','occurrenceID')
"""
        # Check if given name exists
        self.checkTerms(old)
        
        # Add new name to populatedTerms
        if new not in self.populatedTerms:
            self.populatedTerms.append(new)
        # Add new attribute
        setattr(self, new, getattr(self, old))
        
        # Delete old attribute and entry in populatedTerms
        delattr(self, old)
        self.populatedTerms.pop(self.populatedTerms.index(old))
        
        return



#    # FUNCTION TO RENAME FIELDS IN BATCH MODE
    def batchRename(self, changes):
        """
Performs a batch rename of fields. Argument is a dictionary with original names
as keys and new names as values. Raises Mapping Error if any original name does
not exist.

Example:
changes = {
    'id' : 'occurrenceID',
    'occurrenceDetails' : 'occurrenceRemarks'
}
rs.batchRename(changes)
"""
        self.checkTerms(changes.keys())
        
        for i in changes.items():
            self.rename(i[0], i[1])
        
        return



    # FUNCTION TO COUNT THE NUMBER OF RECORDS
    def countRecords(self):
        """
Returns the number of records in the record set.

Example:
rs.countRecords() # Returns 135
"""
        if type(getattr(self, self.populatedTerms[0])) != type([]):
            records = len(getattr(self, self.populatedTerms[0]).values)
        else:
            records = len(getattr(self, self.populatedTerms[0]))
        return records



    # FUNCTION TO COUNT THE FREQUENCIES OF THE DIFFERENT VALUES OF A TERM
    def countTerm(self, term, format = 'dict'):
        """
Extracts all the different values of a term and their frequencies and returns a
dict. Raises MappingError if argument is not present in the record set.

Example:
rs.countTerm('country') # gives {'': 27, 'Canada': 132, 'Republic of Peru': 1, ...}
"""
        self.checkTerms(term)
        
        # Patch to put up with the new structure of fields while keeping the old one just in case
        values = getattr(self, term)
        if type(values) != type([]):
            values = values.values
        
        final = {}

        for value in values:
            if value in final.keys():
                final[value] += 1
            else:
                final[value] = 1
        
        if format == 'dict':
            return final

        elif format == 'csv':
            final_csv = "{0},{1}".format(term, 'count')
            for i in sorted(final, key=final.get, reverse=True):
                final_csv += "\n'{0}',{1}".format(i, final[i])
            return final_csv

        elif format == 'tab':
            final_tab = "{0}\t{1}".format(term, 'count')
            for i in sorted(final, key=final.get, reverse=True):
                final_tab += "\n{0}\t{1}".format(i, final[i])
            return final_tab
    
    
    
    # FUNCTION TO FORMAT THE OUTPUT OF COUNTTERM AS CSV
    def countTermCSV(self, term):
        """
Extracts all the different values of a term and their frequencies and returns a
string ready to be stored in a CSV file. Raises MappingError if argument is not
present in the record set.

Example:
print rs.countTermCSV('country')
country,count
'United States',832
'Canada',132
'Republic of Botswana',106
...
"""
        return self.countTerm(term, 'csv')



    # FUNCTION TO FORMAT THE OUTPUT OF COUNTTERM AS TAB-DELIMITED
    def countTermTAB(self, term):
        """
Extracts all the different values of a term and their frequencies and returns a
string ready to be stored in a tab-delimited file. Raises MappingError if
argument is not present in the record set.

Example:
print rs.countTermTAB('country')
country    count
United States    832
Canada    132
Republic of Botswana    106
...
"""
        return self.countTerm(term, 'tab')



    # FUNCTION TO COUNT THE FREQUENCY OF A VALUE IN A TERM
    def countTermValue(self, term, value):
        """
Returns the number of records with a particular value in the given field.
Returns 0 if the value is not present, and raises a MappingError if the term
does not exist.

Example:
rs.countTermValue('country', 'Bolivia') # returns 1219
rs.countTermValue('country','asdasd') # returns 0
rs.countTermValue('asdasd','') # raises error
"""
        self.checkTerms(term)
        final = 0

        # Patch to put up with the new structure of fields while keeping the old one just in case
        values = getattr(self, term)
        if str(type(values)) == "<type 'instance'>":
            values = values.values

        for i in values:
            if i == value:
                final += 1
        return final



    # FUNCTION TO SUM THE FREQUENCIES OF A LIST OF VALUES IN A TERM
    def countTermMultiValue(self, term, values_list):
        """
Returns the number of records that show ANY value from the given list for the
given field. Returns 0 if none of the values are present, and raises a
MappingError if the term does not exist.

Example:
rs.countTermMultiValue('order', ['Rodentia', 'Sociomorpha']) # returns 869
rs.countTermMultiValue('order', []) # returns 0
rs.countTermMultiValue('asdasd', []) # returns Error
"""
        self.checkTerms(term)
            
        finalcount = 0
        for i in values_list:
            thistermvalue = self.countTermValue(term, i)
            finalcount += thistermvalue
        return finalcount



    # FUNCTION TO COUNT THE NUMBER OF RECORDS WITH A GIVEN COMBINATION OF VALUES IN TERMS
    def countMultiTermValueAND(self, values_dict):
        """
Returns the number of records with a particular combination of values, using AND
logic (counts only the records wich comply with all of the requirements).
Argument must be a dict with the terms as keys and the term values as dict
values.

Example:
values_dict = {'decimalLatitude': '', 'decimalLongitude':''}
rs.countMultiTermValueAND(values_dict) # returns the number of records with null
    latitude and longitude.
"""        
        self.checkTerms(values_dict.keys())

        final_count = 0

        for i in range(self.countRecords()):
            match = 0
            for term in values_dict.keys():
                if type(getattr(self, term)) != type([]):
                    vals = getattr(self, term).values
                else:
                    vals = getattr(self, term)
                if vals[i] != values_dict[term]:
                    match = 0
                    break
                else:
                    match = 1
            if match == 1:
                final_count += 1

        return final_count



    # FUNCTION TO COUNT THE NUMBER OF RECORDS WITH A GIVEN COMBINATION OF VALUES IN TERMS
    def countMultiTermValueOR(self, values_dict):
        """
Returns the number of records with a particular combination of values, using OR
logic (counts the records wich comply with any of the requirements).
Argument must be a dict with the terms as keys and the term values as dict
values.

Example:
values_dict = {'decimalLatitude': '', 'decimalLongitude':''}
rs.countMultiTermValueOR(values_dict) # returns the number of records with null
    latitude or longitude.
"""        
        self.checkTerms(values_dict.keys())

        final_count = 0

        for i in range(self.countRecords()):
            match = 0
            for term in values_dict.keys():
                if type(getattr(self, term)) != type([]):
                    vals = getattr(self, term).values
                else:
                    vals = getattr(self, term)
                if vals[i] != values_dict[term]:
                    match = 0
                else:
                    match = 1
                    break
            if match == 0:
                continue
            else:
                final_count += 1

        return final_count
