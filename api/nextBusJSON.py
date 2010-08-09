import cgi
import models
import geo
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import time
from datetime import datetime
from datetime import timedelta

from django.utils import simplejson
import wsgiref.handlers

from google.appengine.ext import webapp

from main import MobileHandler

class NextBusJSON (MobileHandler):
	
	def get(self):
		result=[]
		route_id = self.request.get('route_id', '')
		route = db.GqlQuery("SELECT * FROM Route WHERE route_id=%s" % route_id).get()
		stop_id = self.request.get('stop_id', 1)
		stop = db.GqlQuery("SELECT * FROM BusStop WHERE stop_id=%s" % stop_id).get()
		
		#get all buses on stops before this
		all_buses=self.get_buses_before(route_id, stop_id)
		buses=all_buses["buses"]
		buses2=all_buses["complimentary_buses"]
		
		if ((buses.count()==0) and (buses2.count()==0)):
			result.append('No buses on this route at this time')
		count=0
		for bus in buses:
			if (count==3):
				break
			dist=geo.distance(bus.lat, bus.lon, stop.lat, stop.lon)
			result.append('%s %.1g mi. away' % (self.get_bus_info(bus), dist))
			count=count+1

		for bus in buses2:
			#self.response.out.write('bus %s at stop %s <br/>' % (bus.busnumber, bus.stopnum))
			if (count==3):
				break
			result.append('%s bus is finishing previous route' % self.get_bus_info(bus))
			count=count+1

		result.append('Timetable: %s' % (route.schedule))

		time_format="%H:%M:%S %p"
		d = timedelta(minutes=5)
		d2 = timedelta(hours=5)
		curr = datetime.utcnow()-d2
		curr2=curr.strftime(time_format)

		result.append('Last Page Refresh: %s' % curr2)

		self.response.content_type = "application/json"
		simplejson.dump(result, self.response.out)


def main():
  application = webapp.WSGIApplication([('/api/nextBus.json', NextBusJSON)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()




