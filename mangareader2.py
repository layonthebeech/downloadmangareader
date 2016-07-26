import os
import urllib2
from bs4 import BeautifulSoup
import sys
import urllib
import requests


def make_folder(chapter_name): 
	#find relative path
	dir = os.path.dirname(__file__)
	#add manga name to relative path
	manga_path = os.path.join(dir, sys.argv[1])

	#if the manga name doesn't exist create it
	if not os.path.exists(manga_path):
    		os.makedirs(manga_path)

	#add chapter path to that path
	chapter_path = os.path.join(manga_path, chapter_name)
	
   	#if the chapter name does not exist create it
	if not os.path.exists(chapter_path):
    		os.makedirs(chapter_path)
    #return path so when writing files you can use it
	return chapter_path
	
def download_file(url, chapter_name):
	#path to save page of manga to
	path = make_folder(chapter_name)
	#take the title from the end of the url and append it to path
	local_filename = path + '/' + url.split('/')[-1]
	#begin request
	r = requests.get(url, stream=True)
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk:
				f.write(chunk)
	return local_filename

def download_chapter(chapter_number):
	#lazy shortcut to name the chapter name the number of the chapter instead of the real name due to the difficulty of scraping that
	chapter_name = chapter_number
	print('chname', chapter_name)
	pages = 0
	page = 1
	#while the page number doesn't equal the final page number
	while True:
		#get url of the page we want to download
		page_url = "http://mangareader.net/" + sys.argv[1] +"/" + chapter_number + "/" + str(page)
		page_html = urllib2.urlopen(page_url)
		soup = BeautifulSoup(page_html, "html.parser")
		number_of_pages = soup.find('select', {'id':'pageMenu'})
		pages = len(number_of_pages)/2
		image_source = soup.find('img',{'src':True})
		image_alt = soup.find('img', {'alt':True})
		print(str(image_source['src']),str(image_alt['alt']))
		download_file(image_source['src'], chapter_name)
		if page == pages:
			break
		page+=1
	


#begin script
toc_url = "http://www.mangareader.net/" + sys.argv[1]
html = urllib2.urlopen(toc_url)
soup = BeautifulSoup(html, "html.parser")

#make manga folder
#series_path = make_folder(sys.argv[1])
#if there is no specific chapter 
if len(sys.argv) == 2:
	#find all the rows of the table which are chapters of the manga
	tables = soup.find_all('table', {'id':'listing'})[0].find_all('tr')
	#for rows in table download the chapter
	for index, row in enumerate(tables): 
		print(tables[index])
		#lazily add a number because it isn't 0 indexed
		indexplus1 = str(index+1)
		download_chapter(indexplus1)
else:
#if there is a specific chatpter argv is the chapter
#will be changing this to prompts to make it clearer
	download_chapter(sys.argv[2])


	

