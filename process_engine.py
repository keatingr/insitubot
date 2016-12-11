from data_api import get_entry

customer_id = 489299

customer = get_entry("id",customer_id,"customer_list")
print customer
#invoices = get_entry("id",)

#{"id":489299,"name":"OSCO (S.Pulaski Chicago)","address":"OSCO-DRUG 6351 S. PULASKI RD   ","address2":"","city":"CHICAGO","state":"IL","zipcode":"00000","contact":"","phone":"","latitude":"34.9121733","longitude":"-77.23188189999999"}

#longitude -77.23188189999999

#latitude 34.9121733