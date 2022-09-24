from bcrypt import hashpw
import requests

"""
    Обернуть функции в блок Try и подумать над кодами возврата, чтобы на фронтеде отображалась ошибка
"""

def getJWT(email='armeno2004@gmail.com', password='Aboba2022@') : 

    """
        Принимаю: логин и пароль
        Возвращаю: JWT token
    """

    """
        сделать проверку на то правильно ввел юзер пароль или нет
    """

    salt = requests.get(f'https://api.sorare.com/api/v1/users/{email}').json()['salt']
    passwordHash = hashpw( bytes(password , 'utf-8') , bytes(salt , 'utf-8'))

    responce = requests.post('https://api.sorare.com/graphql' , 
            headers={'content-type': 'application/json', },
            json={
                "operationName": "SignInMutation",
                "variables": { "input": { "email": email, "password": passwordHash.decode() } },
                "query": "mutation SignInMutation($input: signInInput!) { signIn(input: $input) { currentUser { slug jwtToken(aud: \"<YourAud>\") { token expiredAt } } errors { message } } }",
                "data":{"signIn":{"currentUser":{"slug":"<YourSlug>","jwtToken":{"token":"<YourJWTToken>","expiredAt":"..."}},"errors":[]}}}).json()['data']['signIn']['currentUser']

    JWTtoken = responce['jwtToken']['token']

    return JWTtoken


def getInfo(JWT) : 
    
    """
        Принимаю: JWT токен,
        Возвращаю словарь : JWT, userID , nickname , algoliaApiKey, algoliaAppicationID
    """

    headers = {
        'content-type' : 'application/json' , 
        'Authorization' : f'Bearer {JWT}',
        'JWT-AUD' : '<YourAud>'
    }

    data = {
        "operationName": "ConfigQuery",
        "variables": {},
        "extensions": {
            "operationId": "React/79f363dbf0a16f25b7c4c916862fd82df2749c720ab0d54464f4d5a2f46488d0"
        }   
    }

    responce = requests.post('https://api.sorare.com/graphql' , headers=headers , json=data).json()['data']
   
    userId = responce['currentUser']['id'][5:]
    nickname = responce['currentUser']['nickname']

    algoliaApiKey = responce['config']["algoliaSearchApiKey"]
    algoliaApplicationId = responce['config']["algoliaApplicationId"]

    return {'JWT' : JWT ,'userID' : userId , 'nickname' : nickname , 'x-algolia-application-id' : algoliaApiKey , 'x-algolia-api-key' : algoliaApplicationId}


def getCardsID(algoliaApiKey , algoliaApplicationId, userID) : 

    """
        Принимаю: x-algolia-api-key, x-algolia-application-id , userID
        Возвращаю: массив из ID всех карточек
    """

    url = 'https://7z0z8pasdy-dsn.algolia.net/1/indexes/*/queries'
    headers = {
        'x-algolia-api-key' : algoliaApiKey,
        'x-algolia-application-id' : algoliaApplicationId 
    }
    body = {"requests":[{"indexName":"Card","params":f"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&hitsPerPage=40&analyticsTags=%5B%22Gallery%22%5D&filters=sport%3Abaseball&distinct=true&attributesToRetrieve=%5B%22asset_id%22%5D&attributesToHighlight=none&maxValuesPerFacet=30&page=0&facets=%5B%22user.id%22%2C%22rarity%22%5D&tagFilters=&facetFilters=%5B%22user.id%3A{userID}%22%5D"}]}
    responce = requests.post(url, headers=headers , json=body).json()

    cardsID = []
    for page in responce['results'] : 
        for id in page['hits'] : 
            cardsID.append(id['objectID'][16:])

    return cardsID



