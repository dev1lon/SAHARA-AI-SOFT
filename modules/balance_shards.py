import aiohttp
import time

from aiohttp_proxy import ProxyConnector
from eth_account.messages import encode_defunct
from fake_useragent import UserAgent

from utils.logger import get_logger


logger = get_logger()


async def balance_shards(count, proxy, client):
    user_agent = UserAgent().random

    headers = {
        'user-agent': user_agent,
    }

    json_challenge = {
        'address': client.account.address,
        'timestamp': time.time(),
    }

    connector = ProxyConnector.from_url(f'http://{proxy}')

    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        async with session.post(url='https://legends.saharalabs.ai/api/v1/user/challenge', json=json_challenge) as response:
            challenge = await response.json()
            challenge_code = challenge['challenge']
            sign_text = f'Sign in to Sahara!\nChallenge:{challenge_code}'
            encoded_message = encode_defunct(text=sign_text)
            signed_message = client.w3.eth.account.sign_message(encoded_message, client.private_key)
            signature = signed_message.signature.hex()

            json_wallet = {
                'address': client.account.address,
                'sig': signature,
                'timestamp': time.time(),
            }
        async with session.post(url='https://legends.saharalabs.ai/api/v1/login/wallet', json=json_wallet) as response:
            data = await response.json()
            access_token = data['accessToken']
            headers_info = {
                'authorization': f'Bearer {access_token}'
            }
            json_info = {
                'timestamp': time.time()
            }

        async with session.post(url='https://legends.saharalabs.ai/api/v1/user/info', headers=headers_info, json=json_info) as response:
            data = await response.json()
            balance = data['shardAmount']
            logger.success(f'[{count}] {client.account.address} | {balance} shards')