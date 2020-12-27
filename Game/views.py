from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import os
import sys
import dotenv
import pickle
from Game.models import Player

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage

from Game.fsm import GameMachine
GameMachine.models = ''

dotenv.load_dotenv()

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_access_token == None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
if channel_secret == None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

# Machine config options
states = ['reset', 'idle', 'usage', 'info', 'reply', 'judge']
transitions = [
    {
        'trigger': 'go_back',
        'source': ['reset', 'usage', 'info', 'reply'],
        'dest': 'idle'
    },
    {
        'trigger': 'goto_reset',
        'source': ['idle', 'judge'],
        'dest': 'reset'
    },
    {
        'trigger': 'advance',
        'source': 'idle',
        'dest': 'usage',
        'conditions': 'help'
    },
    {
        'trigger': 'advance',
        'source': 'idle',
        'dest': 'info',
        'conditions': 'get_info'
    },
    {
        'trigger': 'advance',
        'source': 'idle',
        'dest': 'reply',
        'conditions': 'query'
    },
    {
        'trigger': 'advance',
        'source': 'idle',
        'dest': 'judge',
        'conditions': 'answer'
    },
]
initial = 'idle'
auto_transitions = False
show_conditions = True

# Methods

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        print('Request body:', request.body)

        try:
            events = parser.parse(
                    request.body.decode('utf-8'),
                    request.headers['X-Line-Signature']
            )
        except InvalidSignatureError:
            return HttpResponseBadRequest()

        for event in events:
            if event.type != 'message':
                continue
            if event.message.type != 'text':
                continue
            if event.source.type != 'user':
                continue

            try:
                player = Player.objects.get(user_id = event.source.user_id)
                machine = pickle.loads(player.machine)
            except Player.DoesNotExist:
                machine = GameMachine(
                    states = states,
                    transitions = transitions,
                    initial = initial,
                    auto_transitions = auto_transitions,
                    show_conditions = show_conditions,
                )
                machine.goto_reset(event)

                player = Player.objects.create(user_id = event.source.user_id)

            machine.advance(event)
            player.machine = pickle.dumps(machine)
            player.save()

    return HttpResponse('OK')
