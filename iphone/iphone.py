
import math
import geo
import logging
import models
import wsgiref.handlers
import urllib2
from google.appengine.ext import db
from google.appengine.ext import webapp



class MobileHandler(webapp.RequestHandler):


	def getHeader(self, pageTitle):
		self.response.out.write('''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta id="viewport" name="viewport" content="width=320; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;" />
	<title>%s</title>
	<link rel="stylesheet" href="/static/stylesheets/iphone.css" />
	<script type="text/javascript" charset="utf-8">
		window.onload = function() {
		  setTimeout(function(){window.scrollTo(0, 1);}, 100);
		}
	</script>
	  <script type="text/javascript" charset="utf-8" src="/static/js/phonegap.js"></script>
	  <script type="text/javascript" charset="utf-8">

    var getLocation2 = function(color) {
	  document.getElementById("page").style.display = "none"
	  document.getElementById("loading").style.display = "block"
	  document.getElementById("loading_msg").innerHTML= "getting your location..."

      var suc = function(p){
		    window.location = 'http://circulator.dc.gov/iphone/whereismybus/location?color='+color+'&lat='+p.latitude+'&lon='+p.longitude;
		    //alert('http://circulator.dc.gov/iphone/whereismybus/location?color='+color+'&lat='+p.latitude+'&lon='+p.longitude);
      };
      var fail = function(){};
      navigator.geolocation.getCurrentPosition(suc,fail);
    }

    var deviceInfo = function(){
      document.getElementById("platform").innerHTML = Device.platform;
      document.getElementById("version").innerHTML = Device.version;
      document.getElementById("uuid").innerHTML = Device.uuid;
    }
    
    var getLocation = function() {
      var suc = function(p){
		    alert(p.latitude + " " + p.longitude);
      };
      var fail = function(){};
      navigator.geolocation.getCurrentPosition(suc,fail);
    }
    
    var beep = function(){
	    navigator.notification.beep(2);
    }
	
  	var vibrate = function(){
  	  navigator.notification.vibrate(0);
  	}
	
  	var getContact = function(){
  	  var suc = function(c){ alert("Contact 4: " + c.contacts[3].name); };
  		var fail = function(){};
  		navigator.ContactManager.get(suc, fail);
  	}
  	
  	var watchAccel = function() {
  		var suc = function(a){
  			document.getElementById('x').innerHTML = roundNumber(a.x);
  			document.getElementById('y').innerHTML = roundNumber(a.y);
  			document.getElementById('z').innerHTML = roundNumber(a.z);
  		};
  		var fail = function(){};
  		var opt = {};
  		opt.frequency = 100;
  		timer = navigator.accelerometer.watchAcceleration(suc,fail,opt);
  	}
    	
    function roundNumber(num) {
      var dec = 3;
      var result = Math.round(num*Math.pow(10,dec))/Math.pow(10,dec);
      return result;
    }
    
	  var preventBehavior = function(e) { 
      e.preventDefault(); 
    };
		
		function init(){
		  document.addEventListener("touchmove", preventBehavior, false);
		  deviceInfo();
		}

		function go(url){
		  document.getElementById("page").style.display = "none"
		  document.getElementById("loading").style.display = "block"
	      document.getElementById("loading_msg").innerHTML = "loading..."
		  window.location = url;
		  deviceInfo();
		}
		
	  </script>
	
</head>

<body onload="init();">
	<div id="page" style="display: block">
	
''' % (pageTitle))

	def getFooter(self):
		self.response.out.write('''
		</div>
		<div id="loading" style="display: none">
		<br/>
		<br/>
		<br/>
		<br/>
		<center>
		<img src="/static/img/loading.gif" /><br /> 
			<div id="loading_msg">loading...</div>
		</center>	
		</div>
<img src="http://tracking.percentmobile.com/pixel/8ff4c106-3468-11de-a785-12313900c5b8" alt="." width="2" height="2" />
</body>
</html>
	''')

	def get_buses_before(self, route_id, stop_id):
		logging.debug("SELECT * FROM Bus WHERE route_id=%s and stop_id<%s order by stop_id desc" %
			(route_id, float(stop_id+".1")))
		buses = db.GqlQuery("SELECT * FROM Bus WHERE route_id=%s and stop_id<%s order by stop_id desc" %
			(route_id, float(stop_id+".1")))
		return buses

	def get_bus_info(self, bus):
		if (bus.stop_id!=None):
			stop=self.get_stop_name(bus.stop_id)
			return "Bus #%s is near %s" % (bus.number, bus.intersection)
		else:
		    return "Bus #%s is near %s" % (bus.number, bus.intersection)
    
	def get_stop_name(self, stop_id):
		stop =  db.GqlQuery("SELECT * FROM BusStop WHERE stop_id=%s"  % (stop_id)).get()
		return stop.name
	
class DisruptionsHandler(MobileHandler):
	def get(self):
		self.getHeader('DC Circulator')

		self.response.out.write("""
	<div id="header"> 
		<h1>Service Disruptions</h1> 
		<a href="/iphone" id="backButton">Back</a> 
	</div> 

		<p>No known service disruptions at this time.</p> 
		""")
		self.getFooter()
	

class MainHandler(MobileHandler):
	def get(self):
		self.getHeader('DC Circulator Mobile')

		self.response.out.write("""
	<div id="header">
		<h1>DC Circulator</h1>
	</div>
	
	<!--h1>Main index</h1-->

    <p> <a href="/iphone/whereismybus" onclick="go('/iphone/whereismybus');" class="green button">Where is my bus?</a> </p> 			
 
<ul> 
	<li class="arrow"><a href="/iphone/disruptions">Service disruptions</a></li> 
</ul>

<p><strong>We appreciate your feedback</strong> <br/> Please, send us your comments and compliments <a href="mailto:octolabs@dc.gov">here</a>.</p> 
		""")
		self.getFooter()

class LocationHandler(MobileHandler):
	nauticalMilePerLat = 60.00721
	nauticalMilePerLongitude = 60.10793
	rad = math.pi / 180.0
	milesPerNauticalMile = 1.15077945
	
	def distance(self, lat1, lon1, lat2, lon2):                      
	    """
	    Caclulate distance between two lat lons in NM
	    """
	    yDistance = (lat2 - lat1) * self.nauticalMilePerLat
	    xDistance = (math.cos(lat1 * self.rad) + math.cos(lat2 * self.rad)) * (lon2 - lon1) * (self.nauticalMilePerLongitude / 2)
	
	    distance = math.sqrt( yDistance**2 + xDistance**2 )
	
	    return distance * self.milesPerNauticalMile
	
	def get(self):
		color= str(self.request.get('color', ''))
		lat= float(self.request.get('lat', '38.87753218'))
		lon= float(self.request.get('lon', '-76.9949701'))
		
		self.getHeader('DC Circulator')

		self.response.out.write("""
	<div id="header"> 
		<h1>Pick your stop</h1> 
		<a href="/iphone/whereismybus" id="backButton">Back</a> 
	</div> 
		""")


		routes = db.GqlQuery("SELECT * FROM Route WHERE color='%s'" % color)
		
		for route in routes:
			self.response.out.write("<h1>%s</h1>" % route.name)
				
			stops = db.GqlQuery("SELECT * FROM BusStop WHERE route_id=%s" % route.route_id)

			closest_stop=None
			distance=100
			
			for stop in stops:
				dist=self.distance(lat, lon, stop.lat, stop.lon)
				if dist<distance:
					distance=dist
					closest_stop=stop
			
			self.response.out.write("""
		<ul>
			<li><a href="#" onclick="go('/iphone/whereismybus/stop?route_id=%s&stop_id=%s');">%s</a></li>
			
		</ul>
	
			""" % (route.route_id, closest_stop.stop_id, closest_stop.name))

		self.getFooter()
			

class WhereIsMyBusHandler(MobileHandler):
	def get(self):
		self.getHeader('Select Your Route')

		self.response.out.write("""
	<div id="header"> 
		<h1>Route</h1> 
		<a href="/iphone" id="backButton">Back</a> 
	</div> 
		""")


		self.response.out.write("""<ul>
			<li><a href="#" onclick="getLocation2('blue');">Union Station - Navy Yard Metro</a></li>
			<li><a href="#" onclick="getLocation2('green');">Woodley Park - Adams Morgan - McPherson Square Metro</a></li>
			<li><a href="#" onclick="getLocation2('red');">Convention Center - SW Waterfront</a></li>
			<li><a href="#" onclick="getLocation2('yellow');">Georgetown - Union Station</a></li>
			<li><a href="#" onclick="getLocation2('purple');">Smithsonian - National Gallery of Art Loop</a></li>

		</ul>""")

		self.getFooter()


class RouteHandler(MobileHandler):
	def get(self):
		route_id = self.request.get('route_id', '')
		route = db.GqlQuery("SELECT * FROM Route WHERE route_id=%s" % route_id)
		self.getHeader('Pick Your Stop - %s' % (route[0].name))

		self.response.out.write("""
	<div id="header"> 
		<h1>Stops</h1> 
		<a href="/iphone/whereismybus" id="backButton">Back</a> 
	</div> 
		""")


		self.response.out.write('<ul>')
	
		stops = db.GqlQuery("SELECT * FROM BusStop WHERE route_id=%s ORDER BY stop_id" % route_id) 
		#stops = db.GqlQuery("SELECT * FROM Stop WHERE route_id=%s" % route_id)
		i=0
		for stop in stops:
			i=i+1
			self.response.out.write('''<li><a href="#" onclick="go('/iphone/whereismybus/stop?route_id=%s&stop_id=%s');" >%s</a></li>''' % (route_id, stop.stop_id, stop.desc))

		self.response.out.write('</ul>')

		self.response.out.write('<p>')
		self.response.out.write('Timetable: %s' % (route[0].schedule))
		self.response.out.write('</p>')
		
		self.getFooter()


class StopHandler(MobileHandler):
	def get(self):
		route_id = self.request.get('route_id', '')
		route = db.GqlQuery("SELECT * FROM Route WHERE route_id=%s" % route_id).get()
		stop_id = self.request.get('stop_id', 1)
		stop = db.GqlQuery("SELECT * FROM BusStop WHERE stop_id=%s" % stop_id).get()
		self.getHeader('%s' % (stop.name))

		self.response.out.write('''
			<div id="header"> 
				<h1>Next buses</h1> 
				<a href="/iphone/whereismybus" id="backButton">Back</a> 
			</div> 
	    ''') 
		
		#get all buses on stops before this
		buses=self.get_buses_before(route_id, stop_id)
		if (buses.count()==0):
			self.response.out.write("<p>No buses on this route at this time</p>")
		for bus in buses:
			#self.response.out.write('bus %s at stop %s <br/>' % (bus.busnumber, bus.stopnum))
			
			self.response.out.write("<p>"+self.get_bus_info(bus))
			dist=geo.distance(bus.lat, bus.lon, stop.lat, stop.lon)
			self.response.out.write("<br/>%.1g mi. away</p>" % dist)

		self.response.out.write('<p>')
		self.response.out.write('Timetable: %s' % (route.schedule))
		self.response.out.write('</p>')
		
		self.getFooter()


def main():
	application = webapp.WSGIApplication(
		[('/iphone', MainHandler),
		('/iphone/whereismybus', WhereIsMyBusHandler),
		('/iphone/disruptions', DisruptionsHandler),
		('/iphone/whereismybus/location', LocationHandler),
		('/iphone/whereismybus/route', RouteHandler),
		('/iphone/whereismybus/stop', StopHandler)],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
