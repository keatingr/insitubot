
from twilio import twiml
import data_api as da
import pdb
from flask import Flask, request
app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def hello():
	pdb.set_trace()
	in_text = request.form["Body"]
	ph_number = request.form["From"]
	
	number = int(ph_number[-10:])
	entry = da.get_entry("phone",str(number), "customer_list")
	return_text = get_response("Hi " + entry['name'] + ", How can i help you..??")
	response = twiml.Response()
	response.message(return_text)
	return str(response)

def get_response(input_text):
	"""
	Takes in input text and get reply from bot
	"""
	return input_text

if __name__ == "__main__":
    app.run(debug=True)

