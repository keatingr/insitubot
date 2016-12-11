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
users = {}
users[SLACK_USER_MARK] = {'id':0,'displayName': "Mark O", 'insituCustomerId':489299}
users[SLACK_USER_AMEH] = {'id':1,'displayName': "Ameh", 'insituCustomerId':489299}
users[SLACK_USER_RAXESH] = {'id':2,'displayName': "Raxesh", 'insituCustomerId':489299}
users[SLACK_USER_JULIAN] = {'id':3,'displayName': "Julian", 'insituCustomerId':489299}

def handle_command(command, channel, slack_user_id):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    if command == "track open orders":
        print "Entering track open orders"
        response = "Now performing " + command + " for " + users[slack_user_id]['displayName'] + " ..."
        customer_id = users[slack_user_id]['insituCustomerId']
        shipment_locations = pe.get_shipment_locations(customer_id)
        pe.upload_open_orders(customer_id,shipment_locations)
    else:
        response = "homey don't play that"

    slack_client.api_call("chat.postMessage", channel=channel,
                  text=response, as_user=True)

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

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("inSituBot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel and user:
                handle_command(command, channel, user)
            # TODO add error handling
    else:
        print("Connection failed. Bad internet connection? Invalid Slack token or bot ID?")