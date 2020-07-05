#This script scrapes the Hacker News website for data. It finds the highest voted articles and gathers them into a list.
#It outputs a list which includes the links of the articles, their title and their vote number. The links are listed in descending order based on their votes.
#Launch the script from terminal (command line) and enter: scrape.py i 	<-- where "i" is the number of pages you want to scrape on the site
import pprint
import requests
from bs4 import BeautifulSoup
import time
import sys

pages = int(sys.argv[1])	#how many pages to scrape. Always start the script from terminal and give a page number

site_url = "https://news.ycombinator.com/news?p="	

def printy(arg):	#for nicer prints
	pprint.pprint(arg)

def sort_by_votes(result):	#sorts the final list which contains the date
	return sorted(result, key = lambda k: k["votes"], reverse = True)

def crawl_site(site_url, pages):
	result = []
	while pages > 0:
		url = site_url + str(pages)
		#get the page and the html content
		req = requests.get(url)
		soup = BeautifulSoup(req.text, 'html.parser')
		#generate the storylink class which contains the links and the titles, and the subtext class which contains the votes
		links = soup.select(".storylink")
		points = soup.select(".subtext")
		#iterate through the links list and take the items which have at least 100 votes. Then append them to the list called "result".
		for index, item in enumerate(links):
			text = links[index].getText()
			link = links[index].get("href", None)
			score = points[index].select(".score")
			if len(score):
				vote = int(score[0].getText().replace(" points", ""))
				if vote >= 100:
					result.append({"title" : text, "link" : link, "votes" : vote})
		pages -= 1	#decrease the page so we can scrape the next page
		time.sleep(0.03)	#put the script to sleep for 30 millisecond. The Hacker News asks for a scrape delay of 30 in their robots.txt file.
	return printy(sort_by_votes(result))

if (__name__ == "__main__"):
	crawl_site(site_url, pages)