import datetime
import logging
import requests as req
import json

import azure.functions as func

model = '7413'  # F705 SECRID X FREITAG


def main(mytimer: func.TimerRequest,
         freitagQueue: func.Out[func.QueueMessage]) -> None:
    url = 'https://www.freitag.ch/en/json/model/' + model + '/products/0/0'
    res = req.get(url).json()

    # Set Items' json as list and set the list to Queue.
    freitagQueue.set([getItemJson(product) for product in res['products']])

    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)


def getItemJson(product):
    product = product['product']
    item = {
        'PartitionKey': model,
        'RowKey': product['product_id'],
        'title': product['title'],
        'product_cover_photo': [
            x['src'] for x in product['neo_product_360_photo_outside']]
    }
    return json.dumps(item)
