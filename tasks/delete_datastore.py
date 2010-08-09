import cgi
import models
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import time
from datetime import datetime


class DeleteDatastore(webapp.RequestHandler):
  def get(self):

      modelType = self.request.get('modelType')
      if modelType:
        if modelType == 'Stop':
            q = db.GqlQuery("SELECT * FROM Stop")
        if modelType == 'Route':
            q = db.GqlQuery("SELECT * FROM Route")
        elif modelType == 'Trip':
            q = db.GqlQuery("SELECT * FROM Trip")
        elif modelType == 'Bus':
            q = db.GqlQuery("SELECT * FROM Bus")
        elif modelType == 'Timetable':
            q = db.GqlQuery("SELECT * FROM Timetable")
	
        results = q.fetch(999)
        db.delete(results)
        
        self.response.out.write("%s rows from %s deleted." % (len(results), modelType))
      
      else:
        self.response.out.write("Nothing deleted.")

application = webapp.WSGIApplication(
                                     [('/tasks/delete_datastore', DeleteDatastore)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()