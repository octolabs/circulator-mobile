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

class Update (webapp.RequestHandler):
	def get(self):
		self.response.out.write('I <3 cron jobs!')

def main():
  application = webapp.WSGIApplication([('/tasks/update', Update)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()




