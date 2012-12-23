#! /usr/bin/python

import sys
import feedparser
import socket
import time
from HTMLParser import HTMLParser
from datetime import date


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

try:
	with open('events.txt','a') as f:
		f.close()
		pass
except IOError as e:
	f = open('events.txt','w')
	f.write('\n')
	f.close()
	print 'Created events.txt'
try:
	with open('last_update.txt','a') as f:
		f.close()
		pass
except IOError as e:
	f = open('last_update.txt','w')
	f.write('\n')
	f.close()
	print 'Created last_update.txt'

timeout = 120
socket.setdefaulttimeout(timeout)
feed_url = "https://www.dropbox.com/12773868/142359555/fqXaYXQ1UqCXLyoBhYeNlAPJiyvhwr2XbbAknnIQ/events.xml"
d = feedparser.parse(feed_url)

f_update = open('last_update.txt','r')
f_events = open('events.txt','a')
lastmodified = f_update.readline()
print lastmodified
timestamp = time.mktime(d.entries[0].updated_parsed)
print repr(timestamp)
#print lastmodified
#print unicode(d.entries[0].updated).encode("utf-8")
if not lastmodified.rstrip('\n') == repr(timestamp):
	f_update.close()
	f_update = open('last_update.txt','w')
	print "Dropbox has been updated"
	#write to f_updated new update time here
	f_update.write(repr(timestamp))
	lastmodified = lastmodified.rstrip('\n')
	for s in d.entries:
		#if not "You" in unicode(s.description).encode("utf-8"):
			if float(lastmodified) < time.mktime(s.updated_parsed):
				try:
					description_string = strip_tags(unicode(s.description).encode("utf-8"))
					f_events.write(str(time.mktime(s.updated_parsed)) + "," + description_string)
				except IOError  as errormsg:
					#print unicode(s.updated_parsed).encode("utf-8") + "," + unicode(s.updated).encode("utf-8") + "," + unicode(s.description).encode("utf-8") + "\n"
					f_events.write(unicode(s.updated).encode("utf-8") + "," + unicode(s.description).encode("utf-8") + "\n")
	
#maxentries = len(d.entries)
#print maxentries
f_events.close()
f_update.close()




