from bcrypt import hashpw
import requests

def getJWT(email='armeno2004@gmail.com', password='Aboba2022@') : 
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

    """
        сделать ебаную проверку на то правильно ввел юзер пароль или нет
    """
    return JWTtoken

    # if JWTtoken.status_code == '200' : 
    #     pass
    # else : 
    #     return 'Неверный логин или пароль'


# token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzMTI5ZWNiMi05ZDI2LTQ5M2MtODYxNC1kYjIzMjBhOTJlYmMiLCJzY3AiOiJ1c2VyIiwiYXVkIjoiPFlvdXJBdWQ-IiwiaWF0IjoxNjYzNjAzOTMzLCJleHAiOiIxNjk1MTYwODg1IiwianRpIjoiODBiM2EzYjktNTZhMi00YTM0LWI0ZjQtNGZkYzcyY2RjN2U0In0.AiEkzesIsuisFsR3yr6YjsITWEgYMUxgfRDWUXD9L8I'
4334t3t

def getUserID(JWT) : 
    
    """
        Принимаю JWT токен, отправляю запрос и получаю userID и nickname юзера.
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

    responce = requests.post('https://api.sorare.com/graphql' , headers=headers , json=data).json()
   
    userId = responce['data']['currentUser']['id'][5:]

    nickname = responce['data']['currentUser']['nickname']

    return {'userID' : userId , 'nickname' : nickname}


# token = getJWT()
# getUserID(token)

"""

+ 1) получение токена 
+ 2) получение userID
- 3) получение всех ID карточек юзера по его userID
- 4) получение всех карточек юзера 
- 5) отправка json на фронтенд

"""