import aiohttp
import bcrypt

"""
    Обернуть функции в блок Try и подумать над кодами возврата, чтобы на фронтеде отображалась ошибка
"""


async def getJWT(email, password):

    """
        Принимаю: логин и пароль
        Возвращаю: JWT token
    """

    try:
        async with aiohttp.ClientSession() as session:
            salt = (await (await session.get(f'https://api.sorare.com/api/v1/users/{email}')).json()).get('salt')
            passwordHash = bcrypt.hashpw(
                bytes(password, 'utf-8'), bytes(salt, 'utf-8'))
            responce = await session.post('https://api.sorare.com/graphql',
                headers={
                        'content-type': 'application/json', },
                json={
                    "operationName": "SignInMutation",
                    "variables": {"input": {"email": email, "password": passwordHash.decode()}},
                    "query": "mutation SignInMutation($input: signInInput!) { signIn(input: $input) { currentUser { slug jwtToken(aud: \"<YourAud>\") { token expiredAt } } errors { message } } }",
                    "data": {"signIn": {"currentUser": {"slug": "<YourSlug>", "jwtToken": {"token": "<YourJWTToken>", "expiredAt": "..."}}, "errors": []}}})
            JWTtoken = (await responce.json()).get('data').get('signIn').get('currentUser').get('jwtToken').get('token')
            return JWTtoken
    except:
        return 'Неправильный логин или пароль'


async def getInfo(JWT):

    """
        Принимаю: JWT токен,
        Возвращаю словарь : JWT, userID , nickname , algoliaApiKey, algoliaAppicationID
    """

    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {JWT}',
        'JWT-AUD': '<YourAud>'
    }

    data = {
        "operationName": "ConfigQuery",
        "variables": {},
        "extensions": {
            "operationId": "React/79f363dbf0a16f25b7c4c916862fd82df2749c720ab0d54464f4d5a2f46488d0"
        }
    }
    async with aiohttp.ClientSession() as session:
        responce = (await (await session.post('https://api.sorare.com/graphql', headers=headers, json=data)).json())['data']

    userId = responce['currentUser']['id'][5:]
    nickname = responce['currentUser']['nickname']

    algoliaApiKey = responce['config']["algoliaSearchApiKey"]
    algoliaApplicationId = responce['config']["algoliaApplicationId"]

    return {'JWT': JWT, 'userID': userId, 'nickname': nickname, 'x-algolia-application-id': algoliaApplicationId, 'x-algolia-api-key': algoliaApiKey}


class MBACards:

    async def getCardsId(self,algoliaApiKey, algoliaApplicationId, userID):

        """
            Принимаю: x-algolia-api-key, x-algolia-application-id , userID
            Возвращаю: массив из ID всех карточек
        """

        url = 'https://7z0z8pasdy-dsn.algolia.net/1/indexes/*/queries'
        
        headers = {
            'x-algolia-api-key': algoliaApiKey,
            'x-algolia-application-id': algoliaApplicationId
        }
        body = {"requests":[{"indexName":"Card","params":f"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&hitsPerPage=40&analyticsTags=%5B%22Gallery%22%5D&filters=sport%3Abaseball&distinct=true&attributesToRetrieve=%5B%22asset_id%22%5D&attributesToHighlight=none&maxValuesPerFacet=30&page=0&facets=%5B%22user.id%22%2C%22rarity%22%2C%22on_sale%22%2C%22position%22%2C%22grade%22%2C%22serial_number%22%2C%22team.long_name%22%2C%22player.display_name%22%2C%22player.birth_date_i%22%5D&tagFilters=&facetFilters=%5B%22user.id%3A{userID}%22%5D"}]}

        async with aiohttp.ClientSession() as session:
            responce = await (await session.post(url, headers=headers, json=body)).json()

        cardsID = []

        """
            проверка кода 200 , проверить если ли id, если нет то не вызывать getUserCards(cardsID)
        """

        for page in responce['results']:
            for id in page['hits']:
                cardsID.append(id['objectID'][16:])

        return cardsID

    async def getUserCards(self,cardsID):
        """
            Принимаю массив из id карточек, возвращаю объект со всей инфой по карточкам
        """

        body = {
            "operationName": "CardsByIdsQuery",
            "variables": {
                "input": {
                    "assetIds": [],
                    "ids": cardsID
                }
            },
            "query": "query CardsByIdsQuery($input: BaseballCardsInput!) {\n  cards(input: $input) {\n    assetId\n    ...MobileCardDetailsByAssetId_card\n    ...CommonCardPreview_BaseballCard\n    ...Card_CardInterface\n    __typename\n  }\n}\n\nfragment Card_CardInterface on CardInterface {\n  id\n  slug\n  fullImageUrl\n  player {\n    slug\n    displayName\n    __typename\n  }\n  __typename\n}\n\nfragment CommonCardPreview_BaseballCard on BaseballCard {\n  id\n  ...CardProperties_BaseballCard\n  ...CommonCardPreview_CardInterface\n  __typename\n}\n\nfragment CardProperties_BaseballCard on BaseballCard {\n  id\n  assetId\n  totalBonus\n  player {\n    currentSeasonAverageScore {\n      pitching\n      batting\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CommonCardPreview_CardInterface on CardInterface {\n  id\n  ...ClickableCard_CardInterface\n  ...CardDescription_CardInterface\n  __typename\n}\n\nfragment ClickableCard_CardInterface on CardInterface {\n  ...Card_CardInterface\n  __typename\n}\n\nfragment CardDescription_CardInterface on CardInterface {\n  id\n  assetId\n  season\n  rarity\n  player {\n    slug\n    displayName\n    __typename\n  }\n  __typename\n}\n\nfragment MobileCardDetailsByAssetId_card on BaseballCard {\n  id\n  positions\n  __typename\n}\n"
        }

        async with aiohttp.ClientSession() as session:
            cards = await session.post('https://api.sorare.com/sports/graphql', headers={'content-type': 'application/json'}, json=body)
            cards = (await cards.json())['data']

        return cards

    async def getCards(self,x_algolia_api_key, x_algolia_application_id, userID):
        cardsID = await self.getCardsId(x_algolia_api_key, x_algolia_application_id, userID)
        cards = await self.getUserCards(cardsID)
        return {'cards': cards}

class NBACards:

    async def getCardsId(self,algoliaApiKey, algoliaApplicationId, userID):

        """
            Принимаю: x-algolia-api-key, x-algolia-application-id , userID
            Возвращаю: массив из ID всех карточек
        """

        url = 'https://7z0z8pasdy-dsn.algolia.net/1/indexes/*/queries'
        
        headers = {
            'x-algolia-api-key': algoliaApiKey,
            'x-algolia-application-id': algoliaApplicationId
        }
        body = {"requests":[{"indexName":"Card","params":f"analyticsTags=%5B%22Gallery%22%5D&attributesToHighlight=%5B%5D&distinct=false&facets=%5B%22rarity%22%2C%22nba_stats.ten_game_average%22%2C%22grade%22%2C%22serial_number%22%2C%22team.long_name%22%2C%22player.display_name%22%2C%22player.birth_date_i%22%5D&filters=user.id%3A{userID}%20AND%20sport%3Anba&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=40&maxValuesPerFacet=10&page=0&query=&tagFilters="}]}

        async with aiohttp.ClientSession() as session:
            responce = await (await session.post(url, headers=headers, json=body)).json()

        cardsID = []

        """
            проверка кода 200 , проверить если ли id, если нет то не вызывать getUserCards(cardsID)
        """

        for page in responce['results']:
            for id in page['hits']:
                cardsID.append(id['objectID'][16:])

        return cardsID

    async def getUserCards(self,cardsID):
        """
            Принимаю массив из id карточек, возвращаю объект со всей инфой по карточкам
        """

        body = {
            "operationName": "NBACardsByIdsQuery",
            "variables": {
                "input": {
                    "assetIds": [],
                    "ids": cardsID
                }
            },
            "query": "query NBACardsByIdsQuery($input: NBACardsInput!) {\n  nbaCards(input: $input) {\n    assetId\n    ...NBAMobileCardDetailsByAssetId_card\n    ...NBACommonCardPreview_NBACard\n    __typename\n  }\n}\n\nfragment NBACommonCardPreview_NBACard on NBACard {\n  id\n  ...NBACardProperties_NBACard\n  ...CommonCardPreview_CardInterface\n  __typename\n}\n\nfragment NBACardProperties_NBACard on NBACard {\n  id\n  assetId\n  totalBonus\n  seasonBonus\n  rarityBonus\n  xpBonus\n  bonusLossAfterTransfer\n  player {\n    tenGameAverage\n    ...IneligibleIndicator_NBAPlayer\n    __typename\n  }\n  __typename\n}\n\nfragment IneligibleIndicator_NBAPlayer on NBAPlayer {\n  slug\n  isActive\n  __typename\n}\n\nfragment CommonCardPreview_CardInterface on CardInterface {\n  id\n  ...ClickableCard_CardInterface\n  ...CardDescription_CardInterface\n  __typename\n}\n\nfragment ClickableCard_CardInterface on CardInterface {\n  ...Card_CardInterface\n  __typename\n}\n\nfragment Card_CardInterface on CardInterface {\n  id\n  slug\n  player {\n    slug\n    displayName\n    __typename\n  }\n  ...Card_CardParam\n  __typename\n}\n\nfragment Card_CardParam on CardInterface {\n  fullImageUrl\n  player {\n    displayName\n    __typename\n  }\n  __typename\n}\n\nfragment CardDescription_CardInterface on CardInterface {\n  id\n  assetId\n  season\n  rarity\n  player {\n    slug\n    displayName\n    __typename\n  }\n  __typename\n}\n\nfragment NBAMobileCardDetailsByAssetId_card on NBACard {\n  id\n  slug\n  positions\n  __typename\n}\n"
        }

        async with aiohttp.ClientSession() as session:
            cards = await session.post('https://api.sorare.com/sports/graphql', headers={'content-type': 'application/json'}, json=body)
            cards = (await cards.json())['data']

        return cards

    async def getCards(self,x_algolia_api_key, x_algolia_application_id, userID):
        cardsID = await self.getCardsId(x_algolia_api_key, x_algolia_application_id, userID)
        cards = await self.getUserCards(cardsID)
        return {'cards': cards}