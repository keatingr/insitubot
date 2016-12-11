import zipfile, gmplot, os

#CONSTANTS
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

#THE STUFF
def upload_open_orders(customer_id):
	gmap = gmplot.GoogleMapPlotter(42.3344835,-71.2253933, 16).from_geocode("Boston")
	#TODO delete old zip and html files
	gmap.draw("customer_orders_map.html")
	zf = zipfile.ZipFile("customer_orders_map.zip", "w")
	zf.write("customer_orders_map.html")
	zf.close()
	os.system("curl -F file=@customer_orders_map.zip -F channels=#insitusales -F token="+SLACK_BOT_TOKEN+" https://slack.com/api/files.upload")
	#myZipFile = zipfile.ZipFile("customer_orders_map.zip", "w" )
	#myZipFile.write("customer_orders_map.zip","customer_orders_map.html", zipfile.ZIP_DEFLATED )
	#myZipFile.close()


#customer_id = get_customer()['id']
upload_open_orders(None)