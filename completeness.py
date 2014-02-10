def termCompleteness(dwca):
    completeness = {}
    total = dwca.countRecords()
    for term in dwca.populatedTerms:
        compl = total - dwca.countTermValue(term, "")
        perc = "{0}%".format(round(compl*100.0/total,2))
        completeness[term] = {'total': compl, 'percentage': perc}
    return completeness
