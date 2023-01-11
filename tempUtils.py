import aiohttp
import asyncio


async def tempUtils_getAccessToken(code):
    
    headers = {
        'content-type': 'application/x-www-form-urlencoded' , 
        'User-Agent' : 'PostmanRuntime/7.30.0' , 
        'Accept' : '*/*'
    }

    params = {
        "client_id": "4jCGKupPezkAn_E5YNeoO2o2r0kOYNU0Y1iXTStVgT8",
        "client_secret": "m2cDDwXlDngRVXmh_1eQoU55mC_vofh7Hy4p7htqlKQ" , 
        "code" : code , 
        "grant_type" : "authorization_code" , 
        "redirect_uri" : "http://localhost:8000/api/auth"
    }


    async with aiohttp.ClientSession() as session:
        responce = (await (await session.post(f'https://api.sorare.com/oauth/token', headers=headers , params=params)).json())

    return responce['access_token']

async def tempUtils_getUserID(access_token):

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
        responce = (await (await session.post('https://api.sorare.com/graphql', headers=headers, json=data)).json())['data']
    
    userID = responce['currentUser']['id'][5:]
    nickname = responce['currentUser']['slug']

    return {'userID' : userID , 'nickname' : nickname}

async def tempUtils_getInfo(JWT):

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
        responce = (await (await session.post('https://api.sorare.com/graphql', headers=headers, json=data)).json())['data']

    algoliaApiKey = responce['config']["algoliaSearchApiKey"]
    algoliaApplicationId = responce['config']["algoliaApplicationId"]

    return {'x-algolia-application-id': algoliaApplicationId, 'x-algolia-api-key': algoliaApiKey}

async def tempUtils_getCardsId(algoliaApiKey, algoliaApplicationId, userID):

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

async def tempUtils_getUserCards(cardsID):
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

async def main():
    code = "RnfK5APaz-7C_HIq_JzOaBQtcUaEP1LN28DBlLGMCcc"
    
    # access_token = "dtBlFa7Mnur6op10TZznwHYYL0Wb_JZJ4M85kX2aw2s"
    # userID = (await getUserID(access_token))['userID']
    # userInfo = await getInfo(access_token)
    # cardsID = await getCardsId(userInfo['x-algolia-api-key'] , userInfo['x-algolia-application-id'] , userID)
 

asyncio.run(main())