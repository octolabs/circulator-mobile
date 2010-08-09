import logging
import geo
import models
import wsgiref.handlers
import urllib2
from google.appengine.ext import db
from google.appengine.ext import webapp
from datetime import datetime
from datetime import timedelta

class MobileHandler(webapp.RequestHandler):

	def getHeader(self, pageTitle):
		self.response.out.write('''<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.2//EN" 
	"http://www.openmobilealliance.org/tech/DTD/xhtml-mobile12.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>Circulator Mobile</title>
	<link href="/static/css/default.css" type="text/css" rel="stylesheet" />
</head>
<body>
<h1>%s</h1>
<p>
''' % (pageTitle))

	def getFooter(self):
		self.response.out.write('''
<img src="http://tracking.percentmobile.com/pixel/8ff4c106-3468-11de-a785-12313900c5b8" alt="." width="2" height="2" />
</body>
</html>''')


class SupportHandler(MobileHandler):
	def get(self):
		self.getHeader('Where is My Bus?<br/>iPhone app for DC Circulator')

		self.response.out.write("""<p>
Where's My Bus? is a new mobile application for DC's popular Circulator bus and is one of the first tools to provide real time information on the location of a rider's bus, through a simple, easy to use interface. 
<br/>
<br/>
Application lets riders select a Circulator route and bus stop to find out how close the next bus is whether they are at home, the office, or on the go. The application uses real-time GPS data so bus riders can have up-to-the-minute information on all Circulator buses at their fingertips. 
<br/>
<br/>
The DC Circulator surface transit service was launched in July 2005 and has transported more than 8 million workers, residents and visitors quickly and inexpensively around central Washington since its inception. The Circulator has five routes connecting through the District's commercial core, the 43 buses have low floors, multiple doors for easy on-and-off service, and large windows for easy viewing along the route. 
<br/>
<br/>
The Circulator has a simple fare structure of $1 per ride making it easy for people to hop on the bus and pay cash, or purchase tickets in advance online or at curbside multi-space parking meters. Circulator buses arrive at stops every ten minutes throughout the day. 
		</p>
		<hr/>
		""")


		self.response.out.write("""<p>Submit your
			<a href="https://spreadsheets.google.com/a/dc.gov/viewform?hl=en&formkey=dFV1bmhtRlYtU2gzcXdhQ0hJdllhOVE6MA..">feedback</a><br/>
		</p>""")

 

		self.getFooter()



def main():
	application = webapp.WSGIApplication(
		[('/iphone/support', SupportHandler)],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
