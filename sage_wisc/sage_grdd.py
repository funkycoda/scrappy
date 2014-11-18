# -*- coding: utf-8 -*-
"""
	Scraps SAGE Global River Discharge data from 
	http://www.sage.wisc.edu/riverdata/scripts/view_all.php

	:copyright: (c) 2014 by Ajay Ranipeta.
	:license: MIT, see LICENSE for more details.
"""

import re
from array import array

import requests
from bs4 import BeautifulSoup


link_list = []

# start a session
s = requests.Session()

# get a pattern
download_pattern = re.compile(r'station_table_formated\.php')

page = s.get('http://www.sage.wisc.edu/riverdata/scripts/keysearch.php?numfiles=4000&startnum=0')
soup = BeautifulSoup(page.text)

# print(soup.prettify())

for link in soup.find_all('a', {"href": download_pattern}):
	lnk = link.get('href')
	download_url = 'http://www.sage.wisc.edu/riverdata/scripts/%s' % lnk
	print('Adding link: %s' % download_url)
	link_list.append(download_url)


for link in link_list:
	filename = './entries/station_entry_%s.txt' % link[78:]
	print('> Getting page for %s' % filename)
	r = s.get(link)
	f = open(filename,'w')
	f.write(r.text.encode('utf-8'))
	f.close()

