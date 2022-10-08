from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .mba_async import *

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async, async_to_sync
from django.views.decorators.csrf import csrf_exempt
from django.views import View

async def index(request):

    # cards = None
    # if request.method == 'POST' : 
    #     email = request.POST['email']
    #     password = request.POST['password']

    #     JwtToken = await getJWT(email , password)

    #     try : 
    #         userInfo = await getInfo(JwtToken)
    #         cardsID = await getCardsId(userInfo['x-algolia-api-key'], userInfo['x-algolia-application-id'], userInfo['userID'])
    #         cards = await getUserCards(cardsID)    
    #     except: 
    #         return Response(status=403)

    return render(request , 'service/index.html' )


# @api_view(('POST',))
# async def auth(request) : 

#     userInfo = None

#     email = request.POST['email']
#     password = request.POST['password']

#     JwtToken = await getJWT(email , password)

#     try : 
#         userInfo = await getInfo(JwtToken)  
#         # .... запись в бд
#     except: 
#         return Response(status=403)

#     return Response({'userInfo' : userInfo})


# @csrf_exempt
# @async_to_sync
@api_view(('POST',))
async def auth(request) : 

    userInfo = None

    email = request.data['email']
    password = request.data['password']
    print(email , password)
    JwtToken = await getJWT(email , password)

    try : 
        userInfo = await getInfo(JwtToken)  
        # .... запись в бд
    except: 
        return Response(status=403)

    return JsonResponse({'userInfo' : userInfo})
    # sync_to_async
    # return Response({'userInfo' : userInfo})
    


@api_view(('POST',))
async def getCards(request):
    try : 
        cardsID = await getCardsId(request.POST['x-algolia-api-key'], request.POST['x-algolia-application-id'], request.POST['userID'])
        cards = await getUserCards(cardsID)    
        return Response({'cards' : cards})
    except: 
        return Response(status=403)


class Action(APIView) : 

    def get(self,request):
        return render(request , 'service/index.html' )


    def post(self,request) : 
        email = request.data['email']
        password = request.data['password']

        # card = async_to_sync(self.action(email , password))
        cards = self.action(email , password)
        return Response(cards)

    @async_to_sync
    async def action(self,email,password) : 
        JwtToken = await getJWT(email , password)
        userInfo = await getInfo(JwtToken)
        cardsID = await getCardsId(userInfo['x-algolia-api-key'], userInfo['x-algolia-application-id'], userInfo['userID'])
        cards = await getUserCards(cardsID)    
        return {'cards' : userInfo}



# сделать проверку на авторизацию 
# сделать таблицу игроков