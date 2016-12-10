
from twilio import twiml
from flask import Flask, request
app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def hello():
	gettext = request.form["Body"]
	num = request.form["From"]
	response = twiml.Response()
	response.message(gettext + " from "+ num)
	return str(response)

if __name__ == "__main__":
    app.run(debug=True)
