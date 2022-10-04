from django.shortcuts import render
from .mba_async import *

import asyncio
import time

async def index(request):

    cards = None
    if request.method == 'POST' : 
        email = request.POST['email']
        password = request.POST['password']


        JwtToken = await getJWT(email , password)
        userInfo = await getInfo(JwtToken)
        cardsID = await getCardsId(userInfo['x-algolia-api-key'], userInfo['x-algolia-application-id'], userInfo['userID'])
        cards = await getUserCards(cardsID)    

        # await asyncio.sleep(5)
        # time.sleep(5)
        # print(f'{email} : {password}')

    return render(request , 'service/index.html' , {'cards' : cards})
