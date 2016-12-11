
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
	elif hello.counter == "order":
		hello.counter = hello.temp
		if "yes" in in_text.lower():
			return_text = "your order is being processed"
		elif "no" in in_text.lower():
			return_text = "oh..sorry for not able to understand you \
				   correctly, could you tell your order again please..!!"
		else:
			return_text = help_out()
	else:
		return_text = get_response(in_text)
	response = twiml.Response()
	hello.counter +=1
	response.message(return_text)
	return str(response)

def get_response(input_text):
	"""
	Takes in input text and get reply from bot
	"""
	words = input_text.split()
	input_text = input_text.lower()
	if "order" in input_text and "status" not in input_text:
		quantity = [int(s) for s in words if s.isdigit()]
		item_name = str(words[len(words)-1])
		output = "So you need "+str(quantity[0])+" "+item_name
		hello.temp = hello.counter
		hello.counter = "order"
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
	else:
		output = "Could you be more specific please.!!\n" + help_out()
	return output

def help_out():
	text = "You could type below messages:\
		   \n1) order 4 Margherita\
		   \n2) my orders status\
		   \n3) status of order no. 458373\
		   \n4} 'reset' or 'help'\
		   "
	return text

if __name__ == "__main__":
	hello.counter=0
	app.run(debug=True)

