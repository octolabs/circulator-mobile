import cgi
import models
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import time
from datetime import datetime
from datetime import timedelta

import wsgiref.handlers

from google.appengine.ext import webapp

class Kml (webapp.RequestHandler):
	def get(self):
		self.response.content_type = "application/kml+xml"

		self.response.out.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>')
		self.response.out.write("""
	<Style id="green_endpoint">
		<IconStyle>
			<color>ff00ff00</color>
			<scale>1.4</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/target.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>

	<Style id="green_bus">
		<IconStyle>
			<color>ff00ff00</color>
			<scale>0.6</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/bus.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>


	<Style id="green_busstop">
		<IconStyle>
			<color>ff00ff00</color>
			<scale>1.2</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>


	<Style id="red_endpoint">
		<IconStyle>
			<color>ff0000ff</color>
			<scale>1.4</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/target.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>

	<Style id="red_bus">
		<IconStyle>
			<color>ff0000ff</color>
			<scale>0.6</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/bus.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>


	<Style id="red_busstop">
		<IconStyle>
			<color>ff0000ff</color>
			<scale>1.2</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>


	<Style id="blue_endpoint">
		<IconStyle>
			<color>ffff0000</color>
			<scale>1.4</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/target.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>

	<Style id="blue_bus">
		<IconStyle>
			<color>ffff0000</color>
			<scale>0.6</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/bus.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>


	<Style id="blue_busstop">
		<IconStyle>
			<color>ffff0000</color>
			<scale>1.2</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>


	<Style id="yellow_endpoint">
		<IconStyle>
			<color>ff00ffff</color>
			<scale>1.4</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/target.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>

	<Style id="yellow_bus">
		<IconStyle>
			<color>ff00ffff</color>
			<scale>0.6</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/bus.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>


	<Style id="yellow_busstop">
		<IconStyle>
			<color>ff00ffff</color>
			<scale>1.2</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>


	<Style id="purple_endpoint">
		<IconStyle>
			<color>ff0f000f</color>
			<scale>1.4</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/target.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>

	<Style id="purple_bus">
		<IconStyle>
			<color>ff0f000f</color>
			<scale>0.6</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/bus.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>


	<Style id="purple_busstop">
		<IconStyle>
			<color>ff0f000f</color>
			<scale>1.2</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
			</Icon>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>
		""")

		d = timedelta(minutes=5)
		d2 = timedelta(hours=5)
		now = datetime.utcnow() 
		last5minutes = now-d-d2


		buses = models.Bus.all().filter('gps_date >= ', last5minutes)
		for bus in buses:
			if (bus.status=="On Route"):
				self.response.out.write("<Placemark><name>Bus #%s</name><styleUrl>#%s_bus</styleUrl><description>On %s route (#%s)<br/>Intersection: %s, <br/> Velocity: %s, Direction: %s <br/> Time: %s</description><Point><coordinates>%s,%s,0</coordinates></Point></Placemark>" % (bus.number,bus.route_color,bus.route_color,bus.route_id,bus.intersection,bus.velocity, bus.direction, bus.gps_date, bus.lon,bus.lat))
			else:
				self.response.out.write("<Placemark><name>Bus #%s</name><styleUrl>#%s_bus</styleUrl><description>No passengers<br/>Intersection: %s, <br/> Velocity: %s, Direction: %s <br/> Time: %s</description><Point><coordinates>%s,%s,0</coordinates></Point></Placemark>" % (bus.number,bus.route_color,bus.intersection,bus.velocity, bus.direction, bus.gps_date, bus.lon,bus.lat))
					
  
		self.response.out.write('</Document></kml>')


def main():
  application = webapp.WSGIApplication([('/api/circulator.kml', Kml)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()




