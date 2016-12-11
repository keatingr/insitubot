
from twilio import twiml
from flask import Flask, request
app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def hello():
	in_text = request.form["Body"]
	number = request.form["From"]
	return_text = get_response(in_text)
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

