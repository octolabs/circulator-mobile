from google.appengine.ext import db

class Bus(db.Model):
    number = db.StringProperty(required=True)
    report = db.StringProperty()
    address = db.StringProperty(required=True)
    lat = db.FloatProperty()
    lon = db.FloatProperty()
    velocity = db.IntegerProperty()
    direction = db.IntegerProperty()
    gps_date = db.DateTimeProperty()
    status = db.StringProperty()
    intersection = db.StringProperty()
    route_id = db.IntegerProperty()
    route_color = db.StringProperty()
    stop_id= db.IntegerProperty()
    stop_proximity = db.StringProperty()
    next_stop_id= db.IntegerProperty()
    comment = db.StringProperty()

class Route(db.Model):
    route_id = db.IntegerProperty()
    name = db.StringProperty()
    desc = db.StringProperty()
    direction = db.StringProperty()
    schedule = db.StringProperty()
    color = db.StringProperty()
    complimentary_route_id = db.IntegerProperty()
    stops_count= db.IntegerProperty()

class BusStop(db.Model):
    stop_id = db.IntegerProperty()
    name = db.StringProperty()
    desc = db.StringProperty()
    lat = db.FloatProperty()
    lon = db.FloatProperty()
    route_id = db.IntegerProperty()
    number = db.IntegerProperty()

class Timetable(db.Model):
    route_id = db.IntegerProperty()
    day = db.StringProperty()
    begin = db.StringProperty()
    end = db.StringProperty()

class Data(db.Model):
    type = db.StringProperty()
    last_date = db.DateTimeProperty()

class Feedback(db.Model):
	busnumber = db.StringProperty()
	comments = db.StringProperty(multiline=True)
	timestamp = db.DateTimeProperty(auto_now_add=True)
    