import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
SORARE_CLIENT_ID = os.getenv("SORARE_CLIENT_ID")
SORARE_CLIENT_SECRET = os.getenv("SORARE_CLIENT_SECRET")


class AuthWithSorare:

    async def _getAccessToken(self, code):
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }

        params = {
            "client_id": SORARE_CLIENT_ID,
            "client_secret": SORARE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "https://sorareup.com/api/auth"
        }

        async with aiohttp.ClientSession() as session:
            response = (
                await (
                    await session.post(f'https://api.sorare.com/oauth/token', headers=headers, params=params,
                                       ssl=False)).json())
        return response['access_token']

    async def _getUserID(self, access_token):
        """
            Принимаю access token
            Возвращаю: userId, nickname
        """

        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        data = {
            "operationName": "currentUser",
            "query": "query currentUser { currentUser { slug , id} }"
        }

        async with aiohttp.ClientSession() as session:
            response = (await (
                await session.post('https://api.sorare.com/graphql', headers=headers, json=data, ssl=False)).json())[
                'data']

        userID = response['currentUser']['id'][5:]
        nickname = response['currentUser']['slug']

        return {'userID': userID, 'nickname': nickname}

    async def _getInfo(self, JWT):
        """
            Принимаю: JWT токен(access token),
            Возвращаю словарь :  algoliaApiKey, algoliaAppicationID
        """

        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {JWT}'

        }

        data = {
            "operationName": "ConfigQuery",
            "variables": {},
            "extensions": {
                "operationId": "React/79f363dbf0a16f25b7c4c916862fd82df2749c720ab0d54464f4d5a2f46488d0"
            }
        }
        async with aiohttp.ClientSession() as session:
            response = (await (
                await session.post('https://api.sorare.com/graphql', headers=headers, json=data, ssl=False)).json())[
                'data']

        algoliaApiKey = response['config']["algoliaSearchApiKey"]
        algoliaApplicationId = response['config']["algoliaApplicationId"]

        return {'x-algolia-application-id': algoliaApplicationId, 'x-algolia-api-key': algoliaApiKey}

    async def getUserInfo(self, code):

        access_token = await self._getAccessToken(code)
        userInfo = await self._getInfo(access_token)
        user_ID_nickname = await self._getUserID(access_token)

        if user_ID_nickname['nickname'].count('-') > 0:
            userInfo['nickname'] = ''.join(user_ID_nickname['nickname'].split('-')[0])
        else:
            userInfo['nickname']: str = user_ID_nickname['nickname']

        userInfo['userID']: str = user_ID_nickname['userID']
        userInfo['accessToken'] = access_token

        return userInfo
