from flask import Flask,request,abort
import requests
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        payload = request.json
        Reply_token = payload['events'][0]['replyToken']
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
        if 'ดี'in message:
            Reply_message = 'ดีมาก'
            ReplyMessage(Reply_token,Reply_message,'EP5PD+uCt9+nheIpJbyHBEbUFEz1tIY4a0Ezwa2CfLnWMHb9lPq7JnHgnnhTBQvaj8BZVKBSfHNzP7V6UYId9e271cXwJt6q/bKtobThpmfP8a4gRFxTF7DEnwklPYCbFowBh7byxUi2su1G+24ZcQdB04t89/1O/w1cDnyilFU=')
            return request.json, 200
        else:
            abort(400)
def ReplyMessage(Reply_token, TextMessage,Line_Access_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Access_Token)
    print(Authorization)
    headers = {
        'Content-Type' : 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    data = {
        "replyToken":Reply_token,
        "message":[{
            "type":"text",
            "text":TextMessage
        }]
    }
    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200

if __name__ == '__main__':
    app.run(debug=True)