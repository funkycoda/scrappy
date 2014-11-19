# -*- coding: utf-8 -*-
"""
	Scraps WRDC Solar Radiation data from 
	http://wrdc.mgo.rssi.ru/wrdccgi/protect.exe?wrdc/data_gaw.htm

	:copyright: (c) 2014 by Ajay Ranipeta.
	:license: MIT, see LICENSE for more details.
"""

import re
import os
from array import array

import requests
from bs4 import BeautifulSoup


link_list = []

# start a session
s = requests.Session()

# get a pattern
download_pattern = re.compile(r'.*_d\.htm')
global_pattern = re.compile(r'.*_glo_d\.htm')
diffuse_pattern = re.compile(r'.*_dif_d\.htm')
direct_pattern = re.compile(r'.*_dir_d\.htm')
spectral_pattern = re.compile(r'.*_spe_d\.htm')
downward_pattern = re.compile(r'.*_dwl_d\.htm')


def download_daily_data(basepath):
	print(' > Parsing %s' % basepath)
	page = s.get(basepath)
	locsoup = BeautifulSoup(page.text)
	for link in locsoup.find_all('a', {"href": download_pattern}): 
		lnk = link.get('href')
		download_url = 'http://wrdc.mgo.rssi.ru/wrdccgi/%s' % lnk

		# Generate necessary directory and filenames
		filename = lnk[20:]
		basefilename = filename[filename.rindex('/'):]
		dirname = basefilename.split('_',1)[0]
		dirname = '.%s%s' % (dirname, filename[0:filename.rindex('/')])
		htmlfilename = '%s%s' % (dirname, basefilename)
		txtfilename = '%s%s' % (dirname, basefilename.replace('.htm', '.txt'))

		print(' >> Downloading %s' % basefilename)

		# Check if the directory exists. If not, create it
		if not os.path.exists(dirname):
			os.makedirs(dirname)

		# Download the page
		r = s.get(download_url)
		sp = BeautifulSoup(r.text)

		# Save the html version
		f = open(htmlfilename,'w')
		f.write(r.text.encode('utf-8'))
		f.close()

		# Save the text version
		# f = open(txtfilename,'w')
		# f.write(sp.get_text().encode('utf-8'))
		# f.close()



page = s.get('http://wrdc.mgo.rssi.ru/wrdccgi/protect.exe?wrdc/L_GAW.HTM')
soup = BeautifulSoup(page.text)

for link in soup.find_all('a', {"href": download_pattern}): 
	lnk = link.get('href')
	download_url = 'http://wrdc.mgo.rssi.ru/wrdccgi/%s' % lnk
	print('Adding link: %s' % download_url)
	# link_list.append(download_url)
	download_daily_data(download_url)
