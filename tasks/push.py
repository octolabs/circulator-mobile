import cgi
import models
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import time
from datetime import datetime


class Push(webapp.RequestHandler):
  def get(self):

    q = models.Bus.all().filter("address =", cgi.escape(self.request.get('address')))

    result = q.get()
    
    route_id=cgi.escape(self.request.get('route_id'))
    if route_id=="None":
        route_id=None
    else:
        route_id=int(route_id)

    stop_id=cgi.escape(self.request.get('stop_id'))
    if stop_id=="None":
        stop_id=None
    else:
        stop_id=int(stop_id)

    if result==None:
      time_format="%Y-%m-%d %H:%M:%S"

      bus = models.GPS(number=cgi.escape(self.request.get('busnumber')),
        report=cgi.escape(self.request.get('report')),
        address=cgi.escape(self.request.get('address')),
        intersection=cgi.escape(self.request.get('intersection')),
        lat=float(cgi.escape(self.request.get('lat'))),
        lon=float(cgi.escape(self.request.get('lon'))),
        velocity=int(cgi.escape(self.request.get('velocity'))),
        direction=int(cgi.escape(self.request.get('direction'))),
        gps_date=datetime.strptime(cgi.escape(self.request.get('gps_date')),time_format),

        status=str(cgi.escape(self.request.get('status'))),
        #route_id=int(cgi.escape(self.request.get('route_id'))),
        #stop_id=int(cgi.escape(self.request.get('stop_id'))),
        
        )
      bus.put()

      self.response.out.write("OK add")

    else:
      time_format="%Y-%m-%d %H:%M:%S"

      result.number=cgi.escape(self.request.get('number'))
      result.report=cgi.escape(self.request.get('report'))
      result.address=cgi.escape(self.request.get('address'))
      result.intersection=cgi.escape(self.request.get('intersection'))
      result.lat=float(cgi.escape(self.request.get('lat')))
      result.lon=float(cgi.escape(self.request.get('lon')))
      result.velocity=int(cgi.escape(self.request.get('velocity')))
      result.direction=int(cgi.escape(self.request.get('direction')))
      result.gps_date=datetime.strptime(cgi.escape(self.request.get('gps_date')),time_format)

      result.status=str(cgi.escape(self.request.get('status')))
      result.route_color=cgi.escape(self.request.get('route_color'))
      result.route_id=route_id
      result.stop_id=stop_id
      result.put()
      self.response.out.write("OK update")

                 
application = webapp.WSGIApplication(
                                     [('/tasks/push', Push)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()