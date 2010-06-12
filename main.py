import logging
import wsgiref.handlers
from google.appengine.ext import webapp
import os
from google.appengine.ext.webapp import template
import _nextbus

class MainHandler(webapp.RequestHandler):
	def get(self):
		title="Where is My Bus?<br/>for DC Circulator"
		body='<p><b>Select Your Route</b></p>'
		body=body+"""
		<hr/>
		<p>
		<strong>0</strong> <a href="/" accesskey="0">Home</a><br />
		</p>
		"""
		routes=_nextbus.get_all_routes_for_agency("dc-circulator")
		template_values = {'title': title,'body': body,'routes': routes,}
		path = os.path.join(os.path.dirname(__file__), 'routes.html')
		self.response.out.write(template.render(path, template_values))		

class RoutesHandler(webapp.RequestHandler):
	def get(self):
		path=self.request.path.split("/")
		
		route_tag=path[3]
		logging.debug(path)
		logging.debug(path[3])
		
		if (len(path)==5):
			direction_tag=path[4]

			title="Where is My Bus?<br/>for DC Circulator"
			body='<p><b>Select Bus stop</b></p>'
			body=body+"""
			<hr/>
			<p>
			<strong>0</strong> <a href="/" accesskey="0">Home</a><br />
			</p>
			"""
			
			direction=None
			route=_nextbus.get_route_config("dc-circulator",route_tag)
			for d in route.directions:
				logging.debug(d.tag)
				if (d.tag==direction_tag):
					direction=d
					for s in d.stops:
						logging.debug(s.stop_id+" - "+s.title)
			

			template_values = {'title': title,'body': body,'direction': direction,}
			path = os.path.join(os.path.dirname(__file__), 'direction.html')
			self.response.out.write(template.render(path, template_values))		
			
		else:
			title="Where is My Bus?<br/>for DC Circulator"
			body='<p><b>Select Direction</b></p>'
			body=body+"""
			<hr/>
			<p>
			<strong>0</strong> <a href="/" accesskey="0">Home</a><br />
			</p>
			"""
			route=_nextbus.get_route_config("dc-circulator", route_tag)
			template_values = {'title': title,'body': body,'route': route, "route_tag":route_tag}
			path = os.path.join(os.path.dirname(__file__), 'directions.html')
			self.response.out.write(template.render(path, template_values))		


class StopsHandler(webapp.RequestHandler):
	def get(self):
		path=self.request.path.split("/")

		stop_id=path[3]

		logging.debug(path)
		logging.debug(path[3])

		title="Where is My Bus?<br/>for DC Circulator"
		body='<p><b>Select Bus stop</b></p>'
		body=body+"""
		<hr/>
		<p>
		<strong>0</strong> <a href="/" accesskey="0">Home</a><br />
		</p>
		"""
		stop=_nextbus.get_predictions_for_stop("dc-circulator", stop_id)
		template_values = {'title': title,'body': body,'stop': stop,}
		path = os.path.join(os.path.dirname(__file__), 'stop.html')
		self.response.out.write(template.render(path, template_values))		

def main():
	application = webapp.WSGIApplication(
		[('/', MainHandler),
		('/whereismybus/route/.*', RoutesHandler),
		('/whereismybus/stop/.*', StopsHandler),
		],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
