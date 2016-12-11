import os
import time
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
SLACK_USER_MARK = "U3A8AN4VB"
SLACK_USER_JULIAN = "U3CFGALSC"
SLACK_USER_AMEH = ""
SLACK_USER_RAXESH = ""

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel, user):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    #response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
    #           "* command with numbers, delimited by spaces."
    
    #if command.startswith(EXAMPLE_COMMAND):
    response = get_user_from_id(user) + " asked me to " + command
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def get_user_from_id(slack_user_id):
    """
    Map constants for Slack API usernames to a display name
    """
    userDisplayName = slack_user_id
    if slack_user_id == SLACK_USER_MARK:
        userDisplayName = "Mark O"
    elif slack_user_id == SLACK_USER_AMEH:
        userDisplayName = "Ameh"
    elif slack_user_id == SLACK_USER_RAXESH:
        userDisplayName = "Raxesh"
    elif slack_user_id == SLACK_USER_JULIAN:
        userDisplayName = "Julian"
    return userDisplayName

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