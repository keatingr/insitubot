from data_api import get_entry, get_entry_order_status, get_invoices

customer_id = 489299

#customer = get_entry("id",customer_id,"customer_list")
#print "Customer Info: " + customer + "\n\n"
#{"id":489299,"name":"OSCO (S.Pulaski Chicago)","address":"OSCO-DRUG 6351 S. PULASKI RD   ","address2":"","city":"CHICAGO","state":"IL","zipcode":"00000","contact":"","phone":"","latitude":"34.9121733","longitude":"-77.23188189999999"}

#invoices = get_entry('id',customer_id,'customer_invoices',str(customer_id))
invoices = get_invoices(customer_id)
print invoices
#invoice_id = 4400822
'''
for invoice_id in invoices:
	print invoice_id
	print get_entry_order_status('status',invoice_id)

#longitude -77.23188189999999
#latitude 34.9121733'''