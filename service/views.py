from django.shortcuts import render
from .mba_async import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User


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


@api_view(('POST',))
async def auth(request) : 

    userInfo = None
    if request.method == 'POST' : 
        email = request.POST['email']
        password = request.POST['password']

        JwtToken = await getJWT(email , password)

        try : 
            userInfo = await getInfo(JwtToken)  
            # .... запись в бд
        except: 
            return Response(status=403)

    # return render(request , 'service/index.html' , {'userInfo' : userInfo})
    # return Response({'userInfo' : userInfo} , template_name='service/index.html' )
    return Response({'userInfo' : userInfo} , template_name='service/index.html')

@api_view(('POST',))
async def getCards(request):
    try : 
        cardsID = await getCardsId(request.POST['x-algolia-api-key'], request.POST['x-algolia-application-id'], request.POST['userID'])
        cards = await getUserCards(cardsID)    
        return Response({'cards' : cards})
    except: 
        return Response(status=403)

# сделать проверку на авторизацию 
# сделать таблицу игроков