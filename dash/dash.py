
import models
import wsgiref.handlers
import urllib2
from google.appengine.ext import db
from google.appengine.ext import webapp
import math

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
</p>
</body>
</html>''')


class MainHandler(MobileHandler):
    def get(self):
        self.getHeader('Circulator - Dashboard')
        buses = db.GqlQuery("SELECT * FROM Bus")
        on_route=0
        no_passengers=0
        garage=0
        gps_off=0
        count=0
        
        yellow=0
        blue=0
        green=0
        red=0
        purple=0
        
        for bus in buses:
            self.response.out.write("Bus: %s - %s<br/>" % (bus.number, bus.status))
            
            count=count+1
            if bus.status=="On Route":
                on_route=on_route+1
            if bus.status=="No Passengers":
                no_passengers=no_passengers+1
            if bus.status=="Garage":
                garage=garage+1
            if bus.status=="GPS Off":
                gps_off=gps_off+1
            """    
            if bus.color=="yellow": yellow=yellow+1
            if bus.color=="red": red=red+1
            if bus.color=="blue": blue=blue+1
            if bus.color=="green": green=green+1
            if bus.color=="purple": purple=purple+1
            """
            
        self.response.out.write("on_route: %s <br/>" % (on_route))
        self.response.out.write("no_passenger: %s <br/>" % (no_passengers))
        self.response.out.write("garage: %s <br/>" % (garage))
        self.response.out.write("gps_off: %s <br/>" % (gps_off))
        self.response.out.write("count: %s <br/>" % (count))
        
        self.response.out.write("""
        <img src=http://chart.apis.google.com/chart?cht=p3&chd=t:%s,%s,%s,%s&chs=350x100&chl=On_Route|No_Passengers|Garage|GPS_Off /><br/>
        """ % (str(math.floor(on_route*count/100)), str(math.floor(no_passengers*count/100)),str(math.floor(garage*count/100)), str(math.floor(gps_off*count/100))))

        """
        self.response.out.write("yellow: %s <br/>" % (yellow))
        self.response.out.write("red: %s <br/>" % (red))
        self.response.out.write("blue: %s <br/>" % (blue))
        self.response.out.write("green: %s <br/>" % (green))
        self.response.out.write("purple: %s <br/>" % (purple))
        """

        self.response.out.write("<table><tr>" )
        
        routes = models.Route.all()
        for route in routes:
            self.response.out.write("<td valign='top'> <b>%s</b> <br/>" % route.name)
            self.print_route(route)
            self.response.out.write("</td>")

        self.response.out.write("</tr></table>")


    def print_route(self, route):
        stops = models.BusStop.all().filter("route_id =", route.route_id).order("stop_id")
        
        self.response.out.write("<table width='200' cellpadding='0' cellspacing='0' border='0'>")
        for stop in stops:
            bus = models.Bus.all().filter("route_id =",route.route_id).filter("stop_id =",stop.stop_id).get()
            businfo=""
            if (not bus==None):
                businfo="#"+bus.number
                
            self.response.out.write('<tr><td>%s</td><td><img src="/static/images/stop.gif" border="0"/></td><td><font size="-2">%s</font></td></tr>' % (businfo,stop.name))
            self.response.out.write('<tr><td></td><td><img src="/static/images/line.gif" border="0"/></td><td></td></tr>')
        
        self.response.out.write("</table>")
        
        self.getFooter()


def main():
    application = webapp.WSGIApplication(
        [('/dash', MainHandler)],
        debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
