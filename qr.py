import logging
import geo
import models
import wsgiref.handlers
import urllib2
from google.appengine.ext import db
from google.appengine.ext import webapp
from datetime import datetime
from datetime import timedelta

import cgi
import models

class MainHandler(webapp.RequestHandler):
	def get(self):
		

		busnumber=self.request.path.split('/')[2]
		pageTitle="I'm on the Bus! </br> for DC Circulator"
		
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
			''' % (pageTitle))
		self.response.out.write('''<h2>You found it!</h2>
		
		Congratulations! You found this QR tag on the Circulator bus.
		<br/>
		Thank you for riding with us, please provide your feedback using the form below.
		<br/>
		<br/>
		Compliments or complaints (bus #%s):
		<br/>
		<form action="/bus/" method="post">
          <div><input type="hidden" name="busnumber" value="#%s"></input></div>
          <div><textarea name="comments" rows="3" cols="40"></textarea></div>
          <div><input type="submit" value="Submit"></div>
        </form>
		
		<br/>
		<br/>
		<i>If you have ideas for what information you want to see on this page, drop us a line at <a href="mailto:octolabs@dc.gov">octolabs@dc.gov</a> or tweet <a href="http://twitter.com/octolabs">@octolabs</a></i>
		<br/>
		<br/>
		To get information on Circulator arrivals check <a href="http://circulator.dc.gov">"Where's My Bus"</a> application.
		
		''' % (busnumber, busnumber))
		
		self.response.out.write('''
			</body>
			</html>''')
    
	def post(self):
		feedback = models.Feedback()

		feedback.busnumber = self.request.get('busnumber')
		feedback.comments = self.request.get('comments')
		feedback.put()
		
		pageTitle="I'm on the Bus! </br> for DC Circulator"
		
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
			
			''' % (pageTitle))
			
		self.response.out.write('Thank you for your feedback!')


		
		self.response.out.write('''
			</body>
			</html>''')

def main():
	application = webapp.WSGIApplication(
		[('/bus/.*', MainHandler),],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()
