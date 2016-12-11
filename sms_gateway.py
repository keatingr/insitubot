
from twilio import twiml
import nltk
import data_api as da
from flask import Flask, request
app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def hello():
	in_text = request.form["Body"]
	ph_number = request.form["From"]
	if hello.counter == 0:
		number = int(ph_number[-10:])
		entry = da.get_entry("phone",str(number), "customer_list")
		return_text = "Hi " + entry['name'] + ", How can i help you..??\
					   \nYou could type:\
					   \n1) order 4 Margherita\
					   \n2) my orders status\
					   \n3) status of order no. 458373\
					   \n4} 'reset' or 'help'\
					   "
		hello.id = entry['id']
	elif hello.counter == "order":
		hello.counter = hello.temp
		if "yes" in in_text.lower():
			return_text = "your order is being processed"
		elif "no" in in_text.lower():
			return_text = "oh..sorry for not able to understand you \
				   correctly, could you tell your order again please..!!"
		else:
			return_text = help_out()
	elif hello.counter == "exit":
		hello.counter = hello.temp
		if "yes" in in_text.lower():
			return_text = "Have a good day..!!"
		elif "no" in in_text.lower():
			return_text = help_out()
		else:
			return_text = help_out()
	else:
		return_text = get_response(in_text)
	response = twiml.Response()
	if type(hello.counter) is not str:
		hello.counter +=1
	response.message(return_text)
	return str(response)

def get_response(input_text):
	"""
	Takes in input text and get reply from bot
	"""
	words = input_text.split()
	input_text = input_text.lower()
	if "order" in input_text and "status" not in input_text and "my" not in input_text:
		quantity = [int(s) for s in words if s.isdigit()]
		item_name = str(words[len(words)-1])
		if len(quantity)>0:
			output = "So you need "+str(quantity[0])+" "+item_name
			hello.temp = hello.counter
			hello.counter = "order"
		else:
			output = "please specify order quantity too..!!"
	elif "status" in input_text and "order" in input_text:
		order_no = [int(s) for s in words if s.isdigit()]
		if len(order_no)>0:
			details = da.get_order_status(order_no[0])["status"]
			if details:
				output = "Order no. "+str(order_no[0])+" "+details
			else:
				output = "No order details are available for "+str(order_no[0])
		else:
			output = "Could you please specify the order number"
	elif "thanks" in input_text:
		output = "You are welcome..!!"
	elif "my" in input_text and "old" in input_text and "order" in input_text:
		customer_id = [int(s) for s in words if s.isdigit()]
		if len(customer_id)>0:
			invoices = da.get_invoices(customer_id[0])
			order_all = da.get_all_orders(invoices)
			order_all = [str(s) for s in order_all]
			orders = ", ".join(order_all)
			output = "Your old orders were "+orders
		else:
			invoices = da.get_invoices(hello.id)
			order_all = da.get_all_orders(invoices)
			orders = ", ".join(order_all)
			if len(order_all)>0:
				output = "Your old orders were "+orders
			else:
				output = "There were no orders under your name."
	elif "pic" in input_text or "img" in input_text or "photo" in input_text:
		output = "Your pics are sent to your email."
	elif "okay" in input_text or "exit" in input_text:
		output = "Great. Would you like to know anything else.?"
		hello.temp = hello.counter
		hello.counter = "exit"
	else:
		output = "Could you be more specific please.!!\n" + help_out()
	return output

def help_out():
	text = "You could type below messages:\
		   \n1) order 4 Margherita\
		   \n2) my orders status\
		   \n3) status of order no. 458373\
		   \n4) my old orders\
		   \n5) old orders of id no 2938585\
		   \n6} 'reset' or 'help'\
		   \n7) exit\
		   "
	return text

if __name__ == "__main__":
	hello.counter=0
	app.run(debug=True)

