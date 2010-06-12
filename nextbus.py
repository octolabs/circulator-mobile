URL="http://webservices.nextbus.com/service/publicXMLFeed?a=dc-circulator&command=routeConfig"
URL="http://webservices.nextbus.com/service/publicXMLFeed?a=dc-circulator"

NEXTBUSWEBSERVICE="http://webservices.nextbus.com/service/publicXMLFeed"

import urllib

"""
<body> <route tag="1" title="1 - California" shortTitle="1-Calif/> <route tag="3" title="3 - Jackson" shortTitle="3-Jacksn"/> <route tag="4" title="4 - Sutter" shortTitle="4-Sutter"/> <route tag="5" title="5 - Fulton" shortTitle="5-Fulton"/> <route tag="6" title="6 - Parnassus" shortTitle="6-Parnas"/> <route tag="7" title="7 - Haight" shortTitle="7-Haight"/> <route tag="14" title="14 - Mission" shortTitle="14-Missn"/> <route tag="21" title="21 - Hayes" shortTitle="21-Hayes"/>
</body>
"""
routeListURL="http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=dc-circulator"


routeList = urllib.urlopen(routeListURL).read()

print routeList
"""
<body> <route tag="N" routeCode="27" title="N - Judah" color="003399"
oppositeColor="ffffff"> <stop tag="KINGd4S0" title="King St and 4th St" shortTitle="King & 4th"
lat="37.776036" lon="-122.394355" stopId="1"/>

<stop tag="KINGd2S0" title="King St and 2nd St" shortTitle="King & 2nd" lat="37.7796152" lon="-122.3898067" stopId="2"/>
<stop tag="EMBRBRAN" title="Embarcadero and Brannan St" shortTitle="Embarcadero & Brannan" lat="37.7844455" lon="-122.3880081" stopId="3"/>
<stop tag="EMBRFOLS" title="Embarcadero and Folsom St" shortTitle="Embarcadero & Folsom" lat="37.7905742" lon="-122.3896326" stopId="4"/>
...
<direction tag="out" title="Outbound" useForUI="true"> <stop tag="KINGd4S0"/> <stop tag="KINGd2S0"/> <stop tag="EMBRBRAN"/>
<stop tag="EMBRFOLS"/>
<stop tag="CVCENTF"/> </direction> <direction tag="in" title="Inbound" useForUI="true">
<stop tag="CVCENTF"/> <stop tag="EMBRFOLS"/> <stop tag="EMBRBRAN"/> <stop tag="KINGd2S0"/> <stop tag="KINGd4S0"/>
</direction> <direction tag="in_short" title="Inbound Short Run" useForUI="false">
<stop tag="CVCENTF"/> <stop tag="EMBRFOLS"/> <stop tag="EMBRBRAN"/>
</direction> ...
<path> <point lat="37.7695171" lon="-122.4287571"/> <point lat="37.7695099" lon="-122.42887"/>
</path> <path>
<point lat="37.77551" lon="-122.39513"/> <point lat="37.77449" lon="-122.39642"/> <point lat="37.77413" lon="-122.39687"/> <point lat="37.77385" lon="-122.39721"/> <point lat="37.7737399" lon="-122.39734"/> <point lat="37.77366" lon="-122.39744"/> <point lat="37.77358" lon="-122.39754"/> <point lat="37.77346" lon="-122.39766"/> <point lat="37.77338" lon="-122.39772"/> <point lat="37.77329" lon="-122.39778"/> <point lat="37.77317" lon="-122.39784"/>
</path> <path>
<point lat="37.76025" lon="-122.50927"/> <point lat="37.76023" lon="-122.50928"/> <point lat="37.76017" lon="-122.50928"/> <point lat="37.7601299" lon="-122.50927"/> <point lat="37.76008" lon="-122.50924"/> <point lat="37.76006" lon="-122.50921"/> <point lat="37.7600399" lon="-122.50916"/> <point lat="37.76003" lon="-122.50912"/> <point lat="37.7600399" lon="-122.50906"/> <point lat="37.76005" lon="-122.50902"/> <point lat="37.76008" lon="-122.50898"/> <point lat="37.76017" lon="-122.50885"/>
</path> ...

</route> </body>
"""
routeConfigURL="http://webservices.nextbus.com/service/publicXMLFeed? command=routeConfig&a=<agency_tag>&r=<route tag>"

routesURL=URL+"&command=routeConfig"
routes = urllib.urlopen(routesURL).read()

#print routes


"""
<body> <agency tag="actransit" title="AC Transit, CA"
regionTitle="California-Northern"> <agency tag="alexandria" title="Alexandria DASH, VA"
shortTitle="DASH" regionTitle="Virginia"> <agency tag="amerimar" title="Amerimar" regionTitle="Pennsylvania"> <agency tag="blackhawk" title="Black Hawk Transportation Authority,
CO" shortTitle="Black Hawk" regionTitle="Colorado"> <agency tag="camarillo" title="Camarillo Area (CAT), CA"
shortTitle="Camarillo (CAT)" regionTitle="California-Southern"> <agency tag="case-western" title="Case Western University, OH"
shortTitle="Case Western" regionTitle="Ohio"> <agency tag="chapel-hill" title="Chapel Hill Transit, NC"
shortTitle="Chapel Hill" regionTitle="North Carolina"> ...
</body>
"""
agencyListURL="http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList"



"""
error handling:

<body> <Error shouldRetry="true">
Agency server cannot accept client while status is: agency name = sf-muni,status = UNINITIALIZED, client count = 0, last even t = 0 seconds ago Could not get route list for agency tag "sf-muni" Either the route tag is bad or the system is initializing.
</Error> </body>

"""