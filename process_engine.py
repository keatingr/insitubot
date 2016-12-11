import zipfile, gmplot, os
from data_api import get_entry, get_entry_order_status, get_invoices, get_order_status

#CONSTANTS=========
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
customer_id = 489299

#FUNCTIONS=========
def upload_open_orders(customer_id,shipment_locations):
	gmap = gmplot.GoogleMapPlotter(42.3344835,-71.2253933, 16).from_geocode("Boston")
	#TODO delete old zip and html files
	#TODO zoom to data point lon, lats to properly frame in single view (including customer location); draw customer location
	lats = []
	lons = []
	for shipment in shipment_locations:
		print shipment['lat'] + " " + shipment['lon']
		lats.append(float(shipment['lat']))
		lons.append(float(shipment['lon']))
	gmap.scatter(lats,lons,'#FF0000',size=250,marker=False)
	gmap.draw("customer_orders_map.html")
	zf = zipfile.ZipFile("customer_orders_map.zip", "w")
	zf.write("customer_orders_map.html")
	zf.close()
	os.system("curl -F file=@customer_orders_map.zip -F channels=#insitusales -F token="+SLACK_BOT_TOKEN+" https://slack.com/api/files.upload")
	#myZipFile = zipfile.ZipFile("customer_orders_map.zip", "w" )
	#myZipFile.write("customer_orders_map.zip","customer_orders_map.html", zipfile.ZIP_DEFLATED )
	#myZipFile.close()

#EXECUTION BODY========

#customer = get_entry("id",customer_id,"customer_list")
#print "Customer Info: " + customer + "\n\n"
#{"id":489299,"name":"OSCO (S.Pulaski Chicago)","address":"OSCO-DRUG 6351 S. PULASKI RD   ","address2":"","city":"CHICAGO","state":"IL","zipcode":"00000","contact":"","phone":"","latitude":"34.9121733","longitude":"-77.23188189999999"}

#invoices = get_entry('id',customer_id,'customer_invoices',str(customer_id))
invoices = get_invoices(customer_id)
#print invoices
#invoice_id = 4400822

shipment_locations = []
for index, invoice in enumerate(invoices):
	order_info = get_order_status(invoice['id'])
	#print status['latitud']
	#print str(index) + " " + status
	if order_info['status'] == "on route":
		obj = {'id':index,
		'lat':order_info['latitud'],
		'lon':order_info['longitud']}
		shipment_locations.append(obj)
#longitude -77.23188189999999
#latitude 34.9121733'''

#customer_id = get_customer()['id']
upload_open_orders(customer_id,shipment_locations)