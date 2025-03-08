import asyncio
import os

from pathlib import Path

import settings
from utils import utils
from core.process_wallets import process_wallets


BASE_DIR = Path(__file__).resolve().parent
private_keys = utils.read_file(os.path.join(BASE_DIR, "data", "private_keys.txt"))
proxies = utils.read_file(os.path.join(BASE_DIR, "data", "proxies.txt"))


async def main():
    if len(private_keys) != len(proxies):
        raise Exception('Приватные ключи не соответствуют количеству прокси')
    elif len(private_keys)  == 0 or len(proxies) == 0:
        raise Exception('Нет прокси и приватников')

    start_index = settings.skip_wallets

    tasks = []
    for count, (private_key, proxy) in enumerate(zip(private_keys[start_index:], proxies[start_index:]), start=start_index + 1):
        tasks.append(process_wallets(count, private_key, proxy))

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
