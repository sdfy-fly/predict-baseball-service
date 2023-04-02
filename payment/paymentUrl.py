import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()

CRYPTO_CLOUD_TOKEN = os.getenv("CRYPTO_CLOUD_TOKEN")
CRYPTO_CLOUD_SHOP_ID = os.getenv("CRYPTO_CLOUD_SHOP_ID")


async def createPaymentUrl(order_id: str, amount: float):
    url = "https://api.cryptocloud.plus/v1/invoice/create"
    headers = {
        "Authorization": f"Token {CRYPTO_CLOUD_TOKEN}"
    }
    body = {
        "amount": amount,
        "shop_id": CRYPTO_CLOUD_SHOP_ID,
        "order_id": order_id,
        "currency": "USD"
    }

    async with aiohttp.ClientSession() as session:
        response = await (await session.post(url, headers=headers, json=body, ssl=False)).json()

    return response["pay_url"]
