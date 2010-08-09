This specification defines the following files:
agency.txt - Required. This file contains information about one or more transit agencies that provide the data in this feed.
stops.txt - Required. This file contains information about individual locations where vehicles pick up or drop off passengers.
routes.txt - Required. This file contains information about a transit organization's routes. A route is a group of trips that are displayed to riders as a single service.
trips.txt - Required. This file lists all trips and their routes. A trip is a sequence of two or more stops that occurs at specific time.
stop_times.txt - Required. This file lists the times that a vehicle arrives at and departs from individual stops for each trip.
calendar.txt - Required. This file defines dates for service IDs using a weekly schedule. Specify when service starts and ends, as well as days of the week where service is available.

calendar_dates.txt - Optional. This file lists exceptions for the service IDs defined in the calendar.txt file. If calendar_dates.txt includes ALL dates of service, this file may be specified instead of calendar.txt.
fare_attributes.txt - Optional. This file defines fare information for a transit organization's routes.
fare_rules.txt - Optional. This file defines the rules for applying fare information for a transit organization's routes.
shapes.txt - Optional. This file defines the rules for drawing lines on a map to represent a transit organization's routes.
frequencies.txt - Optional. This file defines the headway (time between trips) for routes with variable frequency of service.
