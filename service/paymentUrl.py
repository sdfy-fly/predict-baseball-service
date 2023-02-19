import aiohttp

async def createPaymentUrl(amount:float , userID:str):

    url = "https://api.cryptocloud.plus/v1/invoice/create"
    headers = {
        "Authorization" : "Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mjc5OCwiZXhwIjo4ODA3NjcyNzM5OH0.1rc3zMRQiqUTAkk20qb46Ltg4NGskfs8vDrZFu2E928"
    }
    body = {
        "amount" : amount,
        "shop_id" : "LgkhngPhUPWxKEU5", 
        "order_id" : userID
    }
    async with aiohttp.ClientSession() as session:
        response = await (await session.post(url, headers=headers, json=body, ssl=False)).json()

    return response["pay_url"]

