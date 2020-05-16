# -*- coding: utf-8 -*-
import os
import sys
from argparse import ArgumentParser
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, QuickReplyButton, MessageAction, QuickReply)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
def GetCertInfo():
    channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
    if channel_secret is None:
        print('Specify LINE_CHANNEL_SECRET as environment variable.')
        sys.exit(1)
    if channel_access_token is None:
        print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
        sys.exit(1)
    return [channel_secret, channel_access_token]

channel_access_token,channel_secret = GetCertInfo()
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    choiceList_Text = ["選択肢①","選択肢②","選択肢③"]
    items = [
        QuickReplyButton(action=MessageAction(label=f"{text}", text=f"{text}_text"))
        for text in choiceList_Text
    ]
    msgs = TextSendMessage(
        text="↓選択肢を選んでね↓"
        ,quick_reply=QuickReply(items=items)
    )
    line_bot_api.reply_message(event.reply_token, messages=msgs)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)