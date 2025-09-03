import logging
from time import time

from binance.spot import Spot
from pybit.unified_trading import HTTP

from backend.settings import ENV
from orders.models import TopUp


logger = logging.getLogger(__name__)

client = Spot(api_key=ENV.str('BINANCE_API_KEY'), api_secret=ENV.str('BINANCE_API_SECRET'))
session = HTTP(testnet=False, api_key=ENV.str('BYBIT_API_KEY'), api_secret=ENV.str('BYBIT_API_SECRET'),)


def get_binance_updates():
    timestamp = int((time()) * 1000)
    startTime = timestamp - 1000 * 60 * 60 * 24
    try:
        history = client.deposit_history(status=1, coin='USDT', startTime=startTime, timestamp=timestamp)
        logger.debug(f'Binance response {history}')
        return [(row['amount'], row['txId']) for row in history if row['status'] == 1]
    except Exception as e:
        logger.error(e)
        return []


def get_bybit_updates():
    startTime = int((time() - 60 * 60 * 24) * 1000)
    result = []
    try:
        cursor = None
        while True:
            response = session.get_deposit_records(coin='USDT', startTime=startTime, cursor=cursor)
            result.extend([(row['amount'], row['txID']) for row in response['result']['rows'] if row['status'] == 3])
            logger.debug(f'bybit response {response}')
            cursor = response['result']['nextPageCursor']
            if cursor is None or cursor == '':
                break
        logger.debug(f'{result=}')
    except Exception as e:
        logger.error(e)
    try:
        cursor = None
        while True:
            response = session.get_internal_deposit_records(coin='USDT', startTime=startTime, cursor=cursor)
            result.extend([(row['amount'], row['txID']) for row in response['result']['rows'] if row['status'] == 2])
            logger.debug(f'bybit response {response}')
            cursor = response['result']['nextPageCursor']
            if cursor is None or cursor == '':
                break
    except Exception as e:
        logger.error(e)
    logger.debug(f'{result=}')
    return result


async def check_wallets():
    result = [*get_binance_updates(), *get_bybit_updates()]
    for amount, txId in result:
        if await TopUp.objects.filter(tx_id=txId).aexists():
            logger.debug('This payment has been already proceed')
            continue
        topup = await TopUp.objects.filter(to_pay=amount, is_paid=False).afirst()
        if topup:
            logger.info(f'Found topup {topup}')
            topup.is_paid = True
            topup.tx_id = txId
            await topup.atop()
            await topup.asave(update_fields=('is_paid', 'tx_id'))
