
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
		return_text = "Hi " + entry['name'] + ", How can i help you..??"
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
	if "orders" in input_text:
		quantity = [int(s) for s in input_text.split() if s.isdigit()]
		item_name = str(words[len(words)-1])
		output = "So you need "+str(quantity[0])+" "+item_name
	else:
		output = "Could you be more specific please.!!"
	return output

if __name__ == "__main__":
	hello.counter=0
	app.run(debug=True)

