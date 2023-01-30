from django.shortcuts import render, redirect

from .utils import *
from .playersDetail import MBADetail,NbaDetail
from .schedule import *
from .auth_sorare import AuthWithSorare

from django.contrib.auth.models import User
from asgiref.sync import sync_to_async, async_to_sync

from rest_framework.views import APIView
from rest_framework.response import Response



async def index(request):
    return render(request, 'service/index.html')


class Auth(APIView):
    
    """
        В Post запросе принимаю email и password
        Возвращаю userInfo со всеми данными о юзере(Jwt, userId , nickname и тд)
    """

    def get(self, request):

        code = self.request.query_params.get('code', None)

        if not code:
            return redirect('http://localhost:3000')

        # сохранить данные в бд

        return redirect(f'http://localhost:3000?code={code}')

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        userInfo = self.auth(email, password)
        if not userInfo:
            return Response(status=403)

        return Response(userInfo)

    @async_to_sync
    async def auth(self, email, password):

        try:
            JwtToken = await getJWT(email, password)
            userInfo = await getInfo(JwtToken)
        except:
            return None

        return {'userInfo': userInfo}


class GetUserInfo(APIView):

    def post(self, request):

        code = request.data.get('code')   
        userInfo : dict = self._auth(code)

        if not userInfo : 
            return Response(status=403)

        return Response(userInfo)

    @async_to_sync
    async def _auth(self, code):
        try:
            userInfo = await AuthWithSorare().getUserInfo(code)
        except:
            return None

        return {'userInfo': userInfo}


class UserCards(APIView):

    def post(self, request):
        x_algolia_api_key = request.data['x-algolia-api-key']
        x_algolia_application_id = request.data['x-algolia-application-id']
        userID = request.data['userID']
        sport = request.data['sport']

        cards = self.getCards(sport,x_algolia_api_key, x_algolia_application_id, userID)
        return Response(cards)

    @async_to_sync
    async def getCards(self,sport:str,x_algolia_api_key, x_algolia_application_id, userID):

        cards = None
        if sport.lower() == 'mba' :
            cards = await MBACards().getCards(x_algolia_api_key, x_algolia_application_id, userID)

        if sport.lower() == 'nba' :
            cards = await NBACards().getCards(x_algolia_api_key, x_algolia_application_id, userID)
        return {'cards': cards}


class PlayersDetail(APIView):

    def post(self, request):
        
        sport = request.data['sport']

        data = self.getPlayersDetail(sport)

        if data:
            return Response(data)

        return Response(status=500)

    @async_to_sync
    async def getPlayersDetail(self,sport:str):

        if sport.lower() == 'mba' :
            gpd = MBADetail()
 
 
        elif sport.lower() == 'nba' :
            gpd = NbaDetail()

        else : 
            return None
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
