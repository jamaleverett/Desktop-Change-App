#!/usr/bin/python3.7.1

from subprocess import run
import requests
import json
import urllib.request
import random
import os
import datetime

url = "https://api.unsplash.com/photos/random"
my_client_id = "" #Unsplash told me to keep this a secret :)

#prompts user for terms that will be used to search
# queries = []
# for i in range(3):
#     term = input("Provide a search term: ")
#     queries.append(term)

cur_dir = os.getcwd()
queries = []

#checks for .txt file with search terms. If it doesnt exists, program creates one
if "search_terms.txt" in os.listdir(cur_dir):
	#read txt file for queries; automates a few steps 
	#after program has been run already
	txt = open("search_terms.txt", "r")
	queries = txt.read().split(',')
else:
	txt = open("search_terms.txt", "w")
	#prompts user for terms that will be used to search
	for i in range(3):
		term = input("Provide a search term: ")
		queries.append(term)
	for each in queries:
		txt.write(each + ',')

#selects a random term to search Unsplash for
term = random.choice(queries)    

search = {"query": term, "orientation": "landscape"}

#Header argument is provided by Unsplash to ensure v1 photos are the only results returned
response = requests.get(url + my_client_id, 
	headers={"Accept-Version": 'v1'}, params = search)

x = json.loads(response.content)

links = x['urls']
download = links['raw']
#print(download)

filename = download[34:41] + ".jpg"

#be sure this script has the correct path
script = "osascript -e 'tell application \"System Events\" to tell every desktop to set picture to \"~/Documents/Projects/unsplash_program/" + filename + "\"'"

#working retrieval of a raw .jpg format of the given photo
urllib.request.urlretrieve(download, download[34:41] + ".jpg")


# this shell script will set background as the downloaded image without feedback
# osascript -e 'tell application "System Events" to tell every desktop to set picture to "~/Documents/unsplash_program/background.jpg"'

#WILL NOT WORK WITHOUT "shell=True"
run(script, shell=True)

#open/creates a file to save photo urls & the date that photo was set as the background
file = open("photo_urls.txt","a+")
file.write(str(datetime.datetime.today().strftime('%Y-%m-%d')) + ": " + download + "\n")

#removes the downloaded file from the computer
os.remove(filename)
