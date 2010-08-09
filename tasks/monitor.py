import cgi
import models
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import time
from datetime import datetime
from google.appengine.api import mail

class Monitor(webapp.RequestHandler):
  def get(self):
	time_format="%Y-%m-%d %H:%M:%S"
	gps_date = db.GqlQuery('SELECT * FROM Bus ORDER BY gps_date DESC LIMIT 1').get().gps_date		
	howOld = datetime.utcnow()-gps_date-timedelta(hours=4)
	if (howOld > timedelta(minutes=5)):
		print "Stale data %s" % howOld
		message = mail.EmailMessage(sender="octolabs@dc.gov",
		                            subject="Circulator Bus Data is Stale")
		message.to = "OCTO Labs <octolabs@dc.gov>"
		message.body = """
		Dear OCTO Labs:

		The Circulator Bus Data is %s minutes old. This is a test.

		""" % howOld
		message.send()


application = webapp.WSGIApplication(
                                     [('/tasks/monitor', Monitor)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()