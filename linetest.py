from flask import Flask, request, abort
import requests
import json

app = Flask(__name__)

@app.route('/api/http_trigger', methods=['POST'])
def webhook():
    if request.method == 'POST':
        payload = request.json
        reply_token = payload['events'][0]['replyToken']  # แก้ไขตรงนี้
        print(reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
        if 'ดี' in message:
            reply_message = 'ดีมาก'  # แก้ไขตรงนี้
            reply_message_to_line(reply_token, reply_message, 'EP5PD+uCt9+nheIpJbyHBEbUFEz1tIY4a0Ezwa2CfLnWMHb9lPq7JnHgnnhTBQvaj8BZVKBSfHNzP7V6UYId9e271cXwJt6q/bKtobThpmfP8a4gRFxTF7DEnwklPYCbFowBh7byxUi2su1G+24ZcQdB04t89/1O/w1cDnyilFU=')
            return request.json, 200
        else:
            abort(400)

def reply_message_to_line(reply_token, message, line_access_token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    authorization = 'Bearer {}'.format(line_access_token)
    print(authorization)
    headers = {
        'Content-Type' : 'application/json; charset=UTF-8',
        'Authorization': authorization
    }
    data = {
        "replyToken": reply_token,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data)
    if r.status_code == 200:
        return '', 200
    else:
        return '', r.status_code
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
