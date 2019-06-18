import logging
import os
import requests

import azure.functions as func

# Get token and channel id from Application Configuration.
BOT_TOKEN = os.environ['bot_token']
CHANNEL_ID = os.environ['channel_id']


def main(msg: func.QueueMessage) -> None:
    jsonDict = msg.get_json()  # Parse QueueMessage to Python object.
    module_name = jsonDict['title'].split('_')[0]  # Get module name.
    # Build a Markdown formate link that link to the product page.
    caption = '[' + jsonDict['title'] + ']' + '(' +\
        'https://www.freitag.ch/en/' + module_name +\
        '?productID=' + jsonDict['RowKey'] + ')'
    # Build up data that will be sent out.
    data = {
        'chat_id': CHANNEL_ID,
        'media': [
            getInputMediaPhoto(src, caption)
            for src in jsonDict['product_cover_photo']
        ]
    }

    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMediaGroup'
    # Post data as JSON to Telegram API.
    requests.post(url, json=data)

    logging.info('Python queue trigger function processed a queue item:')


# Return dict in InputMediaPhoto type.
def getInputMediaPhoto(photoSrc: str, caption: str):
    return {
        'type': 'photo',
        'media': photoSrc,
        'caption': caption,
        'parse_mode': 'Markdown'
    }
