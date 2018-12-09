from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('A0M53Rv63zvjUudcGrM4S+wtyfh+hV+1zTcMN8+fNkM121lTU+VZEm6iQWvRubGgxOaybogIkPMrIwCV4duuMIS6LKLQZzgO1tphC30SGEamv0R76qaXfW4OxTsp9Ityqdgi9RlXcgTGfmNXMUTECwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('dbbf55b1f7baccc6014eaf66df1b2bc6')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 200))
    app.run(host='0.0.0.0', port=port)
