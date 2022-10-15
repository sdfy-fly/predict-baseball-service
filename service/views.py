from django.shortcuts import render
from .utils import *

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async, async_to_sync

async def index(request):
    return render(request , 'service/index.html' )

class Auth(APIView): 

    """
        В Post запросе принимаю email и password
        Возвращаю userInfo со всеми данными о юзере(Jwt, userId , nickname и тд)
    """

    def post(self,request) : 
        email = request.data['email']
        password = request.data['password']

        userInfo = self.auth(email,password)
        if not userInfo : 
            return Response(status=403)

        # сохранить данные в бд

        return Response(userInfo)

    @async_to_sync
    async def auth(self,email,password) : 

        try : 
            JwtToken = await getJWT(email , password)
            userInfo = await getInfo(JwtToken)
        except : 
            return None
        
        return {'userInfo' : userInfo}


class UserCards(APIView) : 

    def post(self,request) : 
        
        x_algolia_api_key = request.data['x-algolia-api-key']
        x_algolia_application_id = request.data['x-algolia-application-id']
        userID = request.data['userID']

        cards = self.getCards(x_algolia_api_key , x_algolia_application_id, userID)
        return Response(cards)

    @async_to_sync
    async def getCards(self,x_algolia_api_key,x_algolia_application_id,userID) : 
        
        cardsID = await getCardsId(x_algolia_api_key, x_algolia_application_id, userID)
        cards = await getUserCards(cardsID)    
        return {'cards' : cards}

