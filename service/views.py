from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny

from .utils import *
from .playersDetail import GetPlayersDetail
from .schedule import *

from django.contrib.auth.models import User
from asgiref.sync import sync_to_async, async_to_sync

from rest_framework.views import APIView
from rest_framework.response import Response

from tempUtils import *


async def index(request):
    return render(request, 'service/index.html')


class Auth(APIView):
    """
        В Post запросе принимаю email и password
        Возвращаю userInfo со всеми данными о юзере(Jwt, userId , nickname и тд)
    """
    # permission_classes = [AllowAny]

    def get(self, request):

        code = self.request.query_params.get('code', None)
        ui : dict = self._testAuth(code)
        if not ui:
            return redirect('http://localhost:3000')

        # сохранить данные в бд
        # return render(request, 'service/index.html', {'code': code, 'userInfo': userInfo})
        # return Response(userInfo)
        return redirect(f'http://localhost:3000?code={code}')

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        userInfo = self.auth(email, password)
        if not userInfo:
            return Response(status=403)

        # сохранить данные в бд

        return Response(userInfo)

    @async_to_sync
    async def _testAuth(self, code):
        try:
            access_token = await tempUtils_getAccessToken(code)
            userInfo = await tempUtils_getInfo(access_token)
            user_ID_nickname = await tempUtils_getUserID(access_token)
            userInfo['userID'] = user_ID_nickname['userID']
            userInfo['nickname'] = user_ID_nickname['nickname']
            userInfo['accessToken'] = access_token
        except:
            return None
        return {'userInfo': userInfo}

    @async_to_sync
    async def auth(self, email, password):

        try:
            JwtToken = await getJWT(email, password)
            userInfo = await getInfo(JwtToken)
        except:
            return None

        return {'userInfo': userInfo}


class UserCards(APIView):

    def post(self, request):
        x_algolia_api_key = request.data['x-algolia-api-key']
        x_algolia_application_id = request.data['x-algolia-application-id']
        userID = request.data['userID']

        cards = self.getCards(x_algolia_api_key, x_algolia_application_id, userID)
        return Response(cards)

    @async_to_sync
    async def getCards(self, x_algolia_api_key, x_algolia_application_id, userID):
        cardsID = await getCardsId(x_algolia_api_key, x_algolia_application_id, userID)
        cards = await getUserCards(cardsID)
        return {'cards': cards}


class PlayersDetail(APIView):

    def post(self, request):

        data = self.getPlayersDetail()
        if data:
            return Response(data)

        return Response(status=500)

    @async_to_sync
    async def getPlayersDetail(self):
        gpd = GetPlayersDetail()
        try:
            data = await gpd.getData()
            return data
        except:
            return None


class GetSchesule(APIView):

    def post(self, request):
        data = self.getData()
        return Response(data)

    @async_to_sync
    async def getData(self):
        return await getSchedule()


class GetInjuryNews(APIView):

    def post(self, request):
        data = self.getData(request.data['date'])
        if data:
            return Response(data)
        else:
            return Response(status=500)

    @async_to_sync
    async def getData(self, date):

        try:
            return await getInjuryNews(date)
        except:
            return None
