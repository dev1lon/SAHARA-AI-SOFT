import random

from utils.logger import get_logger


logger = get_logger()


async def transaction(count, client):

    amount = int(random.uniform(0.0001, 0.001) * 10 ** 18)

    tx_hash = None
    try:
        tx_hash = await client.send_transaction(
            to=client.random_account.address,
            value=amount,
            increase_gas_price=1.3
        )
    except Exception as error:
        logger.warning(f'[{count}] {client.account.address} | {error}')

    if tx_hash:
        try:
            await client.verif_tx(tx_hash=tx_hash)
            logger.success(f'[{count}] {client.account.address} | tx_hash - {tx_hash.hex()} | Сделал трансфер на рандомный кошелёк')
        except Exception as err:
            logger.error(f'[{count}] {client.account.address} | Транзакция зафейлилась. Ошибка - {err}')
