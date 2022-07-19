'''
Libraries Used
BeautifulSoup : HTML parser
svg2png : converting the svg images to PNG



'''



from bs4 import BeautifulSoup
import urllib
from  urllib.request import urlopen
from urllib.parse import urlparse
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

#Set the audio and video formats that the application can read
audio_formats = ['.mp3', '.m4a', '.flac', '.wav', '.wma', '.aac', '.ogg']
video_formats = ['.mp4', '.mov', '.wmv', '.avi', '.swf', '.flv', '.f4v', '.mkv', '.webm']

#Running the application
class ImgToTxtApp:
	def setURL(self, url):
		global current_url
		global main_url
		global parsed
		global soup

		remove_files()

		results = []
		isURLValid = validators.url(url)
		if isinstance(isURLValid, validators.ValidationFailure):
			return False
		#Open the URL
		page = urlopen(url).read()
		#Parsing the webpage to BeautifulSoup
		soup = BeautifulSoup(page, 'html.parser')

		current_url = url
		parsed = urlparse(url)
		main_url = parsed.scheme + '://' + parsed.netloc
		print(main_url)
		#Get list of hyperlinks
		link_array = readLinks(soup)
		results.append(link_array)
		#Get list of image links
		img_array = getImages(soup)
		results.append(img_array)
		#Get list of multimedia links
		media_array = getOtherMultimedia(soup)
		results.append(media_array)
		updateHTML()
		downloadHTML()
		downloadHTMLAsPlainText()
		#generatePDFFromHTML()
		#predictedResults = ImageRecognizer.predictImg()

		return results

#Functions
#Checking the links available within BeautifulSoup
#Seperating the links whether is it a local path or hyperlink
#Differeniated with HTTP or not.
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


#Get all the images from img tag or source tag
#After finding the images, the images will be downloaded
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

#Downloading of images with '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif' formats and save the images with its original name
def downloadImages(img_urls):
	for i in range(len(img_urls)):
		old_img_url = img_urls[i]
		#Checking whether image exist
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
#Check if the images exist by requesting of the image URL
#if the status code is 200 (mean success), then it is able to download
def checkUrl(img_url):
	#print("hello " + img_url)
	imgUrlParsed = urlparse(img_url)
	if img_url.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.svg')):
		if imgUrlParsed.scheme != "":
		#check link exist or not
			print("hello " + img_url)
			try:
				response = requests.get(img_url)
				if response.status_code == 200:
					print('Image exist')
					#img_url = 'https:' + img_url
			except IOError as e:
				print(e)
		elif img_url.startswith("//"):
			try:
				#print("helloagain " + img_url)
				response = requests.get(parsed.scheme +":"+ img_url)
				if response.status_code == 200:
					print('Image exist')
					img_url = parsed.scheme + ":" + img_url
			except IOError as e:
				print(e)
		else:			
			try:	
				print("hello2 " + (main_url + img_url))
				response = requests.get(main_url + img_url)
				if response.status_code == 200:
					print('Image exist')
					img_url = main_url + img_url
			except IOError as e:
				print(e)
		print(img_url)
		return img_url

#Get all the multimedia links from source tag with either audio or video type
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
	return [[], []]

#Download the HTML with the updated results
def downloadHTML():
	with open("output.html", "w", encoding="utf-8") as file:
		file.write(str(soup))

def downloadHTMLAsPlainText():
	with open('output.txt', 'w', encoding='utf-8') as f:
		f.write(soup.get_text())			

#def generatePDFFromHTML():
#	pdfkit.from_url(current_url, 'output.pdf')
#Insert the predicted results to the HTML
def updateHTML():
	recog_results = ImageRecognizer.predictImg();
	ocr_results = ImageRecognizer.predictOCR();
	for key in recog_results.keys():
		#ele = soup.find_all(text=".*\s{recog_results[key][1]}*")
		splitImageName = recog_results[key][1].rsplit(".", 1)
		if(splitImageName[-1] == "png"):
			ele = soup.find_all(src=re.compile(splitImageName[0]+".png"))
			if ele:
				new_p = soup.new_tag("p")
				#new_p.string = recog_results[key][1] + "\n recog: " + recog_results[key][0] + "\n ocr: " + ''.join(ocr_results[key])
				new_p.string = "recog: " + recog_results[key][0] + "\n ocr: " + ''.join(ocr_results[key])
			ele = soup.find_all(src=re.compile(splitImageName[0]+".svg"))
			if ele:
				new_p = soup.new_tag("p")
				new_p.string = "recog: " + recog_results[key][0] + "\n ocr: " + ''.join(ocr_results[key])
		else:
			ele = soup.find_all(src=re.compile(recog_results[key][1]))
			if ele:
				new_p = soup.new_tag("p")
				new_p.string = "recog: " + recog_results[key][0] + "\n ocr: " + ''.join(ocr_results[key])
		
		#print(ele)
		#print(new_p.string)
		for k in ele:
			k.insert_after(new_p)
			#soup.body.find(text=recog_results[key][1]).append(0, new_p)


#Remove all images from downloadedIMages folder everytime application runs
def remove_files():
	files = glob.glob('downloadedImages/*')
	for f in files:
		os.remove(f)