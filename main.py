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

	def get_buses_before(self, route_id, stop_id):
		logging.debug("SELECT * FROM Bus WHERE route_id=%s and stop_id<%s order by stop_id desc" %
			(route_id, stop_id))
		buses = db.GqlQuery("SELECT * FROM Bus WHERE route_id=%s and stop_id<%s order by stop_id desc LIMIT 3" %
			(route_id, stop_id))

		route_id2 = db.GqlQuery("SELECT * FROM Route WHERE route_id=%s"  % (route_id)).get().complimentary_route_id
		
		buses2 = db.GqlQuery("SELECT * FROM Bus WHERE route_id=%s order by stop_id desc LIMIT 3" %
			(route_id2))
		
		return {"buses":buses,"complimentary_buses":buses2}

	def get_bus_info(self, bus):
		if (bus.stop_id!=None):
			stop=self.get_stop_name(bus.stop_id)
			return "Bus #%s is near %s" % (bus.number, bus.intersection)
		else:
		    return "Bus #%s is near %s" % (bus.number, bus.intersection)
    
	def get_stop_name(self, stop_id):
		stop =  db.GqlQuery("SELECT * FROM BusStop WHERE stop_id=%s"  % (stop_id)).get()
		return stop.name
	
	

class MainHandler(MobileHandler):
	def get(self):
		self.getHeader('Where is My Bus?<br/>for DC Circulator')
		self.response.out.write('<p><b>Select Your Route</b></p>')

		self.response.out.write("""<p>
			<strong>1</strong> <a href="/whereismybus/color?color=blue" accesskey="1">Union Station - Navy Yard Metro</a><br/>
			<strong>2</strong> <a href="/whereismybus/color?color=green" accesskey="2">Woodley Park - Adams Morgan - McPherson Square Metro</a><br/>
			<strong>3</strong> <a href="/whereismybus/color?color=red" accesskey="3">Convention Center - SW Waterfront</a><br/>
			<strong>4</strong> <a href="/whereismybus/color?color=yellow" accesskey="4">Georgetown - Union Station</a><br/>
			<strong>5</strong> <a href="/whereismybus/color?color=purple" accesskey="5">Smithsonian - National Gallery of Art Loop</a>
		</p>""")


		self.response.out.write("""
		<hr/>
		<p>
		<strong>0</strong> <a href="/" accesskey="0">Home</a><br />
		</p>
		""")
		self.getFooter()


class ChallengeHandler(webapp.RequestHandler):
	def get(self):


		self.response.out.write("""
		<h1> Circulator Open Data Challenge</h1>
		
		<h2>Categories:</h2>
		Public app (mobile or web)
		<br/>
		Visualization
		<br/>
		Internal app (to be used by DDOT/WMATA and FirstTransit)
		<br/>
		<br/>		
		<br/>
		Stay tuned for more info!

		""")



class WhereIsMyBusHandler(MobileHandler):
	def get(self):
		color = self.request.get('color', '')
		self.getHeader('Select Your Direction')
		routes = db.GqlQuery("SELECT * FROM Route WHERE color='%s'" % color)
		i=0
		for route in routes:
			i=i+1
			self.response.out.write('''
			<strong>%s</strong> <a href="/whereismybus/route?route_id=%s" accesskey="%s">%s</a><br />
			''' % (i, route.route_id, i, route.direction))

		self.response.out.write("""
		<hr/>
		<p>
		<strong>0</strong> <a href="/" accesskey="0">Home</a><br />
		</p>
		""")
		self.getFooter()



class RouteHandler(MobileHandler):
	def get(self):
		route_id = self.request.get('route_id', '')
		route = db.GqlQuery("SELECT * FROM Route WHERE route_id=%s" % route_id).get()
		self.getHeader('Pick Your Stop')
		self.response.out.write('<p>')
		self.response.out.write('<b>%s</b><br/><br/>' % route.direction)
		
		
		stops = db.GqlQuery("SELECT * FROM BusStop WHERE route_id=%s ORDER BY stop_id" % route_id) 
		#stops = db.GqlQuery("SELECT * FROM BusStop WHERE route_id=%s" % route_id)
		i=0
		for stop in stops:
			i=i+1
			self.response.out.write('<strong>%s</strong> <a href="/whereismybus/stop?route_id=%s&stop_id=%s" accesskey="%s">%s</a><br />' % (i, route_id, stop.stop_id, i, stop.desc))
		self.response.out.write('</p>')

		self.response.out.write('<p>')
		self.response.out.write('Timetable: %s' % (route.schedule))
		self.response.out.write('</p>')
		
		self.response.out.write('''
		<hr/>
		<p>
		<strong>0</strong> <a href="/" accesskey="0">Home</a><br />
		</p>
		''')
		self.getFooter()


class StopHandler(MobileHandler):
	def get(self):
		route_id = self.request.get('route_id', '')
		route = db.GqlQuery("SELECT * FROM Route WHERE route_id=%s" % route_id).get()
		stop_id = self.request.get('stop_id', 1)
		stop = db.GqlQuery("SELECT * FROM BusStop WHERE stop_id=%s" % stop_id).get()
		self.getHeader('%s' % (stop.name))

		self.response.out.write('<p>')
		self.response.out.write('<b>%s</b>' % (route.direction))
		#self.response.out.write('Coordinates: %s, %s' % (stop[0].stop_lat, stop[0].stop_lon))
		self.response.out.write('</p>')

		#get all buses on stops before this
		all_buses=self.get_buses_before(route_id, stop_id)
		buses=all_buses["buses"]
		buses2=all_buses["complimentary_buses"]
		
		if ((buses.count()==0) and (buses2.count()==0)):
			self.response.out.write("<p>No buses on this route at this time</p>")
		count=0
		for bus in buses:
			#self.response.out.write('bus %s at stop %s <br/>' % (bus.busnumber, bus.stopnum))
			if (count==3):
				break
			self.response.out.write("<p>"+self.get_bus_info(bus))
			dist=geo.distance(bus.lat, bus.lon, stop.lat, stop.lon)
			self.response.out.write("<br/>%.1g mi. away</p>" % dist)
			count=count+1

		for bus in buses2:
			#self.response.out.write('bus %s at stop %s <br/>' % (bus.busnumber, bus.stopnum))
			if (count==3):
				break
			self.response.out.write("<p>"+self.get_bus_info(bus))
			dist=geo.distance(bus.lat, bus.lon, stop.lat, stop.lon)
			#self.response.out.write("<br/>%.1g mi. away</p>" % dist)
			self.response.out.write("<br/>bus is finishing previous route</p>")
			count=count+1

		self.response.out.write('<p>')
		self.response.out.write('Timetable: %s' % (route.schedule))
		self.response.out.write('</p>')
		
		time_format="%H:%M:%S %p"
		d = timedelta(minutes=5)
		d2 = timedelta(hours=4)
		#4 hours for summer time, 5 hours for winter time
		curr = datetime.utcnow()-d2
		curr2=curr.strftime(time_format)
				
		self.response.out.write('''
		<hr/>
		<p>
		Last Page Refresh: %s<br/>
		<strong>*</strong> <a href="http://circulator.dc.gov/whereismybus/stop?route_id=%s&stop_id=%s" accesskey="*">Refresh</a><br/>
		</p>
		<hr/>
		<p>
		<strong>0</strong> <a href="/" accesskey="0">Home</a><br />
		</p>
		''' % (curr2, route_id, stop_id))
		self.getFooter()


def main():
	application = webapp.WSGIApplication(
		[('/', MainHandler),
		('/challenge', ChallengeHandler),
		('/whereismybus/color', WhereIsMyBusHandler),
		('/whereismybus/route', RouteHandler),
		('/whereismybus/stop', StopHandler)],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
