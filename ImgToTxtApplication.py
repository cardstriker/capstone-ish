from bs4 import BeautifulSoup
import urllib
from  urllib.request import urlopen
import validators
from PIL import Image
from reportlab.graphics import renderPDF, renderPM
from cairosvg import svg2png
import requests
import re
import ImageRecognizer
import os
import glob
import pdfkit


#open and read webpage (default)

#formats
audio_formats = ['.mp3', '.m4a', '.flac', '.wav', '.wma', '.aac', '.ogg']
video_formats = ['.mp4', '.mov', '.wmv', '.avi', '.swf', '.flv', '.f4v', '.mkv', '.webm']

class ImgToTxtApp:
	def setURL(self, url):
		global current_url
		global soup

		remove_files()

		results = []
		isURLValid = validators.url(url)
		if isinstance(isURLValid, validators.ValidationFailure):
			return False

		page = urlopen(url).read()
		soup = BeautifulSoup(page, 'html.parser')
		current_url = url
		link_array = readLinks(soup)
		results.append(link_array)
		img_array = getImages(soup)
		results.append(img_array)
		media_array = getOtherMultimedia(soup)
		results.append(media_array)
		updateHTML()
		downloadHTMLAsPDF(url, "helloworld")
		#predictedResults = ImageRecognizer.predictImg()


		return results

#Functions
def readLinks(soup):
	link_array = []
	for link in soup.find_all('a'):
	    link_array.append(link.get('href'))

	#clear NoneType
	link_array = [s for s in link_array if s]

	#find if its URL or website path
	result_array = []
	http_array = [s for s in link_array if s.startswith("http")]
	not_http_array = [s for s in link_array if not s.startswith("http")]
	result_array.append(http_array)
	result_array.append(not_http_array)
	return result_array

def getImages(soup):
	img_array = []
	for img in soup.find_all('img'):
		img_array.append(img.get('src'))
	for source in soup.find_all('source'):
		if 'image' in source.get('type'):
			img_array.append(source.get('srcset'))

	print(img_array)
	downloadImages(img_array)

	return img_array

def downloadImages(img_urls):
	for i in range(len(img_urls)):
		old_img_url = img_urls[i]
		img_url = checkUrl(old_img_url)

		if img_urls[i].lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')) and img_urls[i] is not None:
			try:
				img = Image.open(requests.get(img_url, stream = True).raw)
				img.save('downloadedImages/' + img_urls[i].rsplit('/')[-1])
			except IOError as e:
				print('images')
				print(e)
		
		if img_urls[i].lower().endswith('.svg') and img_urls[i] is not None:
			try:
				svg = requests.get(img_url).text
				svg_url = img_url.rsplit('/')[-1]
				svg_url_name = svg_url.rsplit('.')[0]
				svg2png(bytestring=svg, write_to='downloadedImages/' + svg_url_name.rsplit('/', 1)[-1] + '.png')
			except IOError as e:
				print('svg')
				print(e)

def checkUrl(img_url):
	if img_url.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.svg')):
		if img_url.startswith('http') == False:
			#check link exist or not
			if img_url.startswith('//'):
				try:
					response = requests.get('https:' + img_url)
					if response.status_code == 200:
						print('Image exist')
						img_url = 'https:' + img_url
				except IOError as e:
					print(e)
			else:			
				try:	
					response = requests.get(current_url + img_url)
					if response.status_code == 200:
						print('Image exist')
						img_url = current_url + img_url
				except IOError as e:
					print(e)

		print(img_url)
		return img_url


def getOtherMultimedia(soup):
	media_array = []
	src_list = soup.find_all('source')
	if src_list:
		video_array = []
		audio_array = []
		for src in src_list:
			if src.get('type').startswith('audio') or src.get('type').startswith('video'):
				src = src.get('src')
				print(src)
				if src.endswith(tuple(video_formats)):
					video_array.append(src)
				if src.endswith(tuple(audio_formats)):
					audio_array.append(src)

		media_array.append(video_array)
		media_array.append(audio_array)
	return media_array

def downloadHTMLAsPDF(url, filename):
	with open("output.html", "w", encoding="utf-8") as file:
		file.write(str(soup))

def updateHTML():
	recog_results = ImageRecognizer.predictImg();
	for key in recog_results.keys():
		#ele = soup.find_all(text=".*\s{recog_results[key][1]}*")
		ele = soup.find_all(src=re.compile(recog_results[key][1]))
		new_p = soup.new_tag("p")
		new_p.string = recog_results[key][1] + " " + recog_results[key][0]
		
		print(ele)
		print(new_p.string)
		for k in ele:
			k.insert_after(new_p)
			#soup.body.find(text=recog_results[key][1]).append(0, new_p)
		

def write_text(data: str, path: str):
    with open(path, 'w') as file:
        file.write(data)

def remove_files():
	files = glob.glob('downloadedImages/*')
	for f in files:
		os.remove(f)