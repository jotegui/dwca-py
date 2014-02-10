'''
Created on Apr 9, 2013

@author: jotegui
'''

class DarwinCoreArchiveDownloader(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def downloadLinks(self, url):
        import urllib
        import lxml.html
        
        connection = urllib.urlopen(url)
        dom = lxml.html.fromstring(connection.read())
        
        links = []
        
        for link in dom.xpath('//a/@href'):
            links.append(link)
        
        return links
    
    def buildDwcaLinks(self, url):
        
        links = self.downloadLinks(url)
        
        dwcaLinks = []
        
        for i in links:
            if i[:11] == 'resource.do':
                
                resourceLink = url+i
                archiveLink = url+'archive.do'+i[11:]
                
                dwcaLink = {
                    'resourceLink' : resourceLink,
                    'archiveLink' : archiveLink
                }
                
                dwcaLinks.append(dwcaLink)
        
        return dwcaLinks
    
    def buildDwcaList(self, url):
        
        dwcaLinks = self.buildDwcaLinks(url)
        
        dwcaList = []
        
        for i in dwcaLinks:
            archiveLink = i['archiveLink']
            archiveName = archiveLink[archiveLink.find('?r=')+3:]
            dwcaList.append(archiveName)
        
        return dwcaList
    
    def downloadSingleIPT(self, ipt_url, destination_folder):
        import urllib
        
        dwcaLinks = self.buildDwcaLinks(ipt_url)
        
        for i in dwcaLinks:
            archiveLink = i['archiveLink']
            archiveName = archiveLink[archiveLink.find('?r=')+3:]
            dwca = urllib.urlopen(archiveLink)
            dwcaContent = dwca.read()
            destination_path = destination_folder+archiveName+'.zip'
            destination_file = open(destination_path, 'w')
            destination_file.write(dwcaContent)
            destination_file.close()
            print 'Archive {0} downloaded from {1} to {2}'.format(archiveName, archiveLink, destination_path)
        
        return
    
    def downloadIPT(self, ipt_list, base_folder):
        
        import os
        
        for i in ipt_list:
            ipt_domain = i['ipt_domain']
            ipt_url = i['ipt_url']
            
            print 'Extracting DwCAs from IPT {0}'.format(ipt_domain)
            
            destination_folder = base_folder + ipt_domain+'/'
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
        
            self.downloadSingleIPT(ipt_url, destination_folder)
        
        return