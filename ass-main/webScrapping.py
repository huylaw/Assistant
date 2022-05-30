import wikipedia
import webbrowser
import requests
from bs4 import BeautifulSoup
import threading
import smtplib
import urllib.request
import os
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import sys
sys.stdout.buffer.write(chr(9986).encode('utf8'))

EMAIL = 'lhuy4831@gmail.com'
PASSWORD = '0377909471'
def wikiResult(query):
	query = query.replace('wikipedia','')
	query = query.replace('tìm kiếm','')
	if len(query.split())==0: query = "wikipedia"
	try:
		return wikipedia.summary(query, sentences=2)
	except Exception as e:
		return "Desired Result Not Found"


def maps(text):
	text = text.replace('maps', '')
	text = text.replace('map', '')
	text = text.replace('google', '')
	openWebsite('https://www.google.com/maps/place/'+text)

def giveDirections(startingPoint, destinationPoint):

	geolocator = Nominatim(user_agent='assistant')
	if 'tại đây' in startingPoint:
		res = requests.get("https://ipinfo.io/")
		data = res.json()
		startinglocation = geolocator.reverse(data['loc'])
	else:
		startinglocation = geolocator.geocode(startingPoint)

	destinationlocation = geolocator.geocode(destinationPoint)
	startingPoint = startinglocation.address.replace(' ', '+')
	destinationPoint = destinationlocation.address.replace(' ', '+')

	openWebsite('https://www.google.co.in/maps/dir/'+startingPoint+'/'+destinationPoint+'/')

	startinglocationCoordinate = (startinglocation.latitude, startinglocation.longitude)
	destinationlocationCoordinate = (destinationlocation.latitude, destinationlocation.longitude)
	total_distance = great_circle(startinglocationCoordinate, destinationlocationCoordinate).km #.mile
	return str(round(total_distance, 2)) + 'KM'

def openWebsite(url='https://www.google.com/'):
	webbrowser.open(url)

def jokes():
	URL = 'https://icanhazdadjoke.com/'
	result = requests.get(URL)
	src = result.content

	soup = BeautifulSoup(src, 'html.parser')

	try:
		p = soup.find('p')
		return p.text
	except Exception as e:
		raise e

def youtube(query):
	from youtube_search import YoutubeSearch
	query = query.replace('play',' ')
	query = query.replace('on youtube',' ')
	query = query.replace('youtube',' ')
	results = YoutubeSearch(query,max_results=1).to_dict()
	webbrowser.open('https://www.youtube.com/watch?v=' + results[0]['id'])
	return "Enjoy Sir..."


def googleSearch(query):
	if 'image' in query:
		query += "&tbm=isch"
	query = query.replace('images','')
	query = query.replace('image','')
	query = query.replace('search','')
	query = query.replace('show','')
	webbrowser.open("https://www.google.com/search?q=" + query)
	return "Here you go..."


def email(rec_email=None, text="Hello, It's P.A.N.D.A here...", sub='P.A.N.D.A'):
	if '@gmail.com' not in rec_email: return 1
	text=text.encode('ascii', 'ignore').decode('ascii')
	sub=sub.encode('ascii', 'ignore').decode('ascii')
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(EMAIL, PASSWORD)
	message = 'Subject: {}\n\n{}'.format(sub, text)
	s.sendmail(EMAIL, rec_email, message)
	print("Sent")
	s.quit()
	return 0

