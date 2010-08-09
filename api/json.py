import cgi
import models
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import time
from datetime import datetime

from django.utils import simplejson
import wsgiref.handlers

from google.appengine.ext import webapp

from main import MobileHandler

class Json (MobileHandler):
	def get(self):
		result=[]
		modelType = self.request.get('modelType', '')
		if modelType == 'Route':
			routes = models.Route.all()
			for route in routes:
				result.append({
					"route_id":route.route_id,
					"name":route.name,
					"desc":route.desc
					})
		elif modelType == 'BusStop':
			route_id = self.request.get('route_id', None)
			name = self.request.get('name', None)
			if route_id:
				try:
					stops = models.BusStop.all().filter("route_id = ", int(route_id))
				except: # always going to except!
					stops = models.BusStop.all()
			else:
				stops = models.BusStop.all()
			for stop in stops:
				result.append({
					"stop_id":stop.stop_id,
					"name":stop.name,
					"desc":stop.desc,
					"lat":stop.lat,
					"lon":stop.lon,
					"number":stop.number,
					"route_id":stop.route_id
					})
		elif modelType == 'Bus':
			data = {}
			
			route_id = self.request.get('route_id', '')
			route = models.Route.all().filter('route_id = ', int(route_id)).get()
			data['route_name'] = route.name
			
			timetables = models.Timetable.all().filter('route_id = ', int(route_id))
			timetablesInfo = ''
			for timetable in timetables:
				timetablesInfo = '%s %s %s-%s' % (timetablesInfo, timetable.day, timetable.begin, timetable.end)
			data['route_timetable'] = timetablesInfo.strip()
			
			stop_id = self.request.get('stop_id', 1)
			stop = models.BusStop.all().filter('stop_id = ', int(stop_id)).get()
			
			data['stop_name'] = stop.name
			
			data['buses'] = []
			data['info'] = ''
			#get all buses on stops before this
			buses=self.get_buses_before(route_id, stop_id)
			
			mapUrl = "http://maps.google.com/staticmap?size=320x416&maptype=mobile&markers=%s,%s" % (stop.lat, stop.lon)
			
			for bus in buses:
				mapUrl = "%s%%7C%s,%s,%s" % (mapUrl, bus.lat, bus.lon, bus.route_color)
				busDict = {}
				busDict['number'] = bus.number
				busDict['direction'] = bus.direction
				busDict['lat'] = bus.lat
				busDict['lon'] = bus.lon
				'''
				if (bus.intersection!=None):
					stop=self.get_stop_name(bus.intersection)
					data['info'] = "%s\nBus #%s is at %s." % (data['info'], bus.number, stop)
				elif (bus.to_busstop!=None and bus.from_busstop!=None):
					to_stop=self.get_stop_name(bus.to_busstop)
					from_stop=self.get_stop_name(bus.from_busstop)
					data['info'] = "%s\nBus #%s is between %s and %s." % (data['info'], bus.number, from_stop, to_stop)
				'''
				data['buses'].append(busDict)
			
			data['mapUrl'] = mapUrl
			result.append(data)
		else:
			buses = models.GPS.all()
			for bus in buses:
				result.append({
					"number":bus.number,
					"lat":bus.lat,
					"lon":bus.lon,
					"velocity":bus.velocity,
					"direction":bus.direction,
					"gps_date":bus.gps_date.isoformat()
					})

		self.response.content_type = "application/json"
		simplejson.dump(result, self.response.out)

def main():
  application = webapp.WSGIApplication([('/api/circulator.json', Json)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()




