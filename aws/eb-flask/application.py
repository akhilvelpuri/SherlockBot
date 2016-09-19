import os
from datetime import datetime
from random import randint
from flask import Flask, request, Response
from slackclient import SlackClient
from twilio import twiml
from twilio.rest import TwilioRestClient

'''The following arrays below are for random profile generation'''
fictional_charecters = ['Yoda', 'Naruto', 'Rafi', 'Joffrey', 'Jon Snow', 'Apple', 'Terminator', 'Neo', 'Durant', 'Barbie']
adjectives = ['Adorable', 'Affectionate', 'Acrobatic', 'Basic', 'Deadly', 'Droopy', 'Chubby', 'Curvy', 'Quirky', 'Responsible']
emoji = ['see_no_evil','hear_no_evil','speak_no_evil','sweat_drops','zap','monkey_face','dog','poodle','wolf','cat','lion_face','tiger2','tiger','leopard',
'horse','racehorse','unicorn_face','cow','cow2','ox','water_buffalo','pig','boar','pig_nose','ram','sheep','goat','dromedary_camel','camel','elephant',
'mouse','rat','hamster','rabbit2','rabbit','chipmunk','bear','koala','panda_face','paw_prints','turkey','chicken','rooster','hatching_chick','baby_chick',
'hatched_chick','bird','penguin','dove_of_peace','frog','crocodile','turtle','snake','dragon','whale2','whale','dolphin','fish',
'tropical_fish','blowfish','octopus','shell','crab','snail','bug','ant','honeybee','beetle','spider','spider_web','scorpion','bouquet',
'cherry_blossom','white_flower','rosette','rose','hibiscus','sunflower','blossom','tulip','seedling','evergreen_tree','deciduous_tree','palm_tree',
'cactus','ear_of_rice','herb','shamrock','four_leaf_clover','maple_leaf','fallen_leaf','leaves','earth_americas','earth_asia','earth_africa','dragon_face']
user_profiles = {}

TWILIO_PHONE_NUM = os.environ.get('TWILIO_PHONE_NUM', None)
USER_PHONE_NUM = os.environ.get('USER_PHONE_NUM', None)
slack_client_init = SlackClient(os.environ.get('SLACK_TEST_TOKEN', None))
twilio_client_init = TwilioRestClient(os.environ.get('TWILIO_ACCOUNT_SID', None), 
	os.environ.get('TWILIO_AUTH_TOKEN', None))

application = Flask(__name__)

@application.route('/report', methods=['POST'])
def to_report():
	if(datetime.now().time().hour == 17):
		user_profiles.clear()
	resp = twiml.Response()
	msg = request.form['Body']
	if "/rm" in msg:
		text = msg.replace("/rm","", 1)
		response_message = "\n\n911: \n\nRequest for immediate help!!!\n\nLocation:" + text
		twilio_client_init.messages.create(to=USER_PHONE_NUM, from_=TWILIO_PHONE_NUM, body=response_message)

	if(request.form['From'] not in user_profiles):
		user_profiles[request.form['From']] = [adjectives[randint(0,9)]+' '+fictional_charecters[randint(0,9)], ':'+emoji[randint(0,99)]+':']
	
	user_val = user_profiles[request.form['From']]
	slack_client_init.api_call("chat.postMessage", channel="#controlcenter", 
			text=msg, username=user_val[0], icon_emoji=user_val[1])
	return Response(resp.toxml(), mimetype="text/xml"), 'to_slack'

# run the application.
if __name__ == "__main__":
    # remove debug before deploying a production application.
    application.debug = True
    application.run()