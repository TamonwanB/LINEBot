from flask import Flask, request, abort
from linebot import WebhookHandler, LineBotApi
# from linebot import (
#     LineBotApi,
#     WebhookHandler
# )
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)
import mysql.connector

app = Flask(__name__)

# กำหนดค่า Channel Access Token และ Channel Secret ของคุณ
line_bot_api = LineBotApi('sOMqNyzdSnsU8qNJxndrMDS2zarT6IWqfd/nadp2NoDl2ukWrVRL1mjh/fSvOIOw7EwFatL4o4lljSfQLMuzDgbhz2NS/1t8mgyUAFL+/oyksxdQ9VXkFMfZwTptVlkf3VRfLZepJXKkSe3gyFDSawdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f513674a30f40a8994b4a4cf21804492')

# เชื่อมต่อกับ MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="031244",
    database="linebot"
)
# เส้นทางของ Webhook สำหรับการรับข้อมูลจาก LINE Messaging API
@app.route("/api/Linetest", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# การประมวลผลข้อความ
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    question = event.message.text
    # answer = get_answer(question)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="")
    )

# ฟังก์ชันสำหรับดึงคำตอบจากฐานข้อมูล
def get_answer(question):
    try:
        mycursor = mydb.cursor()
        query = "SELECT answer FROM questionanswer WHERE question = %s"
        mycursor.execute(query, (question,))
        result = mycursor.fetchone()
        mycursor.close()
        if result:
            return result[0]  # Assuming 'result[0]' contains the answer
        else:
            return "ขอโทษครับ ฉันไม่สามารถตอบคำถามนี้ได้"
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000', debug=True)

