import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

jokes = {
         'stupid': ["""Maiven is so stupid, he needs a recipe to make ice cubes.""",
                    """Maiven is so stupid, he thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Maiven is so fat, when he goes to a restaurant, instead of a menu, he gets an estimate.""",
                    """ Maiven is so fat, when the cops see his on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""Maiven is so dumb, when God was giving out brains, he thought they were milkshakes and asked for extra thick.""",
                    """Maiven is so dumb, he locked him keys inside him motorcycle."""] 
         }

# Create your views hime.
class MaivenBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '14051995':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for othim events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])          
        return HttpResponse()  

def post_facebook_message(fbid, recevied_message):
# Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    joke_text = ''
    for token in tokens:
        if token in jokes:
            joke_text = random.choice(jokes[token])
            break
    if not joke_text:
        joke_text = "I didn't understand! Send 'stupid', 'fat', 'dumb' for a Maiven joke!"

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'EAAYq3XrOGskBAKflCQyjP8gZCxlgEZCKQ9dSTJoBFUs8j80GmCjIc6ZBPaferTRJNrZA4XYeux3mXPOUAXFPA97Ec31Hev7JKAftYDWfe8Fhx14k7iwIlUp0RxZCGTBp2n2BYhNADuaHETnxgZB0tZCJ2JgJ4E9HakwN4pEw26XKQZDZD'}
    user_details = requests.get(user_details_url, user_details_params).json()
    joke_text = 'Yo '+user_details['first_name']+'..!' + joke_text   

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAYq3XrOGskBAKflCQyjP8gZCxlgEZCKQ9dSTJoBFUs8j80GmCjIc6ZBPaferTRJNrZA4XYeux3mXPOUAXFPA97Ec31Hev7JKAftYDWfe8Fhx14k7iwIlUp0RxZCGTBp2n2BYhNADuaHETnxgZB0tZCJ2JgJ4E9HakwN4pEw26XKQZDZD' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())              