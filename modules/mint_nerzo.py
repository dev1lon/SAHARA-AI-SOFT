from web3 import AsyncWeb3

from utils import abi
from utils.logger import get_logger


logger = get_logger()


async def mint_nerzo(count, client):
    nft_contract = client.w3.eth.contract(
        address=AsyncWeb3.to_checksum_address('0xC3622849B5E11A7c1D71276D6dc66Fb59eaAa038'),
        abi=abi.NerzoABI
    )

    args = [
        client.account.address,
        1,
        AsyncWeb3.to_checksum_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'),
        int(0.1 * 10 ** 18),
        [
            [],
            0,
            2**256 - 1,
            '0x0000000000000000000000000000000000000000'
        ],
        b''
    ]

    tx_hash = None
    try:
        tx_hash = await client.send_transaction(
            to=AsyncWeb3.to_checksum_address('0xC3622849B5E11A7c1D71276D6dc66Fb59eaAa038'),
            data=nft_contract.encodeABI('claim', args=args),
            value=int(0.1 * 10 ** 18),
            increase_gas_price=1.5
        )
    except Exception as error:
        logger.warning(f'[{count}] {client.account.address} | {error}')

    if tx_hash:
        try:
            await client.verif_tx(tx_hash=tx_hash)
            logger.success(f'[{count}] {client.account.address} | tx_hash - {tx_hash.hex()} | Success claim NFT')
        except Exception as err:
            logger.error(f'[{count}] {client.account.address} | Claim failed. Error - {err}')
