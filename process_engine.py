from data_api import get_entry

customer_id = 2364433

customer = get_entry("id",order_id,"customer_list")
invoices = get_entry("id",)

#[{u'city': u'Bolingbrook', u'name': u'24 STOP (BOLINGBROOK)', u'address2': u'av regional', u'zipcode': u'60440', u'longitude': u'-76.649812', u'phone': u'', u'state': u'IL', u'contact': u'', u'address': u'24 STOP LIQUOR (BOLINGBROOK) 596 N.Pinecrest Rd.   ', u'latitude': u'5.695633', u'id': 2364433}]