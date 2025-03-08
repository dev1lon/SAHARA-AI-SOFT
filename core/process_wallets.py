import asyncio
import random

from modules import faucet, transaction, claim
from .semaphore import semaphore
from .client import Client
from utils.logger import get_logger
import settings


logger = get_logger()


async def process_wallets(count, private_key, proxy):
    async with semaphore:

        client = Client(
            private_key=private_key,
            proxy=proxy,
            rpc='https://eth.llamarpc.com'
        )
        logger.info(f'Запуск [{count}] {client.account.address} | {proxy}')

        if settings.Faucet:
            await faucet.faucet(count, proxy, client)
            sleep_time = random.randint(settings.sleep_actions[0], settings.sleep_actions[1])
            logger.debug(f'[{count}] сон между действиями - {sleep_time} секунд')
            await asyncio.sleep(sleep_time)

        if settings.Transaction:
            await transaction.transaction(count, private_key, proxy)
            sleep_time = random.randint(settings.sleep_actions[0], settings.sleep_actions[1])
            logger.debug(f'[{count}] сон между действиями - {sleep_time} секунд')
            await asyncio.sleep(sleep_time)

        if settings.Claim:
            await claim.claim(count, private_key, proxy, client)

    sleep_time = random.randint(settings.sleep_wallets[0], settings.sleep_wallets[1])
    logger.debug(f'Сон между кошельками - {sleep_time} секунд')
    await asyncio.sleep(sleep_time)
