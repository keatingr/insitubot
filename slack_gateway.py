import os
import time
from slackclient import SlackClient
import process_engine as pe

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
SLACK_USER_MARK = "U3A8AN4VB"
SLACK_USER_JULIAN = "U3CFGALSC"
SLACK_USER_AMEH = "U3A7XB22U"
SLACK_USER_RAXESH = "U39EELHNC"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# initiate user mapping (ordinarily LDAP or local datastore or Twilio auth)
# Team inSituBot consists of purchasing agents, all authorized for the customer id arbitrarily chosen as 489299
users = {}
users[SLACK_USER_MARK] = {'id':0,'displayName': "Mark O", 'insituCustomerId':489299}
users[SLACK_USER_AMEH] = {'id':1,'displayName': "Ameh", 'insituCustomerId':489299}
users[SLACK_USER_RAXESH] = {'id':2,'displayName': "Raxesh", 'insituCustomerId':489299}
users[SLACK_USER_JULIAN] = {'id':3,'displayName': "Julian", 'insituCustomerId':489299}

pendingQuestion = ""

def handle_question_response(pendingQuestion):
    if pendingQuestion != "":
        response = "The last question I asked you was " + pendingQuestion
        slack_client.api_call("chat.postMessage", channel=channel,
            text=response, as_user=True)
    return ""

def handle_declaration_response(command,slack_user_id):
    retVal = "" #if no question is asked don't return a value to be buffered by the function call
    if nlp_understand(command) == "greetings":
        print "Entering greeting"
        #dynamic data in API makes it impossible to construct stable use cases for demo (recently ordered vs not)
        #demo use case will always be not recently placed any orders
        response = "Hello, " + users[slack_user_id]['displayName'] + " I see you have not ordered from us recently would you like to review your profile information?\n\n1. Yes\n2. No"
        retVal = response
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    elif nlp_understand(command) == "track open orders":
        print "Entering track open orders"
        response = "Now performing " + nlp_understand(command) + " for " + users[slack_user_id]['displayName'] + " ..."
        mySaidRecently = response
        slack_client.api_call("chat.postMessage", channel=channel,
            text=response, as_user=True)
        customer_id = users[slack_user_id]['insituCustomerId']
        shipment_locations = pe.get_shipment_locations(customer_id)
        pe.upload_open_orders(customer_id,shipment_locations)
    else:
        response = "I'm still learning and don't understand " + command
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    return retVal #if a question was asked pass to super for buffering

def handle_command(command, channel, slack_user_id, pendingQuestion):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    print "handle_command: " + command
    retVal = ""
    if pendingQuestion != "":
        retVal = handle_question_response(pendingQuestion)
    else:
        retVal = handle_declaration_response(command,slack_user_id)
    print pendingQuestion
    return retVal

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel'], \
                       output['user']
    return None, None, None

def nlp_understand(given_phrase):
    retVal = ""
    if (given_phrase == "track open orders"):
        retVal = "track open orders"
    elif (given_phrase == "too"):
        retVal = "track open orders"
    #elif all other phrases that could mean track open orders return 'track open orders'
    set_of_greetings = set(['hi', 'hello', 'hey', 'heya', 'whatup', 'greetings', 'hola'])
    if (given_phrase in set_of_greetings):
        retVal = "greetings"
    return retVal

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("inSituBot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel and user:
                pendingQuestion = handle_command(command, channel, user, pendingQuestion)
            # TODO add error handling
    else:
        print("Connection failed. Bad internet connection? Invalid Slack token or bot ID?")