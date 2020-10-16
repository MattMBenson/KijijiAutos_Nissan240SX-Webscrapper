# webscraper to search for cars listed on various sites and create a google spreadsheet #
from bs4 import BeautifulSoup
import requests
import csv 

#input your make and model you would like to search for, formatted like Kijiji Autos
CAR_MAKE ='nissan'
CAR_MODEL='240-sx'


#                    Vehicle Object                                     #
class Vehicle:
	def __init__(self, title, price, kilometres, location, linkid):
		self.title = title
		self.price = price
		self.kilometres = kilometres
		self.location = location
		self.linkid =  linkid

URL = 'https://www.kijijiautos.ca/cars/'+CAR_MAKE+'/'+CAR_MODEL+'/'
request = requests.get(URL, headers={'User Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'})
HTML = request.content
soup = BeautifulSoup(HTML,'html.parser')
LISTINGS = soup.find_all(class_='_2HOXt4_JUGriV5QrKxi-Be _2pZK6skcaaZg4HoaZda9Rl') # entire listing

ALL_LISTINGS = [] # list of car objects

for carListing in LISTINGS:
	TITLE = carListing.find(class_='_3jBWYAEU6W4f4h0_uQWlSw').text.strip() # title of ad
	KILOMETRES = carListing.find(class_='CHKTkxN--fPPouXAdU7EV DMyxB523aaKjukBpw8RVf').text.strip() # kilometres
	LOCATION = carListing.find(class_='CHKTkxN--fPPouXAdU7EV DMyxB523aaKjukBpw8RVf _1nxETRmdJY_lgfg1uXbgn9').text.strip() # location
	LINK = carListing.get('data-test-ad-id') # URL STRING
	PRICE = carListing.find(class_='_2zkxeQN7m4FOG4I3VDi6Ue _2vzukMZ1OuwuqTy7CPad-i mjWfW13SHgIHyZfo80E9P _3xSlJhtw8c66mKjEAmR5A').text.strip() # price

	# ADD AN OPTION TO GET IMAGE -- MAKE IMAGE PART OF CAR OBJECT 
	car = Vehicle(TITLE,PRICE,KILOMETRES,LOCATION,LINK)
	ALL_LISTINGS.append(car)

#create csvFile
file = open(CAR_MODEL+' Listings.csv','w')
writer = csv.writer(file,lineterminator='\n')

# header row
writer.writerow(['Title of Listing','Asking Price','Kilometres','Seller Location,','KijijiAutos Link'])

for i in ALL_LISTINGS:
	autoLink = 'https://www.kijijiautos.ca/cars/'+CAR_MAKE+'/'+CAR_MODEL+'/used/#vip='+i.linkid+' '
	writer.writerow([i.title,i.price,i.kilometres,i.location,autoLink])

file.close()	