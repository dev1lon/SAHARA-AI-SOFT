import aiohttp

from aiohttp_proxy import ProxyConnector
from fake_useragent import UserAgent

from core import captcha
from utils.logger import get_logger


logger = get_logger()


async def faucet(count, proxy, client):
    idx = 1
    user_agent = UserAgent().random

    balance  = await client.w3.eth.get_balance(client.account.address)
    if balance < 0.01 * 10 ** 18:
        logger.error(f'[{count}] Нет 0.01 ETH в эфире | {client.account.address}')
        return

    headers_test = {
        'user-agent': user_agent,
    }
    json_test = {
        'jsonrpc': '2.0',
        'id': idx,
        'method': 'eth_getBalance',
        'params': [
            client.account.address,
            'latest',
        ],
    }

    connector = ProxyConnector.from_url(f'http://{proxy}')

    idx += 1

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.post(url='https://testnet.saharalabs.ai/', headers=headers_test, json=json_test) as response:
            if response.status == 200:
                await captcha.captcha(proxy=proxy, session=session, user_agent=user_agent)
                headers_claim = {
                    'cf-turnstile-response': await captcha.captcha(proxy=proxy, session=session, user_agent=user_agent),
                    'user-agent': user_agent,
                }
                json_claim = {
                    'address': client.account.address,
                }
            else:
                logger.error(f'{client.account.address} | Проблема с подключением кошелька')
                return
        async with session.post(url='https://faucet-api.saharaa.info/api/claim2', headers=headers_claim, json=json_claim) as response:
            if response.status == 200:
                logger.success(f'[{count}] {client.account.address} | Success Faucet')
            elif response.status == 429:
                error = await response.json()
                logger.warning(f'[{count}] {client.account.address} | {error["msg"]}')
