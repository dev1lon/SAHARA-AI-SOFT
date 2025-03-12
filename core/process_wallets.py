import asyncio
import random

from modules import balance_shards, faucet, transaction, claim, mint_nerzo
from .semaphore import semaphore
from .client import Client
from utils.logger import get_logger
import settings


logger = get_logger()


async def process_wallets(count, private_key, proxy):
    async with semaphore:

        client_eth = Client(
            private_key=private_key,
            proxy=proxy,
            rpc='https://eth.llamarpc.com'
        )
        client_sah = Client(
            private_key=private_key,
            proxy=proxy,
            rpc='https://testnet.saharalabs.ai'
        )
        logger.info(f'Запуск [{count}] {client_eth.account.address} | {proxy}')

        if settings.balance_shards:
            await balance_shards.balance_shards(count, proxy, client_eth)
            sleep_time = random.randint(settings.sleep_actions[0], settings.sleep_actions[1])
            logger.debug(f'[{count}] сон между действиями - {sleep_time} секунд')
            await asyncio.sleep(sleep_time)

        if settings.Faucet:
            await faucet.faucet(count, proxy, client_eth)
            sleep_time = random.randint(settings.sleep_actions[0], settings.sleep_actions[1])
            logger.debug(f'[{count}] сон между действиями - {sleep_time} секунд')
            await asyncio.sleep(sleep_time)

        if settings.Transaction:
            await transaction.transaction(count, client_sah)
            sleep_time = random.randint(settings.sleep_actions[0], settings.sleep_actions[1])
            logger.debug(f'[{count}] сон между действиями - {sleep_time} секунд')
            await asyncio.sleep(sleep_time)

        if settings.Claim:
            await claim.claim(count, proxy, client_eth)

        if settings.mint_nerzo:
            await mint_nerzo.mint_nerzo(count,client_sah)
            sleep_time = random.randint(settings.sleep_actions[0], settings.sleep_actions[1])
            logger.debug(f'[{count}] сон между действиями - {sleep_time} секунд')
            await asyncio.sleep(sleep_time)

    sleep_time = random.randint(settings.sleep_wallets[0], settings.sleep_wallets[1])
    logger.debug(f'Сон между кошельками - {sleep_time} секунд')
    await asyncio.sleep(sleep_time)
