# libraries
import sys
from bs4 import BeautifulSoup
import commands
import urllib2
import re, math
import sys
from operator import itemgetter
from datetime import datetime
import io, json
import calendar
import time


def getTopsyTweets(ID, URL, timestamp):
	results = []
	try:	
		offset = 0
		while(True):

			topsyURL = "http://topsy.com/trackback?url="+URL+"&perpage=100&offset="+str(offset)

			page = commands.getoutput("casperjs/bin/casperjs topsy.js '"+topsyURL+"'")
			if(page.find('No results found')!=-1):
				break	
			offset = offset + 100		

			soup = BeautifulSoup(page)
			for result in soup.find_all(True,{'class':'result-tweet'}):
				author = result.find(True,{'class':'pull-left'}).get("href")
				url  = result.find(True,{'class':'inline'}).find("a").get("href")
				tweet = result.find(True,{'class':'media-body'}).find("div")
				tweet =  ''.join(tweet.findAll(text=True))
				datetime = result.find(True,{'class':'relative-date'}).get("data-timestamp")
				results.append({"URL":url, "Tweet":tweet,"Timestamp": datetime})
	except:
		print sys.exc_info()
		
	
	with open("Snapshots/"+ID+"_"+timestamp+".topsy", 'w') as outfile:
		json.dump(results, outfile)

def getSnapshotofURL(ID, URL, timestamp):
	page = commands.getoutput("casperjs/bin/casperjs takesnapshot.js '"+URL+"' '"+ID+"_"+timestamp+"'")
	fileout = open("Snapshots/"+ID+"_"+timestamp+".html", 'w')
	fileout.write(page)
	fileout.close()



timenow = str(calendar.timegm(time.gmtime()))
ID = sys.argv[1]
URL = sys.argv[2]
getSnapshotofURL(ID, URL, timenow)
getTopsyTweets(ID, URL,timenow)

