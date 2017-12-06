import requests, urllib2
import xml.etree.ElementTree as ET

#settings
base_api_url = "http://thegamesdb.net/api/"


#get platform list
def get_platforms():
    all_platforms = []
    url = 'http://thegamesdb.net/api/GetPlatformsList.php'
    request = urllib2.Request(url, headers={"Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "http://thewebsite.com",
    "Connection": "keep-alive" })
    contents = urllib2.urlopen(request).read()
    root = ET.fromstringlist(contents)
    platforms = root.find('Platforms')
    #platforms = data.find("Platforms")
    try:
        for platform in platforms.findall('Platform'):
            platf = {}
            if platform.find('id') != None: platf['id'] = platform.find('id').text
            if platform.find('name') != None: platf['name'] = platform.find('name').text
            if platform.find('alias') != None: platf['alias'] = platform.find('alias').text
            all_platforms.append(platf)


    except:
        print('---->>> error building list')

    return all_platforms
