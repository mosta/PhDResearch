# libraries
import sys
from bs4 import BeautifulSoup
import commands
import urllib2
import re, math
import os
from operator import itemgetter
from datetime import datetime
import io, json
import calendar
import time
from timeout import timeout

@timeout(60)
def getTopsyTweets(path, ID, URL, timestamp):
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


        with open(path+ID+"_"+timestamp+".topsy", 'w') as outfile:
                json.dump(results, outfile)

@timeout(60)
def getSnapshotofURL(path, ID, URL, timestamp):
        page = commands.getoutput("casperjs/bin/casperjs takesnapshot.js '"+URL+"' '"+path+"' '"+ID+"_"+timestamp+"'")
        fileout = open(path+ID+"_"+timestamp+".html", 'w')
        fileout.write(page)
        fileout.close()



timenow = str(calendar.timegm(time.gmtime()))
ID = sys.argv[1]
URL = sys.argv[2]
path = "/srv/www/phdresearch/CollectedData/"+ID+"/"
if(os.path.exists(path)==False):
        commands.getoutput("mkdir "+path)
        
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

json_data=open('/srv/www/phdresearch/awscredentials_s3.txt')
data = json.load(json_data)
json_data.close()
S3connection = S3Connection(data["aws_key"],data["aws_secret"])
S3bucket = S3connection.get_bucket('longitudinalstudy')

try:
	getSnapshotofURL(path, ID, URL, timenow)
	topsyFileName = ID+"_"+timenow+".topsy"
	getTopsyTweets(path, ID, URL,timenow)
	htmlFileName = ID+"_"+timenow+".html"
	pngFileName = ID+"_"+timenow+".png"
	
	newfile = Key(S3bucket)
	newfile.key = topsyFileName
	newfile.set_contents_from_filename(path+topsyFileName)
	newfile = Key(S3bucket)
	newfile.key = htmlFileName
	newfile.set_contents_from_filename(path+htmlFileName)
	newfile = Key(S3bucket)
	newfile.key = pngFileName
	newfile.set_contents_from_filename(path+pngFileName)
	
	commands.getoutput("rm -f "+path+topsyFileName)
	commands.getoutput("rm -f "+path+htmlFileName)
	commands.getoutput("rm -f "+path+pngFileName)
except:
	pass

