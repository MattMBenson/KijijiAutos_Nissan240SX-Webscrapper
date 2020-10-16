# webscraper to search for cars listed on various sites and create a google spreadsheet #
from bs4 import BeautifulSoup
import requests
import csv 

#                    Vehicle Object                                     #
class Vehicle:
	def __init__(self, title, price, kilometres, location, transmission):
		self.title = title
		self.price = price
		self.kilometres = kilometres
		self.location = location
		self.transmission =  transmission

	def printTitle(self):
		print("Title: ",self.title)
	def printPrice(self):
		print("Price: ",self.price)
	def printKilo(self):
		print("Kilometres: ",self.kilometres)
	def printLocation(self):
		print("Location: ",self.location)
	def printTrans(self):
		print("Transmission: ",self.trans)


URL = 'https://www.kijijiautos.ca/cars/nissan/240-sx/#ms=18700%3B44&od=down&sb=ct&shortDescription=true'
request = requests.get(URL, headers={'User Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'})
HTML = request.content
soup = BeautifulSoup(HTML,'html.parser')
LISTINGS = soup.find_all(class_='_2HOXt4_JUGriV5QrKxi-Be _2pZK6skcaaZg4HoaZda9Rl') # entire listing

ALL_LISTINGS = [] # list of car objects

for carListing in LISTINGS:
	TITLE = carListing.find(class_='_3jBWYAEU6W4f4h0_uQWlSw').text.strip() # title of ad
	KILOMETRES = carListing.find(class_='CHKTkxN--fPPouXAdU7EV DMyxB523aaKjukBpw8RVf').text.strip() # kilometres
	LOCATION = carListing.find(class_='CHKTkxN--fPPouXAdU7EV DMyxB523aaKjukBpw8RVf _1nxETRmdJY_lgfg1uXbgn9').text.strip() # location
	TRANS = carListing.find(class_='CHKTkxN--fPPouXAdU7EV DMyxB523aaKjukBpw8RVf _1nxETRmdJY_lgfg1uXbgn9').text.strip() # transmission
	PRICE = carListing.find(class_='_2zkxeQN7m4FOG4I3VDi6Ue _2vzukMZ1OuwuqTy7CPad-i mjWfW13SHgIHyZfo80E9P _3xSlJhtw8c66mKjEAmR5A').text.strip() # price
	# ADD AN OPTION TO GET IMAGE -- MAKE IMAGE PART OF CAR OBJECT 
	car = Vehicle(TITLE,PRICE,KILOMETRES,LOCATION,TRANS)
	ALL_LISTINGS.append(car)

# create csvFile
file = open('240-SX_Listings','w')
writer = csv.writer(file)

# header row
writer.writerow(['Listing','Price','Kilometres','Location,','Transmission'])

for i in ALL_LISTINGS:
	writer.writerow([i.title,i.price,i.kilometres,i.location,i.transmission])

file.close()	