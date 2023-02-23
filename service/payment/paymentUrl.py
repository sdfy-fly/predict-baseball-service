import aiohttp

async def createPaymentUrl(userID:str, amount:float):

    url = "https://api.cryptocloud.plus/v1/invoice/create"
    headers = {
        "Authorization" : "Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTg0NiwiZXhwIjo4ODA3Njk4NjIxM30.Xa23tcxDqFetg8H6W7zi-xga79cbOZHwEtzWJ1TDr5c"
    }
    body = {
        "amount" : amount,
        "shop_id" : "gQ4diunlDczqeiFs", 
        "order_id" : userID.split(';')[0]
    }
    async with aiohttp.ClientSession() as session:
        response = await (await session.post(url, headers=headers, json=body, ssl=False)).json()

    return response["pay_url"]

