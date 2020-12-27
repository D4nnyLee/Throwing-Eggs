from django.http import HttpResponse

import os
import sys
import dotenv

from linebot import LineBotApi, WebhookParser
from linebot.models import TextSendMessage

dotenv.load_dotenv()

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_access_token == None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)

def send_reply_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text = text))

    return HttpResponse('OK')

def send_push_message(user_id, text):
    line_bot_api.push_message(user_id, TextSendMessage(text = text))

    return HttpResponse('OK')
