import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library
use_library('django', '1.1')

import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
	def get(self):

		template_values = {'routes': 'routes',}
		path = os.path.join(os.path.dirname(__file__), 'challenge.html')
		self.response.out.write(template.render(path, template_values))		

def main():
	application = webapp.WSGIApplication(
		[('/challenge', MainHandler),
		],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
