import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')

WEBHOOK = f'https://api.telegram.org/bot{os.getenv('TG_TOKEN')}/sendMessage'

def send_webhook(text):
    requests.post(WEBHOOK, json={'chat_id': 1562985568, 'text': text})